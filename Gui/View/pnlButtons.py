__author__ = 'HarperMain'
import wx
from wx.lib.pubsub import pub as Publisher
from title_icons import *
ID_VANILLA = wx.NewId()
ID_European = wx.NewId()
ID_Asian = wx.NewId()
ID_Lookback = wx.NewId()
ID_American = wx.NewId()
def CreateBitmap(xpm):

    bmp = eval(xpm).Bitmap

    return bmp
class PanelButtons ( wx.Panel ):
    ID_VANILLA = wx.NewId()
    ID_European = wx.NewId()
    ID_Asian = wx.NewId()
    ID_Lookback = wx.NewId()
    ID_American = wx.NewId()

    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,100 ), style = wx.TAB_TRAVERSAL )

        # self.ButtonsPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size(500,100), wx.DOUBLE_BORDER|wx.TAB_TRAVERSAL )
        ButtonSizer = wx.BoxSizer( wx.HORIZONTAL )

        self.VanillaButton = wx.BitmapButton( self, ID_VANILLA, CreateBitmap("VanillaOption"), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        ButtonSizer.Add( self.VanillaButton, 0, wx.ALL, 5 )

        self.EuropeanButton = wx.BitmapButton( self, ID_European, CreateBitmap("EuropeanOption"), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        ButtonSizer.Add( self.EuropeanButton, 0, wx.ALL, 5 )

        self.AsianButton = wx.BitmapButton( self, ID_Asian, CreateBitmap("AsianOption"), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        ButtonSizer.Add( self.AsianButton, 0, wx.ALL, 5 )

        self.LookbackButton = wx.BitmapButton( self, ID_Lookback, CreateBitmap("LookBackOption"), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        ButtonSizer.Add( self.LookbackButton, 0, wx.ALL, 5 )

        self.SetSizer( ButtonSizer )
        self.Layout()
        ButtonSizer.Fit( self )

        self.SetSizerAndFit(ButtonSizer)
        self._init__bindings()

    def _init__bindings(self):
        self.EuropeanButton.Bind(wx.EVT_BUTTON, self.OnEuropeanButtonClick)
        self.VanillaButton.Bind(wx.EVT_BUTTON, self.OnVanillaClick)
        self.AsianButton.Bind(wx.EVT_BUTTON, self.OnAsianClick)
        self.LookbackButton.Bind(wx.EVT_BUTTON, self.OnLookbackClick)

    def __del__( self ):
        pass

    def OnEuropeanButtonClick(self, event):
        Publisher.sendMessage('euro', event=event)

    def OnVanillaClick(self, event):
        Publisher.sendMessage('vanilla', event=event)

    def OnAsianClick(self, event):
        Publisher.sendMessage('asian', event=event)

    def OnLookbackClick(self, event):
        Publisher.sendMessage('lookback', event=event)