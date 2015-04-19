__author__ = 'HarperMain'

class ColourClientData(object):

    def __init__(self, name, colour):

        self._name = name
        self._colour = colour


    def GetName(self):

        return self._name


    def GetColour(self):

        return self._colour