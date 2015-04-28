# from mibian import BS, Me
from math import log, e
from scipy.stats import norm

class ImpliedVolatility(object):

    def __init__(self, spot, strike, rate, dividend, expiry, flag, price,
                 volatility=None):
        spot = float(spot)
        strike = float(strike)
        rate = float(rate)
        dividend = float(dividend)
        expiry = float(expiry)*252
        price = float(price)

        if flag =='c':
            call = price
            self.Option = Me([spot, strike, rate, dividend, expiry], callPrice=call)
        else:
            put = price
            self.Option = Me([spot, strike, rate, dividend, expiry], putPrice=put)

    def GetImpliedVol(self):
        return self.Option.impliedVolatility


class Me:

    def __init__(self, args, volatility=None, callPrice=None, putPrice=None, \
            performance=None):
        self.underlyingPrice = float(args[0])
        self.strikePrice = float(args[1])
        self.interestRate = float(args[2]) / 100
        self.dividend = float(args[3])
        self.dividendYield = self.dividend / self.underlyingPrice
        self.daysToExpiration = float(args[4]) / 365

        for i in ['callPrice', 'putPrice', 'callDelta', 'putDelta', \
                'callDelta2', 'putDelta2', 'callTheta', 'putTheta', \
                'callRho', 'putRho', 'vega', 'gamma', 'impliedVolatility', \
                'putCallParity']:
            self.__dict__[i] = None

        if volatility:
            self.volatility = float(volatility) / 100

            self._a_ = self.volatility * self.daysToExpiration**0.5
            self._d1_ = (log(self.underlyingPrice / self.strikePrice) + \
                    (self.interestRate - self.dividendYield + \
                    (self.volatility**2) / 2) * self.daysToExpiration) / \
                    self._a_
            self._d2_ = self._d1_ - self._a_
            if performance:
                [self.callPrice, self.putPrice] = self._price()
            else:
                self.exerciceProbability = norm.cdf(self._d2_)
        if callPrice:
            self.callPrice = round(float(callPrice), 6)
            self.impliedVolatility = impliedVolatility(\
                    self.__class__.__name__, args, self.callPrice)
        if putPrice and not callPrice:
            self.putPrice = round(float(putPrice), 6)
            self.impliedVolatility = impliedVolatility(\
                    self.__class__.__name__, args, putPrice=self.putPrice)
        if callPrice and putPrice:
            self.callPrice = float(callPrice)
            self.putPrice = float(putPrice)
            self.putCallParity = self._parity()

    def _price(self):
        '''Returns the option price: [Call price, Put price]'''
        if self.volatility == 0 or self.daysToExpiration == 0:
            call = max(0.0, self.underlyingPrice - self.strikePrice)
            put = max(0.0, self.strikePrice - self.underlyingPrice)
        if self.strikePrice == 0:
            raise ZeroDivisionError('The strike price cannot be zero')
        else:
            call = self.underlyingPrice * e**(-self.dividendYield * \
                    self.daysToExpiration) * norm.cdf(self._d1_) - \
                    self.strikePrice * e**(-self.interestRate * \
                    self.daysToExpiration) * norm.cdf(self._d2_)
            put = self.strikePrice * e**(-self.interestRate * \
                    self.daysToExpiration) * norm.cdf(-self._d2_) - \
                    self.underlyingPrice * e**(-self.dividendYield * \
                    self.daysToExpiration) * norm.cdf(-self._d1_)
        return [call, put]

def impliedVolatility(className, args, callPrice=None, putPrice=None, high=500.0, low=0.0):
    '''Returns the estimated implied volatility'''
    if callPrice:
        target = callPrice
    if putPrice:
        target = putPrice
    decimals = len(str(target).split('.')[1])		# Count decimals
    for i in range(10000):	# To avoid infinite loops
        mid = (high + low) / 2
        if mid < 0.00001:
            mid = 0.00001
        if callPrice:
            estimate = eval(className)(args, volatility=mid, performance=True).callPrice
        if putPrice:
            estimate = eval(className)(args, volatility=mid, performance=True).putPrice
        if round(estimate, decimals) == target:
            break
        elif estimate > target:
            high = mid
        elif estimate < target:
            low = mid
    return mid