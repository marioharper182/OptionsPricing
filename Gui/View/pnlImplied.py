__author__ = 'Mario'

import wx
import wx.xrc
from Engine_Implied import ImpliedVolatility

###########################################################################
## Class MainPanel
###########################################################################

class PanelImplied ( wx.Panel ):

    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.TAB_TRAVERSAL )

        txtCtrlSizer = wx.BoxSizer( wx.VERTICAL )

        self.StockPrice = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        txtCtrlSizer.Add( self.StockPrice, 0, wx.ALL, 5 )

        self.StockPriceText = wx.StaticText(self, -1, 'Spot Price', pos = wx.Point(125, 10))

        self.OptionPrice = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        txtCtrlSizer.Add( self.OptionPrice, 0, wx.ALL, 5 )

        self.OptionStrikeText = wx.StaticText(self, -1, 'Strike Price', pos = wx.Point(125, 42))

        self.OptionYears = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        txtCtrlSizer.Add( self.OptionYears, 0, wx.ALL, 5 )

        self.OptionYearsText = wx.StaticText(self, -1, 'Years to Expiry (divide by 252 to get days)', pos = wx.Point(125, 75))

        self.Riskfree = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        txtCtrlSizer.Add( self.Riskfree, 0, wx.ALL, 5 )

        self.RiskFreeText = wx.StaticText(self, -1, 'Risk Free Rate', pos = wx.Point(125, 110))

        self.dividend = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        txtCtrlSizer.Add( self.dividend, 0, wx.ALL, 5 )

        self.DividendText = wx.StaticText(self, -1, 'Yearly Dividend (Percentage)', pos = wx.Point(125, 142))

        self.price = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        txtCtrlSizer.Add(self.price, 0, wx.ALL, 5)

        self.PriceText = wx.StaticText(self, -1, 'Observed Price of the Option', pos = wx.Point(125, 174))

        Choices = ['Call', 'Put']
        self.ChoiceBox = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, Choices, 0)
        # self.ChoiceBox.SetSelection(0)
        txtCtrlSizer.Add(self.ChoiceBox, 0, wx.ALL, 5)

        buttonSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.computeButton = wx.Button( self, wx.ID_ANY, u"Compute", wx.DefaultPosition, wx.DefaultSize, 0 )
        buttonSizer.Add( self.computeButton, 0, wx.ALL, 5 )


        self.clearButton = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
        buttonSizer.Add( self.clearButton, 0, wx.ALL, 5 )

        ## Bindings
        self.computeButton.Bind(wx.EVT_BUTTON, self.OnCompute)
        self.clearButton.Bind(wx.EVT_BUTTON, self.OnClear)

        txtCtrlSizer.Add( buttonSizer, 1, wx.EXPAND, 5 )


        self.SetSizer( txtCtrlSizer )
        self.Layout()

    def OnCompute(self, event):
        spot = self.StockPrice.GetValue()
        strike = self.OptionPrice.GetValue()
        expiry = self.OptionYears.GetValue()
        rate = self.Riskfree.GetValue()
        dividend = self.dividend.GetValue()
        price = self.price.GetValue()
        flag = 'c' if self.ChoiceBox.GetString(self.ChoiceBox.GetCurrentSelection()) == 'Call' else 'p'
        ImpliedVol = ImpliedVolatility(spot, strike, rate, dividend, expiry, flag, price)
        result = ImpliedVol.GetImpliedVol()

        print( 'The Black-Schoals implied volatility is:', result)
        # print(stockPrice, optionStrike, optionYears, Riskfree, Volatility)
        #

    def OnClear(self, event):
        self.StockPrice.Clear()
        self.OptionPrice.Clear()
        self.OptionYears.Clear()
        self.Riskfree.Clear()
        self.dividend.Clear()
        self.price.Clear()
        self.ChoiceBox.Clear()
        # pass

    def __del__( self ):
        pass