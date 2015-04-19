__author__ = 'HarperMain'

import wx
from wx.lib.agw import ribbon as RB
from wx.lib.embeddedimage import PyEmbeddedImage
from Bitmaps import *
from title_icons import *
from pnlEuropean import PanelEuropean

ID_CIRCLE = wx.ID_HIGHEST + 1
ID_CROSS = ID_CIRCLE + 1
ID_TRIANGLE = ID_CIRCLE + 2
ID_SQUARE = ID_CIRCLE + 3
ID_POLYGON = ID_CIRCLE + 4
ID_SELECTION_EXPAND_H = ID_CIRCLE + 5
ID_SELECTION_EXPAND_V = ID_CIRCLE + 6
ID_SELECTION_CONTRACT = ID_CIRCLE + 7
ID_PRIMARY_COLOUR = ID_CIRCLE + 8
ID_SECONDARY_COLOUR = ID_CIRCLE + 9
ID_DEFAULT_PROVIDER = ID_CIRCLE + 10
ID_AUI_PROVIDER = ID_CIRCLE + 11
ID_MSW_PROVIDER = ID_CIRCLE + 12
ID_MAIN_TOOLBAR = ID_CIRCLE + 13
ID_POSITION_TOP = ID_CIRCLE + 14
ID_POSITION_TOP_ICONS = ID_CIRCLE + 15
ID_POSITION_TOP_BOTH = ID_CIRCLE + 16
ID_POSITION_LEFT = ID_CIRCLE + 17
ID_POSITION_LEFT_LABELS = ID_CIRCLE + 18
ID_POSITION_LEFT_BOTH = ID_CIRCLE + 19
ID_TOGGLE_PANELS = ID_CIRCLE + 20

def CreateBitmap(xpm):

    bmp = eval(xpm).Bitmap

    return bmp

class ColourClientData(object):

    def __init__(self, name, colour):

        self._name = name
        self._colour = colour


    def GetName(self):

        return self._name


    def GetColour(self):

        return self._colour

