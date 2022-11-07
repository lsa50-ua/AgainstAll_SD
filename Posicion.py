class Posicion:
    def __init__ (self):
        self.x = 0
        self.y = 0

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def addX(self,x):
        self.x += x

    def addY(self,y):
        self.y += y

    def setX(self,x):
        self.x = x

    def setY(self,y):
        self.y = y