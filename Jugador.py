import random
import socket
import sys
from Posicion import *

HEADER = 64
#PORT = 5050
FORMAT = 'utf-8'

#Clase que define a los jugadores de la partida
class Jugador:
    def __init__ (self):
        self.posicion = Posicion(random.randint(1,20),random.randint(1,20))
        self.alias = ""
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

    def matar(self):
        self.muerto = True
    
    def vivoOmuerto(self):
        return self.muerto


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

#HAY QUE DECIR EN EL INICIO DE LA PARTIDA, QUE TIENEN QUE PONER X PARÁMETROS    

if (len(sys.argv) == 5):
    SERVER = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (SERVER, PORT)
            
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

    send(msg)

    #print("Envio al servidor: ", FIN)
    #send("FIN")
    client.close()
else:
    print ("Parece que algo falló. Necesito estos argumentos para el Jugador: <ServerIP> <Puerto> <ALIAS> <PASSWORD>")


#para pillar las teclas del jugador usamos en python, msvrct.getch()decode(FORMAT)
# startime = time.time()
# 
# while True:
#   msg = ""
#   if  msvcrt SEGUIR CON LA FOTO DE LUIS