__author__ = 'HarperMain'

from scipy.stats import norm
import numpy as np

# class EuropeanLookbackGreeks():
#
#     def __init__(self, spot, strike, rate, dividend, sigma, expiry, t):
#
#         self.spot = spot
#         self.strike = strike
#         self.rate = rate
#         self.dividend = dividend
#         self.sigma = sigma
#         self.expiry = expiry
#         self.t = t
#
#         self.tau = tau = self.expiry-self.t
#         self.d1 = (np.log(spot/strike) + (rate - dividend + 1/2 * sigma**2)*tau) / (np.sqrt(tau))
#         self.d2 = self.d1 - sigma * np.sqrt(tau)
#
#         self.Delta = self.EuroDelta()
#         self.Gamma = self.EuroGamma()
#         self.Theta = self.EuroTheta(rate, strike, tau, sigma, spot)
#         self.Rho = self.EuroRho(tau, strike, rate)
#         self.Vega = self.EuroVega(tau, spot)

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
    d1 = (np.log(spot/strike) + (rate - dividend + 1/2 *
                                 sigma**2)*tau) / (np.sqrt(tau))
    return d1

def EuroD2(d1, sigma, tau):
    d2 = d1 - sigma * np.sqrt(tau)
    return d2

    # def ReturnGreeks(self):
    #     EuroGreeks = {}
    #     EuroGreeks['Delta'] = self.Delta
    #     EuroGreeks['Gamma'] = self.Gamma
    #     EuroGreeks['Theta'] = self.Theta
    #     EuroGreeks['Rho'] = self.Rho
    #     EuroGreeks['Vega'] = self.Vega
    #
    #     return EuroGreeks