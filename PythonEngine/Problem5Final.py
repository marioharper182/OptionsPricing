__author__ = 'HarperMain'

import numpy as np
import matplotlib.pyplot as plt
from numpy import sqrt, exp, pi
from matplotlib import pyplot

class EuropeanOption(object):
    def __init__(self, spot, rate, sigma, sigma2, roe, expiry, dividend = 0.0, N=12, M=10000, flag='c'):
        self.matrixengine(spot, rate, sigma, sigma2, roe, expiry, dividend,
                          N, M, flag)

    def matrixengine(self, spot, rate, sigma, sigma2, roe, expiry, dividend, N, M, flag):

        newsig1 = sigma*(1-roe*roe)
        newsig2 = sigma2*(1-roe*roe)

        newdt = float(expiry)/int(N) # Get the dt for the Weiner process
        dW = np.sqrt(newdt)*np.random.normal(0,1,(M,N-1)) # Create the brownian motion
        dW2 = np.sqrt(newdt)*np.random.normal(0,1,(M,N-1)) # Create the brownian motion
        W = np.cumsum(dW, axis=1) # Set up the Weiner Process as a Matrix
        W2 = np.cumsum(dW2, axis=1) # Set up the Weiner Process as a Matrix
        time = np.linspace(0, expiry, N) # Set the discrete time space
        tempA = np.zeros((M,1)) # Create an initial zero vector for the first column
        Wnew = np.c_[tempA,W] # Append the Weiner matrix to the zeros
        Wnew2 = np.c_[tempA,W2] # Append the Weiner matrix to the zeros
        tt = np.tile(np.array(time),(M,1)) # Create a matrix of time x M so we have time for every iteration
        tt2 = np.tile(np.array(time),(M,1)) # Create a matrix of time x M so we have time for every iteration

        ### Calculate the lookback option ###
        assetpath = spot*np.exp((rate+dividend-.5*newsig1*newsig1)*tt+newsig1*Wnew) #European standard
        assetpath2 = spot*np.exp((rate+dividend-.5*newsig2*newsig2)*tt2+newsig2*Wnew2)
        endvals = [(assetpath[i][-1]) for i in range(0 , len(assetpath))]
        endvals2 = [(assetpath2[i][-1]) for i in range(0 , len(assetpath))]
        if flag == 'c':
            option_val1 = [max(endvals[i]-endvals2[i],0) for i in range(len(np.array(endvals)))]
            option_val2 = [max(endvals[i]/endvals2[i] - 1,0) for i in range(len(np.array(endvals)))]
        else:
            option_val1 = [max(endvals2[i]-endvals[i],0) for i in range(len(np.array(endvals)))]
            option_val2 = [max(endvals2[i]/endvals[i] - 1,0) for i in range(len(np.array(endvals)))]
        value = np.mean(option_val1)
        value2 = np.mean(option_val2)
        present_val = np.exp(-rate*expiry)*value
        self.present_val2 = np.exp(-rate*expiry)*value2
        # print('This is the matrix, naive monte carlo: ',present_val)

        sum_CT = sum(option_val1)
        sum_CT2 = sum([i**2 for i in option_val1])

        # self.SD = np.sqrt((sum_CT2 - sum_CT*sum_CT/M)*np.exp(-2*rate*expiry)/(M-1))
        # self.SE = self.SD/np.sqrt(M)
        self.price = present_val
        self.paths = assetpath
        print("The price of asset1-asset2 is: ",self.GetPrice())
        print("The ratio price is: ",self.RatioPrice())
        # self.Plot()

    def RatioPrice(self):
        return self.present_val2

    def GetPrice(self):
        return self.price

    def Plot(self):
        T = range(self.paths.shape[1])

        for i in range(self.paths.shape[0]):
            plt.plot(T, self.paths[i,:])

        plt.show()

### FOR TESTING PURPOSES ONLY ###

def main():

    ###### Initialize Parameters ######

    expiry = 1
    spot = 100
    sigma1 = .35
    sigma2 = .25
    rate = .06
    roe = .40

    EuropeanOption(spot, rate, sigma1, sigma2, roe, expiry, dividend=0.05,flag='c')


if __name__ == '__main__':
    main()