import socket
import sys
import random
import msvcrt

from Posicion import *
from Jugador import *
from Mapa import *
from kafka import KafkaProducer
from kafka import KafkaConsumer
from ensurepip import bootstrap
from os import system     # Para limpiar el terminal

HEADER = 64
FORMAT = 'utf-8'

# Función que manda los mensajes del Consumidor al Productor
def send(msg,client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def menu():
    print("¿Qué quieres hacer ahora?")
    print("Crear perfil (1)")
    print("Editar perfil (2)")     
    print("Unirse a partida (3)") 
    print("Salir (4)")
    print("")

def editar():
    print("¿Qué parámetro quieres cambiar?: ")
    print("EC (1)")     
    print("EF (2)")     
    print("Contraseña (3)")
    print("")

if (len(sys.argv) == 6):
    ENGINE_IP = sys.argv[1]
    ENGINE_PUERTO = int(sys.argv[2])
    ENGINE_ADDR = (ENGINE_IP, ENGINE_PUERTO)

    GESTOR_BOOTSTRAP_SERVER  = sys.argv[3]

    REGISTRY_IP = sys.argv[4]
    REGISTRY_PUERTO = int(sys.argv[5])
    REGISTRY_ADDR = (REGISTRY_IP, REGISTRY_PUERTO)
    
    bucle = True

    print("")

    try:    
        while bucle:
            menu()
            seleccion = int(input("Elección: "))
            print("")

            if seleccion == 1:
                clientRegistryCrear = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientRegistryCrear.connect(REGISTRY_ADDR)

                alias = input("Por favor introduzca un alias de hasta 20 carácteres: ")   
                aliasLimpio = alias.replace(' ','')

                if len(aliasLimpio) <= 20:
                    contraseña = input("Por favor introduzca una contraseña: ")     # No hace falta comprobar si es una contraseña númerica, ya que se pasa directamente a string (sea númerica o no)
                    contraseñaLimpia = contraseña.replace(' ','')     
                    print("")

                    nivel=1
                    ec=random.randint(-10,10)
                    ef=random.randint(-10,10)

                    msg = aliasLimpio + ":" + contraseñaLimpia + ":" + repr(nivel) + ":" + repr(ec) + ":" + repr(ef)

                    send(msg,clientRegistryCrear)

                    print(clientRegistryCrear.recv(2048).decode(FORMAT))
                    print("")

                else:
                    print("")
                    print("El alias debe tener 20 carácteres o menos. Intentelo de nuevo.")
                    print("")

                send("FIN",clientRegistryCrear)
                clientRegistryCrear.close()
            
            elif seleccion == 2:
                clientRegistryEditar = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientRegistryEditar.connect(REGISTRY_ADDR)

                editar()

                try:
                    parametro = int(input("Elección: "))
                    print("")

                    if parametro == 1: 
                        actualAlias = input("Por favor seleccione el alias actual: ")
                        aliasLimpio = actualAlias.replace(' ','')
                        actualContraseña = input("Por favor seleccione la contraseña actual: ")
                        contraseñaLimpia = actualContraseña.replace(' ','')
                        nuevoEC = int(input("Por favor seleccione el nuevo valor EC (de -10 a 10): "))
                        print("")

                        if nuevoEC >= -10 and nuevoEC <= 10:
                            msg = aliasLimpio + ":" + repr(nuevoEC) + ":" + "ec" + ":" + contraseñaLimpia 

                            send(msg,clientRegistryEditar)

                            print(clientRegistryEditar.recv(2048).decode(FORMAT))
                            print("")

                        else:
                            print("Por favor el nuevo valor de EC debe estar en el rango [-10,10]. Intentelo de nuevo.")
                            print("")
                        
                        send("FIN",clientRegistryEditar)
                        clientRegistryEditar.close()

                    elif parametro == 2: 
                        actualAlias = input("Por favor seleccione el alias actual: ")
                        aliasLimpio = actualAlias.replace(' ','')
                        actualContraseña = input("Por favor seleccione la contraseña actual: ")
                        contraseñaLimpia = actualContraseña.replace(' ','')
                        nuevoEF = int(input("Por favor seleccione el nuevo valor EF (de -10 a 10): "))
                        print("")

                        if nuevoEF >= -10 and nuevoEF <= 10:
                            msg = aliasLimpio + ":" + repr(nuevoEF) + ":" + "ef" + ":" + contraseñaLimpia 

                            send(msg,clientRegistryEditar)

                            print(clientRegistryEditar.recv(2048).decode(FORMAT))
                            print("") 

                        else:
                            print("Por favor el nuevo valor de EF debe estar en el rango [-10,10]. Intentelo de nuevo.")
                            print("") 

                        send("FIN",clientRegistryEditar)
                        clientRegistryEditar.close()  

                    elif parametro == 3:
                        actualAlias = input("Por favor seleccione el alias actual: ")
                        aliasLimpio = actualAlias.replace(' ','')
                        actualContraseña = input("Por favor seleccione la contraseña actual: ")
                        contraseñaLimpia = actualContraseña.replace(' ','')
                        nuevaContraseña = input("Por favor seleccione la nueva contraseña: ")
                        nuevaContraseñaLimpia = nuevaContraseña.replace(' ','')
                        print("")

                        msg = aliasLimpio + ":" + nuevaContraseñaLimpia + ":" + "c" + ":" + contraseñaLimpia 

                        send(msg,clientRegistryEditar)

                        print(clientRegistryEditar.recv(2048).decode(FORMAT))
                        print("")

                        send("FIN",clientRegistryEditar)
                        clientRegistryEditar.close()
                            
                    else:
                        print("Parametro desconocido.")
                        print("")

                        send("FIN",clientRegistryEditar)
                        clientRegistryEditar.close()

                except:
                    print("Por favor introduzca un caracter numérico.")
                    print("")

                    send("FIN",clientRegistryEditar)
                    clientRegistryEditar.close()

            elif seleccion == 3:
                clientEngine = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                clientEngine.connect(ENGINE_ADDR)

                alias = input("Por favor introduzca tu alias: ")
                aliasLimpio = alias.replace(' ','')
                contraseña = input("Por favor introduzca tu contraseña: ")
                contraseñaLimpia = contraseña.replace(' ','')
                print("")

                msg = aliasLimpio + ":" + contraseñaLimpia

                send(msg,clientEngine)

                existe = clientEngine.recv(2048).decode(FORMAT)

                if existe != "El usuario introducido no existe en la BBDD.":
                    TOKEN = existe
                    print("Se te ha asignado el TOKEN -> " + repr(TOKEN))
                    print("")
                    send("ESPERA", clientEngine)
                    respuesta = clientEngine.recv(2048).decode(FORMAT)    # Se queda esperando a recibir el mensaje de que va a empezar la partida
                    if respuesta == "Tiempo de espera finalizado Iniciando partida":
                        topicName = 'MAPA'
                        
                        try:
                            consumer = KafkaConsumer (topicName, bootstrap_servers = GESTOR_BOOTSTRAP_SERVER)
                            producer = KafkaProducer(bootstrap_servers = GESTOR_BOOTSTRAP_SERVER)
                            topicName = 'PLAYERS'
                            print
                            for mapa in consumer:
                                
                                system("cls")
                                if mapa.value.decode(FORMAT) == (TOKEN + ":FIN"):
                                    print("Has perdido")
                                    break
                                if mapa.value.decode(FORMAT) == (TOKEN + ":GANADOR"):
                                    print("Has ganado")
                                    break
                                print(mapa.value.decode(FORMAT))
                                #aqui tiene que imprimir el mapa
                                #print ("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value.decode('utf-8')))
                                while 1:
                                    if msvcrt.kbhit():
                                        entradaTec = msvcrt.getch()
                                        msg = TOKEN + ":" + entradaTec.decode(FORMAT)
                                        producer.send(topicName, msg.encode(FORMAT))
                                        break
                                
                        except :
                            print("Casca el envio o recibimientos de datos de Kafka")
                            pass

                        #limpio el buffer de teclas
                        while msvcrt.kbhit():
                            msvcrt.getch()
                        
                else:
                    print(existe)
                    clientEngine.close()

            elif seleccion == 4:
                bucle = False

            else:
                print("Esa opción no existe.")
                print("")
                bucle = True

    except:
        print("El servidor ha forzado la conexión y ha terminado.")
        print("")

else:
    print ("Parece que algo falló. Necesito estos argumentos para el Jugador: <Engine_IP> <Engine_Puerto> <GestorDeColas_IP> <Registry_IP> <Registry_Puerto>")