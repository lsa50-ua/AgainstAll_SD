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

    #Decrementa en una cierta cantidad el nivel del jugador
    
    def obtenerNivel(self):
        return self.nivel
        
    def matar(self):
        self.muerto = True
    
    def vivoOmuerto(self):
        return self.muerto

if (len(sys.argv) == 2):
    bootstrap_servers = [sys.argv[1]]
    try:
        producer = KafkaProducer(bootstrap_servers = bootstrap_servers)
    except:
        print("ERROR en el parametro pasado. Saliendo...")
        sys.exit()
    identificador = str(random.randint(1,10)*random.randint(1,10)*random.randint(1,10))
    msg = "NPC" + ":" + identificador
    producer.send('Players', msg.encode('utf-8'))

    start = time.time()
    timeout = 120
    while 1:
        if time.time() - start > timeout:
            number = random.randint(1, 8)
            if(number == 1):
                producer.send('Players', b'a')
            
            if(number == 2):
                producer.send('Players', b'w')
            
            if(number == 3):
                producer.send('Players', b's')
            
            if(number == 4):
                producer.send('Players', b'd')
            
            if(number == 5):
                producer.send('Players', b'q')
            
            if(number == 6):
                producer.send('Players', b'e')
            
            if(number == 7):
                producer.send('Players', b'z')
            
            if(number == 8):
                producer.send('Players', b'c')
            
            
            #metadata = ack.get()

            time.sleep(1)
        else:
            break
    
else:
    print ("Parece que algo falló. Necesito este argumento para el NPC: <Bootstrap-server del gestor de colas>")