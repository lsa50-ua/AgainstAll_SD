import random
import socket
from ssl import _PasswordType
import sys
from telnetlib import EC
from Posicion import *

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
FIN = "FIN"

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

    def obtenerEF(self):
        return self.EF

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
    

    def main():
        if  (len(sys.argv) == 5):
            SERVER = sys.argv[1]
            PORT = int(sys.argv[2])
            ADDR = (SERVER, PORT)
            
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
            #print (f"Establecida conexión en [{ADDR}]")

            ALIAS=sys.argv[3]
            PASSWORD=sys.argv[4]
            NIVEL=self.obtenerNivel()
            EC=sys.argv[6]
            EF=sys.argv[7]

            while msg != FIN :
                #print("Envio al servidor: ", msg)
                send(msg)
                #print("Recibo del Servidor: ", client.recv(2048).decode(FORMAT))
                msg=input()

            #print ("SE ACABO LO QUE SE DABA")
            #print("Envio al servidor: ", FIN)
            send(FIN)
            client.close()
        else:
            #print ("Oops!. Parece que algo falló. Necesito estos argumentos: <ServerIP> <Puerto> <ALIAS> <PASSWORD>")


#para pillar las teclas del jugador usamos en python, msvrct.getch()decode(FORMAT)
# startime = time.time()
# 
# while True:
#   msg = ""
#   if  msvcrt SEGUIR CON LA FOTO DE LUIS