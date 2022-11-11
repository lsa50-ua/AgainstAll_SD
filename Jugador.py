import random
from Posicion import *

class Jugador:
    def __init__ (self):
        self.posicion = Posicion(random.randint(0,19),random.randint(0,19))
        self.alias = ""
        self.nivel = ""
        self.EF = ""
        self.EC = ""
        self.token = ""
        self.contraseña = ""

    # Decrementa en una cierta cantidad el nivel del jugador
    def decrementarNivel(self, cantidad):
        self.nivel -= cantidad

        # El nivel mínimo es 0
        if self.nivel < 0:
            self.nivel = 0

    def aumentarNivel(self, cantidad):
        self.nivel += cantidad

    def asignarAlias(self,alias):
        self.alias = alias
    
    def obtenerNivel(self):
        return self.nivel
    
    def obtenerEC(self):
        return self.EC

    def asignarEC(self,EC):
        self.EC = EC

    def obtenerEF(self):
        return self.EF
    
    def asignarEF(self,EF):
        self.EF = EF

    def asignarNivel(self,nivel):
        self.nivel = nivel

    def obtenerTOKEN(self):
        return self.token

    def asignarTOKEN(self,token):
        self.token = token
    
    def asignarContraseña(self,contraseña):
        self.contraseña = contraseña
    
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
