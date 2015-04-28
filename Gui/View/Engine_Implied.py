__author__ = 'HarperMain'

from mibian import BS, Me

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
            self.Option = Me([spot, strike, rate, dividend, expiry], callPrice=put)

    def GetImpliedVol(self):
        return self.Option.impliedVolatility


