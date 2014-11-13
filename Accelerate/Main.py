__author__ = 'Mario'

import wx
import wx.xrc, wx.html
import sys

from pnlGui import MainPanel

###########################################################################
## Class MainPanel
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, pos = (100,200), size = wx.Size( 500,300 ),
                            style = wx.MAXIMIZE_BOX | wx.RESIZE_BORDER |
	                        wx.SYSTEM_MENU | wx.CAPTION |	 wx.CLOSE_BOX | wx.TAB_TRAVERSAL )

        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar()

        # mainpanel = wx.Panel(self)

        MainPanel(self)




    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()

    def __del__( self ):
        pass

if __name__ == '__main__':
    app = wx.App()   # Error messages go to popup window
    top = MainFrame(None)
    top.Show()
    app.MainLoop()
    # # Run the application
    # app = wx.App(False)
    # dlg = MainFrame(None)
    # # dlg.ShowModal()
    # # dlg.Destroy()


aboutText = """<p>Sorry, there is no information about this program. It is
running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.
See <a href="http://wiki.wxpython.org">wxPython Wiki</a></p>"""

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())

class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About <<project>>",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400,200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()