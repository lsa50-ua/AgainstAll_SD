import sys
import socket
import threading
import random
import time
import copy
from Mapa import *
from Jugador import *
from kafka import KafkaProducer
from kafka import KafkaConsumer

FORMAT = 'utf-8'
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
GESTOR_BOOTSTRAP_SERVER = ['localhost:9092']
TIMEOUT = 30
socket.setdefaulttimeout(30)

def menuPrincipal():
    print("Nueva partida (1)")
    print("Salir (2)")

def obtenerClimas(game):
    obj = socket.socket()

    #Conexión con el servidor. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
    obj.connect(WEATHER_ADDR)
    print("Conectado al servidor")

    ficheroC = open('Ciudades.txt', 'r')
    lineasC = ficheroC.readlines()
    ficheroC.close()
    lista_climas = []
    i = 0

    while len(lista_climas) != 4:
        #Con el método send, enviamos el mensaje
        obj.send(lineasC[i].rstrip().encode('utf-8'))
        #Cerramos la instancia del objeto servidor
        respuesta=obj.recv(4096)

        if respuesta.decode('utf-8') != "ERROR":
            lista_climas.append(respuesta.decode('utf-8'))
            i+=1
        else:
            print("ERROR: La ciudad ",lineasC[i].rsplit(), "no existe")
            break

    obj.send("0".encode('utf-8'))

    if len(lista_climas) == 4:
        climas = []
        ciudades = []

        print("El mapa esta compuesto por las siguientes ciudades: ")

        for i in range(len(lista_climas)):
            separados = lista_climas[i].split(sep=':')
            print(separados[0], separados[1], end="")
            print("ºC")
            climas.append(separados[1])
            ciudades.append(separados[0])

        game.Climas(climas)
        game.Ciudades(ciudades)     # Guardo las ciudades y sus climas en el mapa
        
    obj.close()
    print("Conexión con el servidor del tiempo cerrada")
    return lista_climas

    
