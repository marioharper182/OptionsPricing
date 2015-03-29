__author__ = 'Mario'
import numpy as np
from EuropeanGreeks import *
from scipy.stats import norm


class EuropeanLookback():
    def __init__(self, strike, t, expiry, spot, sigma, rate, dividend, alpha, dt):

        # Instantiate variables
        self.strike = strike
        self.t = t
        self.expiry = expiry
        self.tau = expiry - t
        self.spot = spot
        self.sigma = sigma
        self.sigma2 = sigma2 = sigma**2
        self.rate = rate
        self.dividend = dividend
        self.alpha = alpha
        self.dt = dt

        self.Vbar = 0
        self.xi = xi = 0

        self.N = N = 1000
        self.M = M = 5000

        beta1 = -.88
        beta2 = -.42
        beta3 = -.0003

        ### Calculate the trivial lookback option
        newdt = float(expiry)/float(N) # Get the dt for the Weiner process
        dW = np.sqrt(newdt)*np.random.normal(0,1,(M,N-1)) # Create the brownian motion
        W = np.cumsum(dW, axis=1) # Set up the Weiner Process as a Matrix
        time = np.linspace(0, expiry, N) # Set the discrete time space
        tempA = np.zeros((M,1)) # Create an initial zero vector for the first column
        Wnew = np.c_[tempA,W] # Append the Weiner matrix to the zeros
        tt = np.tile(np.array(time),(M,1)) # Create a matrix of time x M so we have time for every iteration

        ### Calculate the lookback option ###
        assetpath = spot*np.exp((rate-.5*sigma2)*tt+sigma*Wnew) #European standard
        max_vals = [max(assetpath[i]) for i in range(0 , len(assetpath))]
        option_val = [max(i-strike,0) for i in np.array(max_vals)]
        call_val = np.mean(option_val)
        present_val = np.exp(-rate*expiry)*call_val
        print(present_val)

        self.tau = tau = self.expiry-self.t

        self.matrixengine(spot, rate, sigma, expiry, N, M, strike, sigma2)
        self.montecarloengine()

    def matrixengine(self, spot, rate, sigma, expiry, N, M, strike, sigma2):
        ### Calculate the trivial lookback option
        newdt = float(expiry)/float(N) # Get the dt for the Weiner process
        dW = np.sqrt(newdt)*np.random.normal(0,1,(M,N-1)) # Create the brownian motion
        W = np.cumsum(dW, axis=1) # Set up the Weiner Process as a Matrix
        time = np.linspace(0, expiry, N) # Set the discrete time space
        tempA = np.zeros((M,1)) # Create an initial zero vector for the first column
        Wnew = np.c_[tempA,W] # Append the Weiner matrix to the zeros
        tt = np.tile(np.array(time),(M,1)) # Create a matrix of time x M so we have time for every iteration

        ### Calculate the lookback option ###
        assetpath = spot*np.exp((rate-.5*sigma2)*tt+sigma*Wnew) #European standard
        max_vals = [max(assetpath[i]) for i in range(0 , len(assetpath))]
        option_val = [max(i-strike,0) for i in np.array(max_vals)]
        call_val = np.mean(option_val)
        present_val = np.exp(-rate*expiry)*call_val
        print(present_val)

        ### Initialize Control Variates ###
        sig2 = self.sigma**2
        alphadt = self.alpha*self.dt
        xisdt = self.xi*np.sqrt(self.dt)
        erddt = np.exp((self.rate-self.dividend)*self.dt)
        egam1 = np.exp(2*(self.rate-self.dividend)*self.dt)
        egam2 = -2*erddt + 1
        eveg1 = np.exp(-self.alpha*self.dt)
        eveg2 = self.Vbar - self.Vbar*eveg1

        ### Calculate the general solution to the lookback option (analytic)
        a1 = 1/(sigma*np.sqrt(expiry-time)) * (np.log(spot/option_val) + (rate+.5*sigma2)*(expiry-time))
        a2 = 1/(sigma*np.sqrt(expiry-time)) * (np.log(spot/option_val) - (rate+.5*sigma2)*(expiry-time))
        a3 = 1/(sigma*np.sqrt(expiry-time)) * (np.log(option_val/spot) - (rate+.5*sigma2)*(expiry-time))
        alpha = (2*rate)/sigma2
        Analytic_ish = spot*(norm(a1)*(1+1/alpha)-1) + option_val*np.exp(-rate*(expiry-time))*(norm(a3)-1/alpha *(option_val/spot)**(alpha-1) * norm(a2))

    def montecarloengine(self):

        # Calculate the parameter shorthand that we need for the control variates
        sig2 = self.sigma**2
        alphadt = self.alpha*self.dt
        xisdt = self.xi*np.sqrt(self.dt)
        erddt = np.exp((self.rate-self.dividend)*self.dt)
        egam1 = np.exp(2*(self.rate-self.dividend)*self.dt)
        egam2 = -2*erddt + 1
        eveg1 = np.exp(-self.alpha*self.dt)
        eveg2 = self.Vbar - self.Vbar*eveg1

        sum_CT = 0
        sum_CT2 = 0



        for j in range(1, self.M):
            St1 = []
            St2 = []
            St1.append(self.spot)
            St2.append(self.spot)
            Vt = sig2

            MaxSt1 = max(St1)
            MaxSt2 = max(St2)
            cv1, cv2, cv3 = 0,0,0

            # Initialize the d1, d2 variables for use in the control variates
            d1_St1 = EuroD1(MaxSt1, self.strike, self.rate, self.dividend, self.sigma, self.tau)
            d1_St2 = EuroD1(MaxSt2, self.strike, self.rate, self.dividend, self.sigma, self.tau)
            d2_St1 = EuroD2(d1_St1, self.sigma, self.tau)
            d2_St2 = EuroD2(d1_St2, self.sigma, self.tau)

            for i in range(1, self.N):
                # These are the hedge sensitivites
                t = (i-1)*self.dt
                delta1 = (d1_St1)
                delta2 = (d1_St2)
                gamma1 = EuroGamma(d1_St1, MaxSt1, self.sigma, self.tau)
                gamma2 = EuroGamma(d1_St2, MaxSt2, self.sigma, self.tau)
                vega1 = EuroVega(d1_St1, self.tau, MaxSt1)
                vega2 = EuroVega(d1_St2, self.tau, MaxSt2)

                # Evolution of Variance
                e = np.random.normal(0,1)
                Vtn = Vt + alphadt*(self.Vbar - Vt) + xisdt*np.sqrt(Vt)*e

                # Evolution of Asset Price
                Stn1 = St1 * np.exp( (self.rate-self.dividend-.5*Vt)*self.dt + np.sqrt(Vt)*xisdt*e)
                Stn2 = St1 * np.exp( (self.rate-self.dividend-.5*Vt)*self.dt + np.sqrt(Vt)*xisdt*-e)

                # Process the Control Variates
                cv1 = cv1 + delta1*(Stn1 - St1*erddt) + delta2*(Stn2 - St2*erddt)
                cv2 = cv2 + gamma1*((Stn1-St1)^2 - St1^2 * (egam1*np.exp(Vt*self.dt)+egam2)) + \
                      gamma2*((Stn2-St2)^2 - St2^2*(egam1*np.exp(Vt*self.dt)+egam2))
                cv3 = cv3 + vega1*((Vtn-Vt)-(Vt*eveg1+eveg2-Vt)) + \
                      vega2*((Vtn-Vt)-(Vt*eveg1+eveg2-Vt))

    def SetVbar(self, Vbar):
        self.Vbar = Vbar

    def Setxi(self, xi):
        self.xi = xi

    def SetN(self, N):
        self.N = N

    def SetM(self, M):
        self.M = M

    def GetVariables(self):
        vardic = {}
        vardic['strike'] = self.strike
        vardic['t'] = self.t
        vardic['expiry'] = self.expiry
        vardic['S'] = self.spot
        vardic['sig'] = self.sigma
        vardic['r'] = self.rate
        vardic['div'] = self.dividend
        vardic['alpha'] = self.alpha
        vardic['Vbar'] = self.Vbar
        vardic['xi'] = self.xi
        vardic['N'] = self.N
        vardic['M'] = self.M

        return vardic

def main():

    ###### Initialize Parameters ######
    strike = 80
    t = 1
    expiry = 10
    spot = 105
    sigma = .3
    rate = .03
    dividend = 0
    # Alpha apparently measures performance compared to the projected performance
    alpha = .69
    ## Variables that I have no clue what they mean ##
    Vbar = 0
    xi = 0
    # Steps in time
    N = 10
    #Number of simulations
    M = 100

    ## TODO: Figure out what to set dt to
    dt = 1

    EuropeanLookback(strike=strike, spot=spot, t=t, expiry=expiry, sigma=sigma, dividend=dividend, alpha=alpha, rate=rate, dt=dt)


if __name__ == '__main__':
    main()