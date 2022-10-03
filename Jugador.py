import random
from Posicion import *

#Clase que define a los jugadores de la partida
class Jugador:
    def __init__ (self,alias):
        self.posicion = Posicion(random.randint(1,20),random.randint(1,20))
        self.alias = alias  #pasado como parametro?
        self.nivel = 1
        self.EF = random.randint(-10,10)
        self.EC = random.randint(-10,10)
        self.muerto = False

    #Decrementa en una cierta cantidad el nivel del jugador
    def decrementarNivel(self, cantidad):
        self.nivel -= cantidad

        #El nivel mínimo es 0
        if self.nivel < 0:
            self.nivel = 0
    
    def matar(self):
        self.muerto = True
    
    def vivoOmuerto(self):
        return self.muerto


#para pillar las teclas del jugador usamos en python, msvrct.getch()decode(FORMAT)
# startime = time.time()
# 
# while True:
#   msg = ""
#   if  msvcrt SEGUIR CON LA FOTO DE LUIS