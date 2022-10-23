from inspect import getargs
import random
import socket
import sys
from Posicion import *

#PORT = 5050
HEADER = 64
FORMAT = 'utf-8'

# Clase que define a los jugadores de la partida
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

    while bucle:
        print("¿Qué quieres hacer ahora?")
        print("Crear perfil (1)")     # TERMINADO
        print("Editar perfil (2)")     # terminar
        print("Unirse a partida (3)")     # terminar
        print("Salir (4)")
        seleccion = int(input())
        print("")

        if seleccion == 1:
            print("Por favor introduzca un alias: ")
            alias = input()
            print("")
            print("Por favor introduzca una contraseña: ")
            contraseña = input()
            print("")

            jugador = Jugador()
            jugador.asignarAlias(alias)

            nivel=jugador.obtenerNivel()
            ec=jugador.obtenerEC()
            ef=jugador.obtenerEF()

            msg = alias + ":" + contraseña + ":" + repr(nivel) + ":" + repr(ec) + ":" + repr(ef)

            sendRegistry(msg)
        
        elif seleccion == 2:
            print("¿Qué parámetro quieres cambiar?: ")
            print("Alias (1)")
            print("Contraseña (2)")

            try:
                parametro = int(input())
                print("")

                if parametro == 1: 
                    print("Por favor seleccione el alias actual: ")
                    actualAlias = input()
                    print("")

                    print("Por favor seleccione la contraseña actual: ")
                    actualContraseña = input()
                    print("")

                    print("Por favor seleccione el nuevo alias: ")
                    nuevoAlias = input()
                    print("")

                    msg = actualAlias + ":" + nuevoAlias + ":" + "alias" + ":" + actualContraseña 

                    sendRegistry(msg)

                    print("Se ha cambiado el alias a: " + nuevoAlias)                    

                elif parametro == 2:
                    print("Por favor seleccione el alias actual (si no existe no se podrá realizar el cambio): ")
                    actualAlias = input()
                    print("")
                    
                    print("Por favor seleccione la nueva contraseña: ")
                    nuevaContraseña = input()
                    print("")

                    msg = actualAlias + ":" + nuevaContraseña + ":" + "contraseña"

                    sendRegistry(msg)

                    print("Se ha cambiado la contraseña a: " + nuevaContraseña)
                        
                else:
                    bucle = False
                    print("Parametro desconocido. Termina la conexión.")

            except:
                print("Por favor introduzca un caracter numérico.")
                print("")

        elif seleccion == 4:
            bucle = False
            print("Terminamos la conexión. Hasta luego.")

        else:
            print("Esa opción no existe.")
            print("")
            bucle = True

    sendRegistry("FIN")
    clientRegistry.close()

else:
    print ("Parece que algo falló. Necesito estos argumentos para el Jugador: <Engine_IP> <Engine_Puerto> <GestorDeColas_IP> <GestorDeColas_Puerto> <Registry_IP> <Registry_Puerto>")