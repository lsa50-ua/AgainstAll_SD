import socket
import random
import sys
from Posicion import *

#CAMBIAR TODA LA CLASE, LA HE COPIADO DE LA CLASE JUGADOR
#Clase que define a los NPCs de la partida
class NPC:
    def __init__ (self):
        self.posicion = Posicion(random.randint(1,20),random.randint(1,20))
        self.nivel = 1
        self.muerto = False

    #Decrementa en una cierta cantidad el nivel del jugador
    def decrementarNivel(self, cantidad):
        self.nivel -= cantidad

        #El nivel mínimo es 0
        if self.nivel < 0:
            self.nivel = 0
    
    def obtenerNivel(self):
        return self.nivel
        
    def matar(self):
        self.muerto = True
    
    def vivoOmuerto(self):
        return self.muerto

if (len(sys.argv) == 3):
    IP = sys.argv[1]
    PUERTO = int(sys.argv[2])
    ADDR = (IP,PUERTO)
            
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    #print (f"Establecida conexión en [{ADDR}]")

    ALIAS=sys.argv[3]
    PASSWORD=sys.argv[4]

    jugador = Jugador()
    jugador.asignarAlias(ALIAS)

    NIVEL=jugador.obtenerNivel()
    EC=jugador.obtenerEC()
    EF=jugador.obtenerEF()

    msg = ALIAS + ":" + PASSWORD + ":" + repr(NIVEL) + ":" + repr(EC) + ":" + repr(EF)

    #print("Envio al servidor: ", FIN)
    #send("FIN")
    client.close()
else:
    print ("Parece que algo falló. Necesito estos argumentos para el NPC: <GestorDeColas_IP> <GestorDeColas_Puerto>")