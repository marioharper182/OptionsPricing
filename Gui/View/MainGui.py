__author__ = 'HarperMain'

import wx
import wx.lib.agw.aui as aui
from wx.lib.pubsub import pub as Publisher

from pnlWelcome import PanelWelcome
from pnlEuropean import PanelEuropean
from pnlButtons import PanelButtons
from pnlVanilla import PanelVanilla
from pnlAsian import PanelAsian
from pnlLookback import PanelLookback
from pnlConsole import consoleOutput
from pnlAmerican import PanelAmerican
from pnlImplied import PanelImplied


class AppMain(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 650), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # self._init_sizers()
        self.__init__Panels()
        self._init__AUI()
        self.__init__subscribers()
        self._init__bindings()

        self.ShowWelcomePanel()

        self.m_mgr.Update()
        self.Show()

    def _init__AUI(self):
        self.m_mgr = aui.AuiManager()
        self.m_mgr.SetManagedWindow(self)

        self.m_mgr.AddPane(self.PanelButton,
                           aui.AuiPaneInfo().
                           Top().
                           Layer(1).
                           Name("ButtonBar").
                           CloseButton(False).
                           MaximizeButton(True).
                           MinimizeButton(True).
                           PinButton(False).
                           Resizable().
                           # Movable().
                           Floatable(False)
                           )

        self.m_mgr.AddPane(self.PanelEuropean,
                           aui.AuiPaneInfo().
                           Bottom().
                           Name("European").
                           Caption("European Option (Monte Carlo)").
                           CloseButton(False).
                           Maximize().
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).Show(show=False).Hide().
                           BestSize(wx.Size(500, 400))
                           )

        self.m_mgr.AddPane(self.PanelAsian,
                           aui.AuiPaneInfo().
                           Bottom().
                           Name("Asian").
                           Caption("Asian Option").
                           CloseButton(False).
                           Maximize().
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).Show(show=False).Hide().
                           BestSize(wx.Size(500, 400))
                           )

        self.m_mgr.AddPane(self.PanelLookback,
                           aui.AuiPaneInfo().
                           Bottom().
                           Name("Lookback").
                           Caption("European Lookback Option").
                           CloseButton(False).
                           Maximize().
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).Show(show=False).Hide().
                           BestSize(wx.Size(500, 400))
                           )

        self.m_mgr.AddPane(self.PanelVanilla,
                           aui.AuiPaneInfo().
                           Bottom().
                           Name("Vanilla").
                           Caption("BlackScholes European").
                           CloseButton(False).
                           Maximize().
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).Show(show=False).Hide().
                           BestSize(wx.Size(500, 400))
                           )

        self.m_mgr.AddPane(self.PanelAmerican,
                           aui.AuiPaneInfo().
                           Bottom().
                           Name("American").
                           Caption("American Option").
                           CloseButton(False).
                           Maximize().
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).Show(show=False).Hide().
                           BestSize(wx.Size(500, 400))
                           )

        self.m_mgr.AddPane(self.PanelImplied,
                           aui.AuiPaneInfo().
                           Bottom().
                           Name("Implied").
                           Caption("BlackScholes Implied Volatility").
                           CloseButton(False).
                           Maximize().
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).Show(show=False).Hide().
                           BestSize(wx.Size(500, 400))
                           )

        self.m_mgr.AddPane(self.PanelWelcome,
                           aui.AuiPaneInfo().
                           Layer(1).
                           Name("Welcome").
                           Caption("Please Make A Selection").
                           Maximize().
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).Show(show=True).
                           BestSize(wx.Size(500, 200))
                           )

        self.m_mgr.AddPane(self.PanelConsole,
                           aui.AuiPaneInfo().
                           Bottom().
                           Name("Console").
                           Caption("Console Output").
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).Show(show=True).
                           Fixed()
                           )

        self.m_mgr.Update()
        self.Centre(wx.BOTH)

    def __init__Panels(self):
        # self.pnlDocking = wx.Panel(id=wx.ID_ANY, name='pnlDocking', parent=self, size=wx.Size(500, 400),
        # style=wx.TAB_TRAVERSAL)
        self.PanelButton = PanelButtons(self)
        self.PanelWelcome = PanelWelcome(self)
        self.PanelConsole = consoleOutput(self)

        self.PanelEuropean = PanelEuropean(self)
        self.PanelEuropean.Hide()
        self.PanelVanilla = PanelVanilla(self)
        self.PanelVanilla.Hide()
        self.PanelAsian = PanelAsian(self)
        self.PanelAsian.Hide()
        self.PanelLookback = PanelLookback(self)
        self.PanelLookback.Hide()
        self.PanelAmerican = PanelAmerican(self)
        self.PanelAmerican.Hide()
        self.PanelImplied = PanelImplied(self)
        self.PanelImplied.Hide()

    def __init__subscribers(self):
        Publisher.subscribe(self.OnEuropeanButtonClick, 'euro')
        Publisher.subscribe(self.OnAsianButtonClick, 'asian')
        Publisher.subscribe(self.OnVanillaButtonClick, 'vanilla')
        Publisher.subscribe(self.OnLookbackButtonClick, 'lookback')
        Publisher.subscribe(self.OnAmericanButtonClick, 'american')
        Publisher.subscribe(self.OnImpliedButtonClick, 'implied')

    def _init_sizers(self):
        self.s = wx.BoxSizer(wx.VERTICAL)
        self.s.AddWindow(self.pnlDocking, 85, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.s)

    def _init__bindings(self):
        # self.EuropeanButton.Bind(wx.EVT_BUTTON, self.OnEuropeanButtonClick)
        pass

    def __del__(self):
        pass

    def HidePanes(self):
        Pane1 = self.m_mgr.GetPane(self.PanelWelcome)
        Pane2 = self.m_mgr.GetPane(self.PanelVanilla)
        Pane3 = self.m_mgr.GetPane(self.PanelEuropean)
        Pane4 = self.m_mgr.GetPane(self.PanelAsian)
        Pane5 = self.m_mgr.GetPane(self.PanelLookback)
        Pane6 = self.m_mgr.GetPane(self.PanelAmerican)
        Pane7 = self.m_mgr.GetPane(self.PanelImplied)
        Pane1.Hide()
        Pane2.Hide()
        Pane3.Hide()
        Pane4.Hide()
        Pane5.Hide()
        Pane6.Hide()
        Pane7.Hide()

    def ShowWelcomePanel(self):
        # print('Welcome to the basic derivatives pricing application')
        # print('Please make a selection above')
        self.HidePanes()
        WelcomePane = self.m_mgr.GetPane(self.PanelWelcome)
        WelcomePane.Show(show=True)
        self.m_mgr.Update()

    def OnEuropeanButtonClick(self, event):
        print('Switched to European Monte Carlo Pricing')
        self.HidePanes()
        EuropeanPane = self.m_mgr.GetPane(self.PanelEuropean)
        EuropeanPane.Show(show=True)
        EuropeanPane.Maximize()
        self.m_mgr.Update()

    def OnVanillaButtonClick(self, event):
        print('Switched to Vanilla Black-Scholes European')
        self.HidePanes()
        VanillaPane = self.m_mgr.GetPane(self.PanelVanilla)
        VanillaPane.Show(show=True).Maximize()
        self.m_mgr.Update()

    def OnAsianButtonClick(self, event):
        print('Switched to Asian Option Pricing')
        self.HidePanes()
        AsiaPane = self.m_mgr.GetPane(self.PanelAsian)
        AsiaPane.Show(show=True).Maximize()
        self.m_mgr.Update()

    def OnLookbackButtonClick(self, event):
        print('Switched to European Lookback Option Pricing')
        print('For your convenience, we have taken the liberty of assigning '
              'the parameters (alpha, chi, average Volatility of Volatility, '
              'and preset the number of fixings to be 100 until expiry. '
              'To change these, please toggle the "Advanced Settings" option.')
        self.HidePanes()
        LookbackPane = self.m_mgr.GetPane(self.PanelLookback)
        LookbackPane.Show(show=True).Maximize()
        self.m_mgr.Update()

    def OnAmericanButtonClick(self, event):
        print('Switched to American Option Pricing')
        self.HidePanes()
        AmericanPane = self.m_mgr.GetPane(self.PanelAmerican)
        AmericanPane.Show(show=True).Maximize()
        self.m_mgr.Update()

    def OnImpliedButtonClick(self, event):
        print('Switched to Black-Scholes Implied Volatility')
        self.HidePanes()
        ImpliedPane = self.m_mgr.GetPane(self.PanelImplied)
        ImpliedPane.Show(show=True).Maximize()
        self.m_mgr.Update()


def CreateBitmap(xpm):
    bmp = eval(xpm).Bitmap

    return bmp


if __name__ == '__main__':
    app = wx.App()
    AppMain(None)
    app.MainLoop()