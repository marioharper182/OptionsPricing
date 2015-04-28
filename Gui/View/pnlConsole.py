__author__ = 'HarperMain'
import wx
import sys
import logging
from wx import richtext

class consoleOutput(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
        self.logger = logging.getLogger('wxApp')

        # Add a panel so it looks the correct on all platforms
        # self.log = wx.TextCtrl(self, -1, size=(100,100),
        #                   style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)


        self.log = wx.richtext.RichTextCtrl(self, -1, size=(500,150),
                                            style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.SIMPLE_BORDER|wx.CURSOR_NONE)



        self.log.Bind(wx.EVT_CONTEXT_MENU, self.onRightUp)


        # deactivate the console if we are in debug mode
        if not sys.gettrace():
            redir = RedirectText(self.log)
            sys.stdout = redir


        # Add widgets to a sizer
        sizer = wx.BoxSizer()
        sizer.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)


        self.SetSizerAndFit(sizer)

    def onRightUp(self, event):
        self.log.PopupMenu(ConsoleContextMenu(self, event))

class RedirectText(object):

    def __init__(self,TextCtrl):

        self.out=TextCtrl
        self.__line_num = 0

    def line_num(self,reset=False):
        if not reset:
            self.__line_num += 1
            return self.__line_num
        else:
            self.__line_num = 0

    def write(self,string):

        args = string.split('|')
        string = args[-1]
        args = [a.strip() for a in args[:-1]]

        if len(string.strip()) > 0:

            string += '\n'
            if 'RESET' in args:
                self.line_num(reset=True)
                return


            string = str(self.line_num())+ ':  '+string if string != '\n' else string
            self.out.SetInsertionPoint(0)
            if 'WARNING' in args:
                self.out.BeginTextColour((255, 140, 0))
            elif 'ERROR' in args:
                self.out.BeginTextColour((255, 0, 0))
            elif not 'DEBUG' in args:
                self.out.BeginTextColour((0, 0, 0))

            # self.out.Text =  self.out.Text.Insert(string+ "\n");

            self.out.WriteText(string)
            self.out.EndTextColour()

            self.out.Refresh()

    def flush(self):
        pass

class ConsoleContextMenu(wx.Menu):
    """
    Context menu for when a user does a right click in the ConsoleOutput
    """

    def __init__(self, parent, event):
        wx.Menu.__init__(self)
        self.log = parent.log
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Clear Console')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnClear, mmi)

    def OnClear(self, event):
        """
        User clears the
        """
        self.log.Clear()
        print 'RESET |'

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()