class AppMain(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, log=None):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.bSizer = wx.BoxSizer( wx.VERTICAL )
        self.panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(500, 100), wx.TAB_TRAVERSAL)
        self.bSizer.Add( self.panel, 1, wx.EXPAND |wx.ALL, 5 )

        self._ribbon = RB.RibbonBar(self.panel, wx.ID_ANY, agwStyle=RB.RIBBON_BAR_DEFAULT_STYLE|RB.RIBBON_BAR_SHOW_PANEL_EXT_BUTTONS)
        # self.panelchanging = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        # self.bSizer.Add( self._ribbon, 0, wx.ALL, 5)
        # self.bSizer.Add( self.panelchanging, 1, wx.EXPAND |wx.ALL, 5 )


        self._bitmap_creation_dc = wx.MemoryDC()
        self._colour_data = wx.ColourData()
        self.UI_Ribbon1()
        self.UI_Ribbon2()
        self.UI_Ribbon3()
        self.UI_Ribbon4()
        self._ribbon.Realize()

        self.UI_Panel()


        # self.BindEvents([selection, shapes, provider_bar, toolbar_panel])

        # self.SetIcon(images.Mondrian.Icon)
        self._init__Bindings()
        self.CenterOnScreen()
        self.Show()

    def UI_Ribbon1(self):

        home = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Options Pricing", CreateBitmap("ribbon"))
        # toolbar_panel = RB.RibbonPanel(home, wx.ID_ANY, "Options Choices", wx.NullBitmap, wx.DefaultPosition,
        #                                wx.DefaultSize, agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE|RB.RIBBON_PANEL_EXT_BUTTON)

        # toolbar = RB.RibbonToolBar(toolbar_panel, ID_MAIN_TOOLBAR)
        # toolbar.AddTool(wx.ID_ANY, CreateBitmap("align_left"))
        shapes_panel = RB.RibbonPanel(home, wx.ID_ANY, "Options Pricing", CreateBitmap("circle_small"))
        self.shapes = shapes = RB.RibbonButtonBar(shapes_panel)
        self.simpleeurope = shapes.AddSimpleButton(ID_CROSS, "Simple European", CreateBitmap("VanillaOption"), "")
        self.blackscholes = shapes.AddSimpleButton(ID_TRIANGLE, "Black-Scholes European", CreateBitmap("EuropeanOption"), "")
        self.asianoption = shapes.AddDropdownButton(ID_SQUARE, "Asian Option", CreateBitmap("AsianOption"), "")
        self.eurolookback = shapes.AddDropdownButton(ID_POLYGON, "European LookBack", CreateBitmap("LookBackOption"), "")

    def UI_Ribbon2(self):
        statsRibbon = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Distributions", CreateBitmap("empty"))

    def UI_Ribbon3(self):
        scheme = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Appearance", CreateBitmap("eye"))
        self._default_primary, self._default_secondary, self._default_tertiary = self._ribbon.GetArtProvider().GetColourScheme(1, 1, 1)

        provider_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Art", wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize,
                                        agwStyle=RB.RIBBON_PANEL_NO_AUTO_MINIMISE)
        provider_bar = RB.RibbonButtonBar(provider_panel, wx.ID_ANY)
        provider_bar.AddSimpleButton(ID_DEFAULT_PROVIDER, "Default Provider",
                                     wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(32, 32)), "")
        provider_bar.AddSimpleButton(ID_AUI_PROVIDER, "AUI Provider", CreateBitmap("aui_style"), "")
        provider_bar.AddSimpleButton(ID_MSW_PROVIDER, "MSW Provider", CreateBitmap("msw_style"), "")

        primary_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Primary Colour", CreateBitmap("colours"))
        self._primary_gallery = self.PopulateColoursPanel(primary_panel, self._default_primary, ID_PRIMARY_COLOUR)

        secondary_panel = RB.RibbonPanel(scheme, wx.ID_ANY, "Secondary Colour", CreateBitmap("colours"))
        self._secondary_gallery = self.PopulateColoursPanel(secondary_panel, self._default_secondary, ID_SECONDARY_COLOUR)

    def UI_Ribbon4(self):
        dummy_3 = RB.RibbonPage(self._ribbon, wx.ID_ANY, "Data Input", CreateBitmap("empty"))

    def UI_Panel(self):
        self._ribbon.Realize()

        # self._logwindow = wx.TextCtrl(self.panel, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
        #                               wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_LEFT | wx.TE_BESTWRAP | wx.BORDER_NONE)
        #
        # self._togglePanels = wx.ToggleButton(self.panel, ID_TOGGLE_PANELS, "&Toggle panels")
        # self._togglePanels.SetValue(True)

        s = wx.BoxSizer(wx.VERTICAL)

        s.Add(self._ribbon, 0, wx.EXPAND)
        # s.Add(self._logwindow, 1, wx.EXPAND)
        # s.Add(self._togglePanels, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 10)

        self.panel.SetSizer(s)

    def _init__Bindings(self):
        # self.shapes.Bind(RB.EVT_RIBBONPANEL_EXTBUTTON_ACTIVATED, self.ShowPanelEuropean, id=ID_CROSS)
        self.shapes.Bind(RB.EVT_RIBBONBUTTONBAR_CLICKED, self.ShowPanelEuropean, id=ID_CROSS)
        # self.shapes.Bind(RB.EVT_RIBBONTOOLBAR_CLICKED, self.ShowPanelEuropean, id=ID_CROSS)
        self.shapes.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.onEuroLookbackClicked, id=ID_SQUARE)
        self.shapes.Bind(RB.EVT_RIBBONBUTTONBAR_DROPDOWN_CLICKED, self.onEuroLookbackClicked, id=ID_POLYGON)

    def ShowPanelEuropean(self, event):
        self.panelchanging = PanelEuropean(self)

    def onEuroLookbackClicked(self, event):
        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "Naive Monte Carlo")
        menu.Append(wx.ID_ANY, "With Control-Variates and Stochastic Volatility")

        event.PopupMenu(menu)

    def PopulateColoursPanel(self, panel, defc, gallery_id):

        gallery = wx.FindWindowById(gallery_id, panel)

        if gallery:
            gallery.Clear()
        else:
            gallery = RB.RibbonGallery(panel, gallery_id)

        dc = self._bitmap_creation_dc
        def_item = self.AddColourToGallery(gallery, "Default", dc, defc)
        gallery.SetSelection(def_item)

        self.AddColourToGallery(gallery, "BLUE", dc)
        self.AddColourToGallery(gallery, "BLUE VIOLET", dc)
        self.AddColourToGallery(gallery, "BROWN", dc)
        self.AddColourToGallery(gallery, "CADET BLUE", dc)
        self.AddColourToGallery(gallery, "CORAL", dc)
        self.AddColourToGallery(gallery, "CYAN", dc)
        self.AddColourToGallery(gallery, "DARK GREEN", dc)
        self.AddColourToGallery(gallery, "DARK ORCHID", dc)
        self.AddColourToGallery(gallery, "FIREBRICK", dc)
        self.AddColourToGallery(gallery, "GOLD", dc)
        self.AddColourToGallery(gallery, "GOLDENROD", dc)
        self.AddColourToGallery(gallery, "GREEN", dc)
        self.AddColourToGallery(gallery, "INDIAN RED", dc)
        self.AddColourToGallery(gallery, "KHAKI", dc)
        self.AddColourToGallery(gallery, "LIGHT BLUE", dc)
        self.AddColourToGallery(gallery, "LIME GREEN", dc)
        self.AddColourToGallery(gallery, "MAGENTA", dc)
        self.AddColourToGallery(gallery, "MAROON", dc)
        self.AddColourToGallery(gallery, "NAVY", dc)
        self.AddColourToGallery(gallery, "ORANGE", dc)
        self.AddColourToGallery(gallery, "ORCHID", dc)
        self.AddColourToGallery(gallery, "PINK", dc)
        self.AddColourToGallery(gallery, "PLUM", dc)
        self.AddColourToGallery(gallery, "PURPLE", dc)
        self.AddColourToGallery(gallery, "RED", dc)
        self.AddColourToGallery(gallery, "SALMON", dc)
        self.AddColourToGallery(gallery, "SEA GREEN", dc)
        self.AddColourToGallery(gallery, "SIENNA", dc)
        self.AddColourToGallery(gallery, "SKY BLUE", dc)
        self.AddColourToGallery(gallery, "TAN", dc)
        self.AddColourToGallery(gallery, "THISTLE", dc)
        self.AddColourToGallery(gallery, "TURQUOISE", dc)
        self.AddColourToGallery(gallery, "VIOLET", dc)
        self.AddColourToGallery(gallery, "VIOLET RED", dc)
        self.AddColourToGallery(gallery, "WHEAT", dc)
        self.AddColourToGallery(gallery, "WHITE", dc)
        self.AddColourToGallery(gallery, "YELLOW", dc)

        return gallery


    def AddColourToGallery(self, gallery, colour, dc, value=None):

        item = None

        if colour != "Default":
            c = wx.NamedColour(colour)

        if value is not None:
            c = value

        if c.IsOk():

            iWidth = 64
            iHeight = 40

            bitmap = wx.EmptyBitmap(iWidth, iHeight)
            dc.SelectObject(bitmap)
            b = wx.Brush(c)
            dc.SetPen(wx.BLACK_PEN)
            dc.SetBrush(b)
            dc.DrawRectangle(0, 0, iWidth, iHeight)

            colour = colour[0] + colour[1:].lower()
            size = wx.Size(*dc.GetTextExtent(colour))
            notcred = min(abs(~c.Red()), 255)
            notcgreen = min(abs(~c.Green()), 255)
            notcblue = min(abs(~c.Blue()), 255)

            foreground = wx.Colour(notcred, notcgreen, notcblue)

            if abs(foreground.Red() - c.Red()) + abs(foreground.Blue() - c.Blue()) + abs(foreground.Green() - c.Green()) < 64:
                # Foreground too similar to background - use a different
                # strategy to find a contrasting colour
                foreground = wx.Colour((c.Red() + 64) % 256, 255 - c.Green(),
                                       (c.Blue() + 192) % 256)

            dc.SetTextForeground(foreground)
            dc.DrawText(colour, (iWidth - size.GetWidth() + 1) / 2, (iHeight - size.GetHeight()) / 2)
            dc.SelectObjectAsSource(wx.NullBitmap)

            item = gallery.Append(bitmap, wx.ID_ANY)
            gallery.SetItemClientData(item, ColourClientData(colour, c))

        return item

if __name__ == '__main__':
    app = wx.App()
    AppMain(None, title='Application', size=(500,500))
    app.MainLoop()