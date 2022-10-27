import random
import socket
import sys
from Posicion import *

HEADER = 64
FORMAT = 'utf-8'

class Jugador:
    def __init__ (self):
        self.posicion = Posicion(random.randint(1,20),random.randint(1,20))
        self.alias = ""
        self.nivel = 1
        self.EF = random.randint(-10,10)
        self.EC = random.randint(-10,10)
        self.muerto = False

    # Decrementa en una cierta cantidad el nivel del jugador
    def decrementarNivel(self, cantidad):
        self.nivel -= cantidad

        # El nivel mínimo es 0
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
    
    def vivoMuerto(self):
        return self.muerto

# Función que manda los mensajes del Jugador al Registry
def sendRegistry(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    clientRegistry.send(send_length)
    clientRegistry.send(message)

def menu():
    print("¿Qué quieres hacer ahora?")
    print("Crear perfil (1)")
    print("Editar perfil (2)")     
    print("Unirse a partida (3)")     # terminar
    print("Salir (4)")
    print("")

def editar():
    print("¿Qué parámetro quieres cambiar?: ")
    print("EC (1)")     
    print("EF (2)")     
    print("Contraseña (3)")
    print("")

# Main
if (len(sys.argv) == 7):
    ENGINE_IP = sys.argv[1]
    ENGINE_PUERTO = int(sys.argv[2])
    ENGINE_ADDR = (ENGINE_IP, ENGINE_PUERTO)

    GESTOR_IP = sys.argv[3]
    GESTOR_PUERTO = int(sys.argv[4])
    GESTOR_ADDR = (GESTOR_IP, GESTOR_PUERTO)

    REGISTRY_IP = sys.argv[5]
    REGISTRY_PUERTO = int(sys.argv[6])
    REGISTRY_ADDR = (REGISTRY_IP, REGISTRY_PUERTO)
            
    #clientEngine = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #clientGestor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientRegistry = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #clientEngine.connect(ENGINE_ADDR)
    #clientGestor.connect(GESTOR_ADDR)
    clientRegistry.connect(REGISTRY_ADDR)
    
    bucle = True

    print("")

    try:    
        while bucle:
            menu()
            seleccion = int(input("Elección: "))
            print("")

            if seleccion == 1:
                alias = input("Por favor introduzca un alias de hasta 20 carácteres: ")

                if len(alias) <= 20:
                    contraseña = input("Por favor introduzca una contraseña: ")
                    print("")

                    jugador = Jugador()
                    jugador.asignarAlias(alias)

                    nivel=jugador.obtenerNivel()
                    ec=jugador.obtenerEC()
                    ef=jugador.obtenerEF()

                    msg = alias + ":" + contraseña + ":" + repr(nivel) + ":" + repr(ec) + ":" + repr(ef)

                    sendRegistry(msg)

                    print(clientRegistry.recv(2048).decode(FORMAT))
                    print("")

                else:
                    print("")
                    print("El alias debe tener 20 carácteres o menos. Intentelo de nuevo.")
                    print("")
            
            elif seleccion == 2:
                editar()

                try:
                    parametro = int(input("Elección: "))
                    print("")

                    if parametro == 1: 
                        actualAlias = input("Por favor seleccione el alias actual: ")
                        actualContraseña = input("Por favor seleccione la contraseña actual: ")
                        nuevoEC = int(input("Por favor seleccione el nuevo valor EC (de -10 a 10): "))
                        print("")

                        if nuevoEC >= -10 and nuevoEC <= 10:
                            msg = actualAlias + ":" + repr(nuevoEC) + ":" + "ec" + ":" + actualContraseña 

                            sendRegistry(msg)

                            print(clientRegistry.recv(2048).decode(FORMAT))
                            print("")

                        else:
                            print("Por favor el nuevo valor de EC debe estar en el rango [-10,10]. Intentelo de nuevo.")
                            print("")

                    elif parametro == 2: 
                        actualAlias = input("Por favor seleccione el alias actual: ")
                        actualContraseña = input("Por favor seleccione la contraseña actual: ")
                        nuevoEF = int(input("Por favor seleccione el nuevo valor EF (de -10 a 10): "))
                        print("")

                        if nuevoEF >= -10 and nuevoEF <= 10:
                            msg = actualAlias + ":" + repr(nuevoEF) + ":" + "ef" + ":" + actualContraseña 

                            sendRegistry(msg)

                            print(clientRegistry.recv(2048).decode(FORMAT))
                            print("") 

                        else:
                            print("Por favor el nuevo valor de EF debe estar en el rango [-10,10]. Intentelo de nuevo.")
                            print("")       

                    elif parametro == 3:
                        actualAlias = input("Por favor seleccione el alias actual: ")
                        actualContraseña = input("Por favor seleccione la contraseña actual: ")
                        nuevaContraseña = input("Por favor seleccione la nueva contraseña: ")
                        print("")

                        msg = actualAlias + ":" + nuevaContraseña + ":" + "c" + ":" + actualContraseña 

                        sendRegistry(msg)

                        print(clientRegistry.recv(2048).decode(FORMAT))
                        print("")
                            
                    else:
                        print("Parametro desconocido.")
                        print("")

                except:
                    print("Por favor introduzca un caracter numérico.")
                    print("")

            elif seleccion == 3:
                alias = input("Por favor introduzca tu alias: ")
                contraseña = input("Por favor introduzca tu contraseña: ")
                print("")
                ### TERMINAR ###
                # 1- El player se conecta al engine y le pasa su alias y su password.
                # 2- El engine consulta en la BD si ese Player existe y su password es correcta.
                # 3- Caso que sea así le devuelve por el mismo socket que previamente se abrió. un token (que puedes expresar como un simple número aleatorio o hash ). Este token es como una "entrada de cine", una autorización que le vale SOLO PARA ESE PLAYER y esa partida.
                # 4- El player se conectará a partir de ese momento a Kafka y cada vez que envie un mensaje como productor, enviará en el mismo mensaje ese token (número) además de la información que quieras enviar (como la tecla pulsada).
                # 5- El engine, leerá el mensaje y validará que ese token existe. De esta manera habrá validado que puede procesar el mensaje y procederá a dicho procesamiento.

            elif seleccion == 4:
                bucle = False

            else:
                print("Esa opción no existe.")
                print("")
                bucle = True

        sendRegistry("FIN")
        print(clientRegistry.recv(2048).decode(FORMAT))
        print("")
        clientRegistry.close()

    except:
        print(f"El servidor ha forzado la conexión y ha terminado.")
        print("")
        clientRegistry.close()

else:
    print ("Parece que algo falló. Necesito estos argumentos para el Jugador: <Engine_IP> <Engine_Puerto> <GestorDeColas_IP> <GestorDeColas_Puerto> <Registry_IP> <Registry_Puerto>")