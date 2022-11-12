import random
import sys
from Posicion import *
from kafka import KafkaProducer
from kafka import KafkaConsumer
import time
import threading

FORMAT = 'utf-8'

def enviarMovsNPC(identificador):
    global partidaTerminada
    while 1:
        if(partidaTerminada == True):
            break
        else:
            number = random.randint(1, 8)
            if(number == 1):
                msg = identificador + ":a"
                producer.send('Players', msg.encode(FORMAT))
            
            if(number == 2):
                msg = identificador + ":w"
                producer.send('Players', msg.encode(FORMAT))

            
            if(number == 3):
                msg = identificador + ":s"
                producer.send('Players', msg.encode(FORMAT))

            
            if(number == 4):
                msg = identificador + ":d"
                producer.send('Players', msg.encode(FORMAT))

            
            if(number == 5):
                msg = identificador + ":q"
                producer.send('Players', msg.encode(FORMAT))

            
            if(number == 6):
                msg = identificador + ":e"
                producer.send('Players', msg.encode(FORMAT))

            
            if(number == 7):
                msg = identificador + ":z"
                producer.send('Players', msg.encode(FORMAT))

            
            if(number == 8):
                msg = identificador + ":c"
                producer.send('Players', msg.encode(FORMAT))
            
            
            #metadata = ack.get()

            time.sleep(1)

if (len(sys.argv) == 2):
    GESTOR_BOOTSTRAP_SERVER = [sys.argv[1]]
    try:
        producer = KafkaProducer(bootstrap_servers = GESTOR_BOOTSTRAP_SERVER)
        consumer = KafkaConsumer ('MAPA', bootstrap_servers = GESTOR_BOOTSTRAP_SERVER)
    except:
        print("ERROR en el parametro pasado. Saliendo...")
        sys.exit()
    
    identificador = str(random.randint(1,10)*random.randint(1,10)*random.randint(1,10))
    msg = "NPC" + ":" + identificador
    try:
        producer.send('Players', msg.encode('utf-8'))
    except:
        print("No hay niguna partida en curso. Saliendo...")
        sys.exit()
    for validacion in consumer:
        if validacion.decode(FORMAT) == (identificador + ":OK"):
            print("NPC con el identificador: " + identificador + " entrando en partida")
            break
        elif validacion == "FinDePartida":
            print("La partida ha finalizado antes de poder meterse el NPC")
            sys.exit()
        else:
            identificador = str(random.randint(1,10)*random.randint(1,10)*random.randint(1,10))
            msg = "NPC" + ":" + identificador
            producer.send('Players', msg.encode('utf-8'))
    
    global partidaTerminada
    partidaTerminada = False
    t1 = threading.Thread(target=enviarMovsNPC, args=(identificador))
    t1.start()
    for info in consumer:
        if info == (identificador + ":FIN"):
            print("El NPC ha muerto")
            partidaTerminada = True
            break
        if info == "FinDePartida":
            print("La partida ha finalizado")
            partidaTerminada = True
            break
    
    time.sleep(1) #para que finalice el hilo

else:
    print ("Parece que algo falló. Necesito este argumento para el NPC: <Bootstrap-server del gestor de colas>")