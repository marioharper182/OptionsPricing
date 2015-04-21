__author__ = 'HarperMain'

import wx
from title_icons import *


class AppMain(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, log=None):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self._init__toolbar()
        self.Show()

    def _init__toolbar(self):
        # self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        vbox = wx.BoxSizer(wx.VERTICAL)
        toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER)
        toolbar.AddTool(wx.ID_ANY, CreateBitmap("EuropeanOption"))
        # toolbar.AddTool()
        toolbar.AddSimpleTool(1, EuropeanOption.GetBitmap(), 'Simple European', '')
        toolbar.AddSimpleTool(0, wx.Image('AmericanOption.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Simple European', '')

def CreateBitmap(xpm):

    bmp = eval(xpm).Bitmap

    return bmp

if __name__ == '__main__':
    app = wx.App()
    AppMain(None, title='Application', size=(500,500))
    app.MainLoop()