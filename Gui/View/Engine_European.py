__author__ = 'HarperMain'

import numpy as np
from numpy import sqrt, exp, pi
from matplotlib import pyplot

class EuropeanOption(object):
    def __init__(self, spot, rate, sigma, expiry, N, M, strike, sigma2):
        self.matrixengine(spot, rate, sigma, expiry, N, M, strike, sigma2)
        self.price = 0


    def matrixengine(self, spot, rate, sigma, expiry, N, M, strike, sigma2):

        newdt = float(expiry)/float(N) # Get the dt for the Weiner process
        dW = np.sqrt(newdt)*np.random.normal(0,1,(M,N-1)) # Create the brownian motion
        W = np.cumsum(dW, axis=1) # Set up the Weiner Process as a Matrix
        time = np.linspace(0, expiry, N) # Set the discrete time space
        tempA = np.zeros((M,1)) # Create an initial zero vector for the first column
        Wnew = np.c_[tempA,W] # Append the Weiner matrix to the zeros
        tt = np.tile(np.array(time),(M,1)) # Create a matrix of time x M so we have time for every iteration

        ### Calculate the lookback option ###
        assetpath = spot*np.exp((rate-.5*sigma2)*tt+sigma*Wnew) #European standard
        endvals = [(assetpath[i][-1]) for i in range(0 , len(assetpath))]
        option_val = [max(i-strike,0) for i in np.array(endvals)]
        call_val = np.mean(option_val)
        present_val = np.exp(-rate*expiry)*call_val
        print('This is the matrix, naive monte carlo: ',present_val)

        sum_CT = sum(option_val)
        sum_CT2 = sum([i**2 for i in option_val])

        self.SD = np.sqrt((sum_CT2 - sum_CT*sum_CT/M)*np.exp(-2*rate*expiry)/(M-1))
        self.SE = self.SD/np.sqrt(M)
        print(self.SD, self.SE)

        self.price = present_val


    def GetPrice(self):
        return [self.price, self.SD, self.SE]