if (len(sys.argv) == 5):
    PUERTO = int(sys.argv[1])
    MAX_CONEXIONES = int(sys.argv[2])     # Número máximo de jugadores que se puede conectar a la partida

    WEATHER_IP = sys.argv[3]
    WEATHER_PUERTO = int(sys.argv[4])
    WEATHER_ADDR = (WEATHER_IP,WEATHER_PUERTO)

    ADDR_ESCUCHAR = (SERVER,PUERTO)

    def handle_client(conn,addr, starttime):
        print(f"[NUEVA CONEXION] {addr} connected.")
        global jugadores_preparados
        connected = True
        tieneToken = False

        try:
            while connected:
                try:
                    msg_length = conn.recv(HEADER).decode(FORMAT)
                except:
                    pass

                if msg_length:
                    msg_length = int(msg_length)
                    try:
                        msg = conn.recv(msg_length).decode(FORMAT)
                    except:
                        pass   
                    parametros = msg.split(":")
                    
                    if msg == "FIN":
                        connected = False
                    elif msg == "ESPERA":
                        if (time.time() - starttime) > TIMEOUT:
                            connected = False
                        else:
                            while True:
                                if (time.time() - starttime) > TIMEOUT:
                                    break
                            if len(jugadores_preparados) > 1:       
                                info = "Tiempo de espera finalizado Iniciando partida"
                                conn.send(info.encode(FORMAT))
                            else:
                                info = "No se puede iniciar partida jugadores insuficientes"
                                conn.send(info.encode(FORMAT))
                                connected = False
                    elif len(parametros) == 2:
                        ALIAS = parametros[0]
                        PASSWORD = parametros[1]

                        encontrado = False
                        distintoDe0 = False

                        with open("Registro.txt", "r") as f:
                            lines = f.readlines()
                            lines.pop(0)

                        for line in lines:
                            particion = line.split(" ")
                            buscarAlias = particion[0].split(":")
                            buscarContraseña = particion[1].split(":")
                            buscarTOKEN = particion[5].split(":")

                            if buscarAlias[1] == ALIAS and buscarContraseña[1] == PASSWORD:
                                encontrado = True  

                                revisarToken = buscarTOKEN[1].replace('\n','')     

                                if revisarToken != "0":
                                    YATIENETOKEN = revisarToken
                                    distintoDe0 = True

                        if distintoDe0:
                            mensaje = YATIENETOKEN
                            conn.send(mensaje.encode(FORMAT))
                            print("El jugador '" + ALIAS + "' se ha unido a la partida con el TOKEN -> " + repr(YATIENETOKEN) + ".")
                            TOKEN = YATIENETOKEN
                            jugadores_preparados.append(TOKEN)
                            tieneToken = True

                        elif encontrado:
                            previo = True
                            estaElToken = False
                            añadidoTOKEN = False

                            while previo:
                                TOKEN = random.randint(1,10000)

                                with open("Registro.txt", "r") as f:
                                    lines = f.readlines()
                                    lines.pop(0)

                                for line in lines:
                                    particion = line.split(" ")
                                    buscarTOKEN = particion[5].split(":")

                                    if buscarTOKEN[1] == TOKEN:
                                        estaElToken = True  
                                
                                if estaElToken == False:
                                    previo = False

                            with open("Registro.txt", "r") as f:
                                lines = f.readlines()
                                lines.pop(0)

                            with open("Registro.txt", "w") as f:
                                f.write("#Usuarios"+'\n')

                                for line in lines:
                                    particion = line.split(" ")
                                    buscarAlias = particion[0].split(":")
                                    buscarContraseña = particion[1].split(":")

                                    if buscarAlias[1] == ALIAS and buscarContraseña[1] == PASSWORD:
                                        buscarNivel = particion[2].split(":")
                                        buscarEC = particion[3].split(":")
                                        buscarEF = particion[4].split(":")

                                        f.write('ALIAS:' + buscarAlias[1] + ' CONTRASEÑA:' + buscarContraseña[1] + ' NIVEL:' + buscarNivel[1] + ' EC:' + buscarEC[1] + ' EF:' + buscarEF[1] + ' TOKEN:' + repr(TOKEN) + '\n')

                                        print("")
                                        print("El jugador '" + buscarAlias[1] + "' se ha unido a la partida con el TOKEN -> " + repr(TOKEN) + ".")
                                        jugadores_preparados.append(TOKEN)
                                        mensaje = TOKEN
                                        conn.send(mensaje.encode(FORMAT))
                                        añadidoTOKEN = True
                                        tieneToken = True
                                    else:
                                        f.write(line)    

                            if añadidoTOKEN == False:
                                conn.send("El usuario introducido no existe en la BBDD.".encode(FORMAT))
                                conn.close()

                        else:
                            conn.send("El usuario introducido no existe en la BBDD.".encode(FORMAT))
                            conn.close()

                    else:
                        connected = True
            
            print("")
            print(f"Cerrada la conexión en: {addr} ")
            print("")

            if tieneToken:
                jugadores_preparados.remove(TOKEN)

            conn.close()

        except:
            print("")
            print(f"Se ha forzado la conexión y ha terminado en: {addr} ")

            if tieneToken:
                jugadores_preparados.remove(TOKEN)

            conn.close()

    def start():
        server.listen()
        print("")
        print(f"[LISTENING] Engine a la escucha en {SERVER}")
        CONEX_ACTIVAS = threading.active_count()-1
        print("")
        starttime = time.time()
        empezar = False
        global jugadores_preparados
        jugadores_preparados = []
        climas = []
        print("Tiempo restante para iniciar partida: ", TIMEOUT," s")

        while True:
            if (time.time() - starttime) > TIMEOUT:
                if len(jugadores_preparados) < 2:
                    print("La partida no se puede iniciar por falta de jugadores, Volviendo al menu...")
                    break
                else:
                    if len(climas) != 4:
                        game = Mapa()     # Mapa del juego
                        climas = obtenerClimas(game)

                        if len(climas) != 4:
                            print("Falta o falla algo en Ciudades.txt; Abortando Partida, Volviendo al menu...")
                            break

                        else:
                            print()
                            print("Comenzando Partida")
                            print()
                            pInGame = copy.deepcopy(jugadores_preparados)
                            acabada = False
                            topicName = 'PLAYERS'

                            # Fichero donde se guardan los TOKENS de los jugadores que empiezan a jugar en la partida
                            # Sirve para saber si hay que crear un jugador con ese TOKEN o si ya ha sido creado

                            #file = open("Jugando.txt", "w")
                            #file.write()
                            #file.close()

                            try:
                                consumer = KafkaConsumer (topicName, bootstrap_servers = GESTOR_BOOTSTRAP_SERVER)
                                producer = KafkaProducer(bootstrap_servers = GESTOR_BOOTSTRAP_SERVER)
                                # mandar el mapa generado a todos los jugadores

                                producer.send('MAPA', "hello".encode(FORMAT))

                                while acabada != True:
                                    for movimiento in consumer:
                                        print(movimiento.value.decode(FORMAT))     # SACAR EL TOKEN Y EL MOVIMIENTO DE AQUÍ, CON SPLIT
                                        #hacer respectivo movimiento en el mapa calcular si se ha pegado con alguien, subido de nivel, explotado mina
                                        #producer.send('MAPA', mapa.encode(FORMAT))
                                        producer.send('MAPA', "adios".encode(FORMAT))

                                        if len(pInGame) == 1:
                                            print("Ha ganado el jugador con el Token: ",jugadores_preparados[0])
                                            ganador = jugadores_preparados[0] + ":GANADOR"
                                            producer.send('MAPA', ganador.encode(FORMAT))
                                            acabada = True
                                            break

                            except:
                                print("Casca el kafka")
                                pass
            else:
                try:
                    conn, addr = server.accept()
                except:
                    pass

                if (time.time() - starttime) < TIMEOUT:
                    CONEX_ACTIVAS = threading.active_count()
                    
                    if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
                        thread = threading.Thread(target=handle_client, args=(conn, addr, starttime))
                        thread.start()

                        #print('\n' + f"[CONEXIONES ACTIVAS]: {CONEX_ACTIVAS}")
                        #print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO: " + repr(MAX_CONEXIONES-CONEX_ACTIVAS))
                        
                    else:
                        print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
                        conn.send("Demasiadas conexiones. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
                        conn.close()
                        CONEX_ACTUALES = threading.active_count()-1

            

    ######################### MAIN ##########################

    print("")
    print("Iniciando Engine.")
    print("")

    seguir = True

    try:
        while seguir:
            menuPrincipal()

            try:
                eleccion = int(input('Elige una opcion: '))
            except:
                pass

            print("")

            if eleccion == 1:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.bind(ADDR_ESCUCHAR)
                start()
                server.close()

            elif eleccion == 2:
                seguir = False           

            else:
                print("Introduce una opción correcta.")
                print("")
                break

    except ValueError:
            print("")
            print("Por favor introduzca un carácter númerico.")
            print("")

else:
    print ("Parece que algo falló. Necesito estos argumentos para el Jugador: <Puerto_Escucha> <MAX_Jugadores> <Weather_IP> <Weather_Puerto>")