class Point:
    def __init__(self, hoek = 0, hoogte = 0):
        self.Hoek = hoek
        self.Hoogte = hoogte

    def setPoints(self):
        

    @property
    def Hoek(self):
        return self.__Hoek
    
    @Hoek.setter
    def Hoek(self, val):
        self.__Hoek = val
    
    @property
    def Hoogte(self):
        return self.__Hoogte

    @Hoogte.setter
    def Hoogte(self, val)
        self.__Hoogte = val