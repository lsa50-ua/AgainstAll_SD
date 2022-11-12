import socket
import random
import sys
from Posicion import *
from kafka import KafkaProducer
import msvcrt
import time


#Clase que define a los NPCs de la partida
class NPC:
    def __init__ (self):
        self.posicion = Posicion(random.randint(1,20),random.randint(1,20))
        self.nivel = random.randint(1, 10)
        self.muerto = False
        self.token
        

    #Decrementa en una cierta cantidad el nivel del jugador
    
    def obtenerNivel(self):
        return self.nivel
        
    def matar(self):
        self.muerto = True
    
    def vivoOmuerto(self):
        return self.muerto
