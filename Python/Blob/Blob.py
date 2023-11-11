class Blob:
    def __init__(self, x, y, paintRatio, width=1, height=1):
        self.X = x
        self.Y = y
        self.PaintRatio = paintRatio
        self.Width  = width
        self.Height = height

    def setPoints(self):
        


    @property
    def X(self):
        return self.__X

    @X.setter
    def X(self, val):
        self.__X = val

    @property
    def Y(self):
        return self.__Y

    @Y.setter
    def Y(self, val):
        self.__Y = val

    @property
    def PaintRatio(self):
        return self.__PaintRatio

    @PaintRatio.setter
    def PaintRatio(self, val):
        self.__PaintRatio = val

    @property
    def Width(self):
        return self.__Width

    @Width.setter
    def Width(self, val):
        self.__Width = val

    @property
    def Height(self):
        return self.__Height
    
    @Height.setter
    def Height(self, val):
        self.__Height = val
