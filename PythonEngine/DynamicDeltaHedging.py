__author__ = 'HarperMain'

import numpy as np
from numpy import log, exp, sqrt
from scipy.stats import norm
from VanillaClass import Vanilla


class Prob3(object):
    def __init__(self):
        self.initialparameters()
        self.Engine()

        # A = self.EuroD1(self.spot, self.strike, self.rate, self.dividend, self.sigma, self.dt)
        # print norm.cdf(A)
        # print(A)

    def initialparameters(self):
        # Set up initial params here
        self.expiry = 91.0
        self.spot = 40.0
        self.strike = 40.0
        self.strike2 = 45.0
        self.sigma = .3
        self.rate = .08
        self.year = 365.0
        self.dividend = 0
        self.dt = self.expiry/self.year

        #Set some lists to capture information as it comes
        self.spotlist = [40,39,40.25,41.20,40.75,39.55,38.75,41.85]
        self.asset40Valuelist = []
        self.asset45Valuelist = []
        self.portfolioDelta = []

        #Other changing variables
        self.buyasset40 = 0
        self.sellasset45 = 0
        self.cash = 0

    def Engine(self):
        count = 0
        for i in range(len(self.spotlist)):
            self.spot = self.spotlist[count]
            self.RetrieveOption()
            if count == 0:
                self.buyasset40 = -self.asset40Valuelist[-1]
                self.sellasset45 = self.asset45Valuelist[-1]
                short = self.portfolioDelta[-1]*self.spot
                print("The initial amount of cash is: ", short+self.sellasset45+self.buyasset40)
                self.cash = short+self.sellasset45+self.buyasset40
            else:
                self.buyasset40 = self.asset40Valuelist[-1]
                self.sellasset45 = -1*self.asset45Valuelist[-1]
                sharesowed = -1*self.portfolioDelta[-2]*self.spot
                loanincome = self.cash*exp(self.rate*1/self.year)
                self.overnight = self.buyasset40+self.sellasset45+sharesowed+loanincome
                print("The overnight change for day",count,"is: ", self.overnight)
                newbalance = self.portfolioDelta[-1]-self.portfolioDelta[-2]
                self.cash = self.cash - newbalance*self.spot


            self.expiry = self.expiry-1
            self.dt = self.expiry/self.year
            count = count+1


    def RetrieveOption(self):
        asset40 = Vanilla('c',self.spot, self.strike, self.rate, self.sigma, self.dt, self.dividend)
        Value40 = asset40.GetValue()
        Delta40 = asset40.GetDelta()

        asset45 = Vanilla('c',self.spot, self.strike2, self.rate, self.sigma, self.dt, self.dividend)
        Value45 = asset45.GetValue()
        Delta45 = asset45.GetDelta()

        self.asset40Valuelist.append(Value40)
        self.asset45Valuelist.append(Value45)
        self.portfolioDelta.append(Delta40-Delta45)

def main():

    ###### Initialize Parameters ######

    expiry = 91
    spot = 40
    strike = 40
    sigma1 = .3
    # sigma2 = .25
    rate = .08
    # roe = .40

    Prob3()


if __name__ == '__main__':
    main()