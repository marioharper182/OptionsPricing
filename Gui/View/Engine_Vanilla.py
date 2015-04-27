__author__ = 'HarperMain'
import numpy as np
from numpy import exp, log, sqrt

class Vanilla(object):
    def __init__(self, flag, S, K, r, v, T, div):
        self.Vanilla = self.BlackSholes(flag, float(S),
                                        float(K), float(r), float(v),
                                        float(T), float(div))
        self.GetValue()

    def BlackSholes(self, CallPutFlag,S,K,r,v,T, div):

        d1 = (log(S/K)+(r-div+v*v/2.)*T)/(v*sqrt(T))

        d2 = d1-v*sqrt(T)
        if CallPutFlag=='c':

            return S*exp(-div*T)*self.norm_cdf(d1)-K*exp(-r*T)*self.norm_cdf(d2)

        else:

            return K*exp(-r*T)*self.norm_cdf(-d2)-S*exp(-div*T)*self.norm_cdf(-d1)

    def norm_pdf(self, x):
        """Standard normal probability density function"""
        return (1.0/((2*np.pi)**0.5))*exp(-0.5*x*x)

    def norm_cdf(self, x):
        """An approximation to the cumulative distribution function for the standard normal distribution:
        N(x) = \frac{1}{sqrt(2*\pi)} \int^x_{-\infty} e^{-\frac{1}{2}s^2} ds"""
        k = 1.0/(1.0+0.2316419*x)
        k_sum = k*(0.319381530 + k*(-0.356563782 + k*(1.781477937 + k*(-1.821255978 + 1.330274429*k))))

        if x >= 0.0:
            return (1.0 - (1.0/((2*np.pi)**0.5))*exp(-0.5*x*x) * k_sum)
        else:
            return 1.0 - self.norm_cdf(-x)

    def GetValue(self):
        return self.Vanilla