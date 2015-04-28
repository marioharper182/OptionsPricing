__author__ = 'Mario'

import numpy as np
from scipy.stats import norm

class EuropeanLookback():
    def __init__(self, strike, expiry, spot, sigma, rate, dividend, M, flag, N=100, Vbar=.12, alpha=.69):

        # Instantiate variables
        self.strike = float(strike)
        self.expiry = float(expiry)
        self.spot = float(spot)
        self.sigma = float(sigma)
        self.sigma2 = sigma2 = float(sigma)*float(sigma)
        self.rate = float(rate)
        self.dividend = float(dividend)
        self.alpha = float(alpha)
        self.dt = float(expiry)/float(N)

        self.Vbar = Vbar
        self.xi = xi = .025

        self.N = N
        self.M = int(M)

        self.beta1 = -.88
        self.beta2 = -.42
        self.beta3 = -.0003

        self.alphadt = self.alpha*self.dt
        self.xisdt = self.xi*np.sqrt(self.dt)
        self.erddt = np.exp((self.rate-self.dividend)*self.dt)
        self.egam1 = np.exp(2*(self.rate-self.dividend)*self.dt)
        self.egam2 = -2*self.erddt + 1
        self.eveg1 = np.exp(-self.alpha*self.dt)
        self.eveg2 = self.Vbar - self.Vbar*self.eveg1


        self.VectorizedMonteCarlo(float(spot), float(rate), float(sigma),
                                  float(expiry), int(N), int(M), float(strike),
                                  float(sigma2), flag)


    def VectorizedMonteCarlo(self, spot, rate, sigma, expiry, N, M, strike, sigma2, flag):
        # Initialize the matrices
        newdt = float(expiry)/float(N) # Get the dt for the Weiner process
        dW = np.sqrt(newdt)*np.random.normal(0,1,(M,N-1)) # Create the brownian motion
        W = np.cumsum(dW, axis=1) # Set up the Weiner Process as a Matrix
        time = np.linspace(0, expiry, N) # Set the discrete time space
        tempA = np.zeros((M,1)) # Create an initial zero vector for the first column

        #This is the Random aspects and the stochastic volatility
        Wnew = np.c_[tempA,W] # Append the Weiner matrix to the zeros vector
        Vt = self.sigma2
        Vtn = np.abs(Vt + self.alphadt*(self.Vbar - Vt) + self.xisdt*np.sqrt(Vt)*Wnew)
        tt = np.tile(np.array(time),(M,1)) # Create a matrix of time x M so we have time for every iteration
        self.tau = expiry-1

        ### Calculate the lookback option ###
        assetpath1 = np.array(spot*np.exp((rate-.5*Vtn)*tt+np.sqrt(Vtn)*Wnew)) #European standard Antithetic1
        assetpath2 = np.array(spot*np.exp((rate-.5*Vtn)*tt+np.sqrt(Vtn)*-Wnew)) #European standard Antithetic2

        d1_St1 = EuroD1(assetpath1, strike, rate, self.dividend, sigma, self.tau)
        d1_St2 = EuroD1(assetpath2, strike, rate, self.dividend, sigma, self.tau)
        delta1 = (d1_St1)
        delta2 = (d1_St2)
        gamma1 = EuroGamma(d1_St1, assetpath1, sigma, self.tau)
        gamma2 = EuroGamma(d1_St2, assetpath2, sigma, self.tau)
        vega1 = EuroVega(d1_St1, self.tau, assetpath1)
        vega2 = EuroVega(d1_St2, self.tau, assetpath2)

        St1n = assetpath1
        # St1n = np.c_[assetpath1, assetpath1[:,-1]]
        St2n = assetpath2
        # St2n = np.c_[assetpath2, assetpath2[:,-1]]
        St1 = np.delete(np.c_[tempA, assetpath1],-1,1)
        St2 = np.delete(np.c_[tempA, assetpath2],-1,1)

        Vt = np.delete(np.c_[Vt+tempA, Vtn],-1,1)
        # Vtn = np.c_[Vtn, Vtn[:, -1]]

        cv1, cv2, cv3 = 0,0,0 # PreAllocate the ControlVariates
        # Define ControlVariate Params
        cv1 = cv1 + delta1*(St1n - St1*self.erddt) + delta2*(St2n - St2*self.erddt)
        cv2 = cv2 + gamma1*((St1n-St1)**2 - St1**2 * (self.egam1*np.exp(Vt*self.dt)+self.egam2)) + \
              gamma2*((St2n-St2)**2 - St2**2*(self.egam1*np.exp(Vt*self.dt)+self.egam2))
        cv3 = cv3 + vega1*((Vtn-Vt)-(Vt*self.eveg1+self.eveg2-Vt)) + \
              vega2*((Vtn-Vt)-(Vt*self.eveg1+self.eveg2-Vt))

        # Assign Antithetics Maxima's
        max_vals1 = np.array([max(assetpath1[i]) for i in range(0 , len(assetpath1))])
        max_vals2 = np.array([max(assetpath1[i]) for i in range(0 , len(assetpath1))])
        CT = .5*((max_vals1 - self.strike) + (max_vals2 - self.strike) +
                 self.beta1*cv1[:,-1] + self.beta2*cv2[:,-1] + self.beta3*cv3[:,-1])

        sum_CT = sum(CT)
        sum_CT2 = sum([i**2 for i in CT])

        call_value = sum_CT/self.M *np.exp(-self.rate*self.expiry)
        self.SD = np.sqrt((sum_CT2 - sum_CT*sum_CT/self.M)*np.exp(-2*self.rate*self.expiry)/(self.M-1))
        self.SE = self.SD/np.sqrt(self.M)
        # print('This is the CV method with Stochastic Volatility: ', call_value)
        # print(self.SD, self.SE)

        if flag == 'c':
            option_val = np.array([max(i-strike,0) for i in np.array(max_vals1)])
        else:
            option_val = np.array([max(strike-i,0) for i in np.array(max_vals1)])
        call_val = np.mean(option_val)
        self.present_val = np.exp(-rate*expiry)*call_val
        # print('This is the matrix, naive monte carlo: ',present_val)

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
        # vardic['t'] = self.t
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

    def GetPrice(self):
        return [self.present_val, self.SD, self.SE]


