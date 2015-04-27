__author__ = 'HarperMain'

import wx
import wx.lib.agw.aui as aui
from wx.lib.pubsub import pub as Publisher
from title_icons import *
from pnlWelcome import PanelWelcome
from pnlEuropean import PanelEuropean
from pnlButtons import PanelButtons
from pnlVanilla import PanelVanilla
from pnlAsian import PanelAsian
from pnlLookback import PanelLookback

class AppMain(wx.Frame):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,550 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )



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
                           Bottom().
                           Layer(1).
                           Name("Welcome").
                           Maximize().
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).Show(show=True).
                           BestSize(wx.Size(500, 200))
                           )

        # self.Bind(wx.EVT_BUTTON, self.OnEuropeanButtonClick)

        self.m_mgr.Update()
        self.Centre(wx.BOTH)

    def __init__Panels(self):
        # self.pnlDocking = wx.Panel(id=wx.ID_ANY, name='pnlDocking', parent=self, size=wx.Size(500, 400),
        #                            style=wx.TAB_TRAVERSAL)
        self.PanelButton = PanelButtons(self)
        self.PanelWelcome = PanelWelcome(self)
        # self.PanelWelcome.Hide()
        self.PanelEuropean = PanelEuropean(self)
        self.PanelEuropean.Hide()
        self.PanelVanilla = PanelVanilla(self)
        self.PanelVanilla.Hide()
        self.PanelAsian = PanelAsian(self)
        self.PanelAsian.Hide()
        self.PanelLookback = PanelLookback(self)
        self.PanelLookback.Hide()

    def __init__subscribers(self):
        Publisher.subscribe(self.OnEuropeanButtonClick, 'euro')
        Publisher.subscribe(self.OnAsianButtonClick, 'asian')
        Publisher.subscribe(self.OnVanillaButtonClick, 'vanilla')
        Publisher.subscribe(self.OnLookbackButtonClick, 'lookback')

    def _init_sizers(self):
        self.s = wx.BoxSizer(wx.VERTICAL)
        self.s.AddWindow(self.pnlDocking, 85, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.s)

    def _init__bindings(self):
        # self.EuropeanButton.Bind(wx.EVT_BUTTON, self.OnEuropeanButtonClick)
        pass

    def __del__( self ):
        pass

    def HidePanes(self):
        Pane1 = self.m_mgr.GetPane(self.PanelWelcome)
        Pane2 = self.m_mgr.GetPane(self.PanelVanilla)
        Pane3 = self.m_mgr.GetPane(self.PanelEuropean)
        Pane4 = self.m_mgr.GetPane(self.PanelAsian)
        Pane5 = self.m_mgr.GetPane(self.PanelLookback)
        Pane1.Hide()
        Pane2.Hide()
        Pane3.Hide()
        Pane4.Hide()
        Pane5.Hide()

    def ShowWelcomePanel(self):
        self.HidePanes()
        WelcomePane = self.m_mgr.GetPane(self.PanelWelcome)
        WelcomePane.Show(show=True)
        self.m_mgr.Update()

    def OnEuropeanButtonClick(self, event):
        self.HidePanes()
        EuropeanPane = self.m_mgr.GetPane(self.PanelEuropean)
        EuropeanPane.Show(show=True)
        EuropeanPane.Maximize()
        self.m_mgr.Update()

    def OnVanillaButtonClick(self, event):
        self.HidePanes()
        VanillaPane = self.m_mgr.GetPane(self.PanelVanilla)
        VanillaPane.Show(show=True).Maximize()
        self.m_mgr.Update()

    def OnAsianButtonClick(self, event):
        self.HidePanes()
        AsiaPane = self.m_mgr.GetPane(self.PanelAsian)
        AsiaPane.Show(show=True).Maximize()
        self.m_mgr.Update()

    def OnLookbackButtonClick(self, event):
        self.HidePanes()
        LookbackPane = self.m_mgr.GetPane(self.PanelLookback)
        LookbackPane.Show(show=True).Maximize()
        self.m_mgr.Update()

    def OnAmericanButtonClick(self, event):
        pass

def CreateBitmap(xpm):

    bmp = eval(xpm).Bitmap

    return bmp

if __name__ == '__main__':
    app = wx.App()
    AppMain(None)
    app.MainLoop()