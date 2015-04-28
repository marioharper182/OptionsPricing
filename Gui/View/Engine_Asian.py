__author__ = 'HarperMain'

import numpy as np
from numpy import sqrt, exp, pi
from matplotlib import pyplot

class AsianOption(object):
    def __init__(self, spot, rate, sigma, expiry, N, M, strike, flag):
        self.matrixengine(float(spot), float(rate), float(sigma), float(expiry),
                          int(N), int(M), float(strike), flag)

    def matrixengine(self, spot, rate, sigma, expiry, N, M, strike, flag):

        newdt = float(expiry)/float(N) # Get the dt for the Weiner process
        dW = np.sqrt(newdt)*np.random.normal(0,1,(M,N-1)) # Create the brownian motion
        W = np.cumsum(dW, axis=1) # Set up the Weiner Process as a Matrix
        time = np.linspace(0, expiry, N) # Set the discrete time space
        tempA = np.zeros((M,1)) # Create an initial zero vector for the first column
        Wnew = np.c_[tempA,W] # Append the Weiner matrix to the zeros
        tt = np.tile(np.array(time),(M,1)) # Create a matrix of time x M so we have time for every iteration

        ### Calculate the lookback option ###
        assetpath = spot*np.exp((rate-.5*sigma*sigma)*tt+sigma*Wnew) #European standard
        avevals = [np.average(assetpath[i]) for i in range(0 , len(assetpath))]
        if flag == 'c':
            option_val = [max(i-strike,0) for i in np.array(avevals)]
        else:
            option_val = [max(strike-i,0) for i in np.array(avevals)]
        value = np.mean(option_val)
        present_val = np.exp(-rate*expiry)*value
        # print('This is the matrix, naive monte carlo: ',present_val)

        sum_CT = sum(option_val)
        sum_CT2 = sum([i**2 for i in option_val])

        self.SD = np.sqrt((sum_CT2 - sum_CT*sum_CT/M)*np.exp(-2*rate*expiry)/(M-1))
        self.SE = self.SD/np.sqrt(M)
        self.price = present_val


    def GetPrice(self):
        return [self.price, self.SD, self.SE]