def EuroDelta(d1):
    # Delta is the price sensitivity
    Delta = norm.cdf(d1)
    return Delta

def EuroGamma(d1, spot, sigma, tau):
    # Gamma is a second order time-price sensitivity
    Gamma = norm.ppf(norm.cdf(d1)) / (spot*sigma*np.sqrt(tau))
    return Gamma

def EuroTheta(d1, d2, rate, strike, tau, sigma, spot):
    # Theta is the time sensitivity
    Theta = -rate*strike*np.exp(-rate*tau) * norm.cdf(d2) - \
            (sigma*spot*norm.ppf(norm.cdf(d1))/(2*tau))
    return Theta

def EuroRho(d2, tau, strike, rate):
    # Rho is the interest rate sensitivity
    Rho = tau*strike*np.exp(-rate*tau) * norm.cdf(d2)
    return Rho

def EuroVega(d1, tau, spot):
    # Vega is a volatility sensitivity
    Vega = np.sqrt(tau)*spot*norm.cdf(d1)
    return Vega

def EuroD1(spot, strike, rate, dividend, sigma, tau):
    d1 = ((np.log(spot/strike) + (rate - dividend + 1/2 *
                                 sigma**2)*tau))/ (np.sqrt(tau))
    return d1

def EuroD2(d1, sigma, tau):
    d2 = d1 - sigma * np.sqrt(tau)
    return d2
### FOR TESTING PURPOSES ONLY ###
#
# def main():
#
#     ###### Initialize Parameters ######
#     strike = 80
#     t = 1
#     expiry = 10
#     spot = 105
#     sigma = .3
#     rate = .03
#     dividend = 0
#     # Alpha apparently measures performance compared to the projected performance
#     alpha = .69
#     ## Variables that I have no clue what they mean ##
#     Vbar = 0
#     xi = 0
#     # Steps in time
#     N = 10
#     #Number of simulations
#     M = 100
#
#     ## TODO: Figure out what to set dt to
#     dt = 1
#
#     EuropeanLookback(strike=strike, spot=spot, t=t, expiry=expiry, sigma=sigma, dividend=dividend, alpha=alpha, rate=rate, dt=dt)
#
#
# if __name__ == '__main__':
#     main()