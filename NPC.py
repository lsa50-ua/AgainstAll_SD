import random
from Posicion import *



#Clase que define a los NPCs de la partida
class NPC:
    def __init__ (self):
        self.posicion = Posicion(random.randint(0,19),random.randint(0,19))
        self.nivel = random.randint(1, 9)
        self.muerto = False
        self.token = ""
    
    def obtenerNivel(self):
        return self.nivel
        
    def obtenerNivel_Char(self):
        if self.nivel == 1:
            return '1'
        if self.nivel == 2:
            return '2'
        if self.nivel == 3:
            return '3'
        if self.nivel == 4:
            return '4'
        if self.nivel == 5:
            return '5'
        if self.nivel == 6:
            return '6'
        if self.nivel == 7:
            return '7'
        if self.nivel == 8:
            return '8'
        if self.nivel == 9:
            return '9'
        
    def matar(self):
        self.muerto = True
    
    def vivoOmuerto(self):
        return self.muerto

    def obtenerTOKEN(self):
        return self.token

    def asignarTOKEN(self,token):
        self.token = token

    def obtenerPosicion(self):
        return self.posicion

    def asignarPosicion(self,posicion):
        self.posicion.setX(posicion.getX())
        self.posicion.setY(posicion.getY())
    
    def asignarPosicionX(self,x):
        self.posicion.setX(x)

    def añadirPosicionX(self,x):
        self.posicion.addX(x)

    def asignarPosicionY(self,y):
        self.posicion.setY(y)

    def añadirPosicionY(self,y):
        self.posicion.addY(y)
