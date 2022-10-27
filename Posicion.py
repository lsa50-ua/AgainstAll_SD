class Posicion:
    def __init__ (self,x,y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def addX(self,x):
        self.x += x

    def addY(self,y):
        self.y += y