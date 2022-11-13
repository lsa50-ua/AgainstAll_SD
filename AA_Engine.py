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
TIMEOUT = 10
socket.setdefaulttimeout(10)

def menuPrincipal():
    print("Nueva partida (1)")
    print("Salir (2)")

def infoPlayers(lista):
    info = "INFOP: "
    for i in range(len(lista)):
        info += "Jugador " + lista[i].getAlias() + " Posicion(" + lista[i].obtenerPosicion().getY() + "," + lista[i].obtenerPosicion().getX() + ") Nivel: " + str(lista[i].obtenerNivel())
        if i < (len(lista) - 1):
            info += ";"

def obtenerClimas(game):
    obj = socket.socket()
    obj.connect(WEATHER_ADDR)
    print("")
    print("Conectado al servidor clima.")
    print("")

    ficheroC = open('Ciudades.txt', 'r')
    lineasC = ficheroC.readlines()
    ficheroC.close()
    lista_climas = []
    i = 0

    while len(lista_climas) != 4:
        obj.send(lineasC[i].rstrip().encode('utf-8'))
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
    print("")
    print("Conexión con el servidor del tiempo cerrada.")
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
                                info = "Tiempo de espera finalizado. Iniciando partida."
                                conn.send(info.encode(FORMAT))
                            else:
                                info = "No se puede iniciar partida jugadores insuficientes."
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
                            buscarEC = particion[3].split(":")
                            buscarEF = particion[4].split(":")
                            buscarTOKEN = particion[5].split(":")

                            if buscarAlias[1] == ALIAS and buscarContraseña[1] == PASSWORD:
                                encontrado = True  

                                revisarToken = buscarTOKEN[1].replace('\n','')     

                                if revisarToken != "0":
                                    YATIENETOKEN = revisarToken
                                    YATIENEALIAS = buscarAlias[1]
                                    YATIENENIVEL = 1
                                    YATIENEEC = buscarEC[1]
                                    YATIENEEF = buscarEF[1]
                                    TIENECONTRA = buscarContraseña[1]
                                    distintoDe0 = True

                        if distintoDe0:
                            mensaje = YATIENETOKEN
                            conn.send(mensaje.encode(FORMAT))
                            print("El jugador '" + ALIAS + "' se ha unido a la partida con el TOKEN -> " + repr(YATIENETOKEN) + ".")
                            TOKEN = YATIENETOKEN

                            jugadorConTOKEN = Jugador()
                            jugadorConTOKEN.asignarAlias(YATIENEALIAS)
                            jugadorConTOKEN.asignarEC(int(YATIENEEC))
                            jugadorConTOKEN.asignarNivel(1)
                            jugadorConTOKEN.asignarTOKEN(str(TOKEN))
                            jugadorConTOKEN.asignarContraseña(TIENECONTRA)
                            jugadorConTOKEN.asignarEF(int(YATIENEEF))
                            jugadorConTOKEN.Vivo()

                            jugadores_preparados.append(jugadorConTOKEN)

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

                            escribir = False

                            with open("Registro.txt", "r") as f:
                                lines = f.readlines()
                                lines.pop(0)

                            with open("Registro.txt", "w") as f:
                                f.write("#Usuarios")
                                f.write('\n')

                                for line in lines:
                                    particion = line.split(" ")
                                    buscarAlias = particion[0].split(":")
                                    buscarContraseña = particion[1].split(":")

                                    if buscarAlias[1] == ALIAS and buscarContraseña[1] == PASSWORD:
                                        buscarNivel = particion[2].split(":")
                                        buscarEC = particion[3].split(":")
                                        buscarEF = particion[4].split(":")

                                        MENSAJE = 'ALIAS:' + buscarAlias[1] + ' CONTRASEÑA:' + buscarContraseña[1] + ' NIVEL:' + buscarNivel[1] + ' EC:' + buscarEC[1] + ' EF:' + buscarEF[1] + ' TOKEN:' + repr(TOKEN)

                                        escribir = True

                                        print("")
                                        print("El jugador '" + buscarAlias[1] + "' se ha unido a la partida con el TOKEN -> " + repr(TOKEN) + ".")

                                        jugadorSinTOKEN = Jugador()
                                        jugadorSinTOKEN.asignarAlias(buscarAlias[1])
                                        jugadorSinTOKEN.asignarEC(int(buscarEC[1]))
                                        jugadorSinTOKEN.asignarNivel(1)
                                        jugadorSinTOKEN.asignarTOKEN(str(TOKEN))
                                        jugadorSinTOKEN.asignarContraseña(buscarContraseña[1])
                                        jugadorSinTOKEN.asignarEF(int(buscarEF[1]))
                                        jugadorSinTOKEN.Vivo()

                                        jugadores_preparados.append(jugadorSinTOKEN)     
                                        mensaje = repr(TOKEN)
                                        conn.send(mensaje.encode(FORMAT))
                                        añadidoTOKEN = True
                                        tieneToken = True 
                                    else:
                                        f.write(line)    

                                if escribir:
                                    f.write('\n' + MENSAJE)     # Se pone al jugador con el nuevo TOKEN al final del tablero, para evitar el error del salto de linea

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
                posiciones = []
                algunMuerto = False
                for i in range(len(jugadores_preparados)):
                    if str(TOKEN) == jugadores_preparados[i].obtenerTOKEN():
                        posiciones.append(i) 
                        algunMuerto = True
                
                if algunMuerto:
                    for posicion in posiciones:
                        jugadores_preparados.pop(posicion)

            conn.close()

        except:
            print("")
            print(f"Se ha forzado la conexión y ha terminado en: {addr} ")

            if tieneToken:
                posiciones = []
                algunMuerto = False
                for i in range(len(jugadores_preparados)):
                    if str(TOKEN) == jugadores_preparados[i].obtenerTOKEN():
                        posiciones.append(i)
                        algunMuerto = True
                
                if algunMuerto:
                    for posicion in posiciones:
                        jugadores_preparados.pop(posicion)

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
        listaNPC = []
        print("Tiempo restante para iniciar partida: ", TIMEOUT," s")
        print("")

        while True:
            if (time.time() - starttime) > TIMEOUT:
                if len(jugadores_preparados) < 2:
                    print("La partida no se puede iniciar por falta de jugadores, Volviendo al menu...")
                    print("")
                    break
                else:
                    if len(climas) != 4:
                        game = Mapa()     # Mapa del juego
                        game.Jugadores(jugadores_preparados)     # Guardo los jugadores en el mapa
                        climas = obtenerClimas(game)

                        if len(climas) != 4:
                            print("Falta o falla algo en Ciudades.txt; Abortando Partida, Volviendo al menu...")
                            print("")
                            break

                        else:
                            print()
                            print("Comenzando Partida")
                            print()
                            pInGame = copy.deepcopy(jugadores_preparados)
                            acabada = False
                            topicName = 'PLAYERS'

                            for i in range(len(pInGame)):
                                game.incorporarJugador(pInGame[i].obtenerTOKEN())     # Pone a todos los jugadores en su posición inicial 

                            pInGame = game.getJugadores()     # Para que estén actualizados los niveles

                            try:
                                consumer = KafkaConsumer (topicName, bootstrap_servers = GESTOR_BOOTSTRAP_SERVER)
                                producer = KafkaProducer(bootstrap_servers = GESTOR_BOOTSTRAP_SERVER)
                                #info = infoPlayers(pInGame)
                                #producer.send('MAPA', info.encode(FORMAT))
                                cadena = game.matrizToString()
                                producer.send('MAPA', cadena.encode(FORMAT))

                                while acabada != True:
                                    for movimiento in consumer:
                                        movimientoJugador = movimiento.value.decode(FORMAT).split(":")

                                        if len(movimientoJugador) == 2:
                                            tokenJugador = movimientoJugador[0]
                                            moverJugador = movimientoJugador[1]      

                                            if moverJugador != "ESCAPE":     # ha pulsado ESCAPE
                                                if moverJugador == 'w' or moverJugador == 'W':     # w-W -> ARRIBA
                                                    print("El jugador " + tokenJugador + " ha pulsado la tecla " + moverJugador + ".")
                                                    game.moduloW(tokenJugador)

                                                elif moverJugador == 's' or moverJugador == 'S':     # s-S -> ABAJO
                                                    print("El jugador " + tokenJugador + " ha pulsado la tecla " + moverJugador + ".")
                                                    game.moduloS(tokenJugador)
                                        
                                                elif moverJugador == 'a' or moverJugador == 'A':     # a-A -> IZQUIERDA
                                                    print("El jugador " + tokenJugador + " ha pulsado la tecla " + moverJugador + ".")
                                                    game.moduloA(tokenJugador)

                                                elif moverJugador == 'd' or moverJugador == 'D':      # d-D -> DERECHA
                                                    print("El jugador " + tokenJugador + " ha pulsado la tecla " + moverJugador + ".")
                                                    game.moduloD(tokenJugador)

                                                elif moverJugador == 'e' or moverJugador == 'E':      # e-E -> ARRIBA-DERECHA
                                                    print("El jugador " + tokenJugador + " ha pulsado la tecla " + moverJugador + ".")
                                                    game.moduloE(tokenJugador)

                                                elif moverJugador == 'q' or moverJugador == 'Q':      # q-Q -> ARRIBA-IZQUIERDA
                                                    print("El jugador " + tokenJugador + " ha pulsado la tecla " + moverJugador + ".")
                                                    game.moduloQ(tokenJugador)
                                                
                                                elif moverJugador == 'z' or moverJugador == 'Z':      # z-Z -> ABAJO-IZQUIERDA
                                                    print("El jugador " + tokenJugador + " ha pulsado la tecla " + moverJugador + ".")
                                                    game.moduloZ(tokenJugador)

                                                elif moverJugador == 'c' or moverJugador == 'C':      # c-C -> ABAJO-DERECHA
                                                    print("El jugador " + tokenJugador + " ha pulsado la tecla " + moverJugador + ".")
                                                    game.moduloC(tokenJugador)

                                                else:
                                                    print("El jugador '" + tokenJugador + "' ha pulsado una tecla incorrecta.")

                                                
                                                for i in range(len(pInGame)):
                                                    print(pInGame[i].obtenerNivel())

                                                    #for i in range(len(pInGame)):
                                                        #if pInGame[i].obtenerTOKEN() == tokenJugador:
                                                            #mensaje = pInGame[i].obtenerTOKEN() + ":INCORRECTA"

                                                    #producer.send('MAPA', mensaje.encode(FORMAT))
                                                """
                                                listaMsgMuertos = game.matarJugadores()
                                                
                                                for i in range(len(listaMsgMuertos)):
                                                    producer.send('MAPA', listaMsgMuertos[i].encode(FORMAT))
                                                    particion = listaMsgMuertos[i].split(":")

                                                    print("")
                                                    print("El jugador '" + particion[0] + "' ha sido eliminado de la partida.")
                                                    print("")
                                                
                                                pInGame = game.getJugadores()
                                                """
                                                
                                            else:
                                                print("El jugador " + tokenJugador + " ha decidido abandonar la partida.")     # Hacer lo necesario para que sea eliminado de la partida                            ##### IMPORTANTE ##### 
                                                msgInfo = tokenJugador + ":FIN"
                                                for i in range(len(pInGame)):
                                                    if pInGame[i].obtenerTOKEN() == tokenJugador:
                                                        pInGame[i].Muerto()

                                                producer.send('MAPA', msgInfo.encode(FORMAT))

                                        movimientoNPC = movimiento.value.decode(FORMAT).split('-')
                                        if len(movimientoNPC) == 2:
                                            tokenNPC = movimientoNPC[0]
                                            jugadaNPC = movimientoNPC[1]
                                            if jugadaNPC == 'w':     # w-W -> ARRIBA
                                                print("El NPC: " + tokenNPC + " ha pulsado la tecla " + jugadaNPC + ".")
                                                game.moduloW_N(tokenNPC)
                                            elif jugadaNPC == 's':     # s-S -> ABAJO
                                                print("El NPC: " + tokenNPC + " ha pulsado la tecla " + jugadaNPC + ".")
                                                game.moduloS_N(tokenNPC)                                    
                                            elif jugadaNPC == 'a':     # a-A -> IZQUIERDA
                                                print("El NPC: " + tokenNPC + " ha pulsado la tecla " + jugadaNPC + ".")
                                                game.moduloA_N(tokenNPC)
                                            elif jugadaNPC == 'd':      # d-D -> DERECHA
                                                print("El NPC: " + tokenNPC + " ha pulsado la tecla " + jugadaNPC + ".")
                                                game.moduloD_N(tokenNPC)
                                            elif jugadaNPC == 'e':      # e-E -> ARRIBA-DERECHA
                                                print("El NPC: " + tokenNPC + " ha pulsado la tecla " + jugadaNPC + ".")
                                                game.moduloE_N(tokenNPC)
                                            elif jugadaNPC == 'q':      # q-Q -> ARRIBA-IZQUIERDA
                                                print("El NPC: " + tokenNPC + " ha pulsado la tecla " + jugadaNPC + ".")
                                                game.moduloQ_N(tokenNPC)   
                                            elif jugadaNPC == 'z':      # z-Z -> ABAJO-IZQUIERDA
                                                print("El NPC: " + tokenNPC + " ha pulsado la tecla " + jugadaNPC + ".")
                                                game.moduloZ_N(tokenNPC)
                                            elif jugadaNPC == 'c':      # c-C -> ABAJO-DERECHA
                                                print("El NPC: " + tokenNPC + " ha pulsado la tecla " + jugadaNPC + ".")
                                                game.moduloC_N(tokenNPC)
                                            elif jugadaNPC == "NewNPC":
                                                repe = False
                                                listaNPC = game.getNPCs()
                                                for i in range(len(listaNPC)):
                                                    if listaNPC[i].obtenerTOKEN() == tokenNPC:
                                                        msgRepe = tokenNPC + ":repetido"
                                                        producer.send('MAPA', msgRepe.encode(FORMAT))
                                                        repe = True
                                                        break
                                                if repe == False:
                                                    
                                                    msgOK = tokenNPC +":OK"
                                                    time.sleep(1)
                                                    newNPC = NPC()
                                                    newNPC.asignarTOKEN(tokenNPC)
                                                    producer.send('MAPA', msgOK.encode(FORMAT))
                                                    
                                                    game.añadirNPC(newNPC)
                                                    game.incorporarNPC(tokenNPC)
                                                    print("NPC con el token: " + tokenNPC + " y nivel: " + newNPC.obtenerNivel_Char() + " entrando en partida")
                                                    

                                        listaMsgMuertos = game.matarJugadores()
                                                
                                        for i in range(len(listaMsgMuertos)):
                                            producer.send('MAPA', listaMsgMuertos[i].encode(FORMAT))
                                            particion = listaMsgMuertos[i].split(":")

                                            print("")
                                            print("El jugador '" + particion[0] + "' ha sido eliminado de la partida.")
                                            print("")

                                        listaNPCMuertos = game.matarNPCs()
                                        for i in range(len(listaNPCMuertos)):
                                            producer.send('MAPA', listaNPCMuertos[i].encode(FORMAT))
                                            particion = listaNPCMuertos[i].split("-")

                                            print("")
                                            print("El NPC '" + particion[0] + "' ha sido eliminado de la partida.")
                                            print("")
                                        
                                        pInGame = game.getJugadores()
                                        
                                        #info = infoPlayers(pInGame)
                                        #producer.send('MAPA', info.encode(FORMAT))                                                    
                                        cadena = game.matrizToString()
                                        producer.send('MAPA', cadena.encode(FORMAT))

                                        if len(pInGame) == 1:
                                            print("Ha ganado el jugador con el Token: ",pInGame[0].obtenerTOKEN())     
                                            ganador = pInGame[0].obtenerTOKEN() + ":GANADOR"     
                                            producer.send('MAPA', ganador.encode(FORMAT))
                                            acabada = True
                                            producer.send('MAPA', "FinDePartida".encode(FORMAT))
                                            break
                                
                            except:
                                print("Casca el kafka.")
                                producer.send('MAPA', "FinDePartida".encode(FORMAT))
                                pass
                            break
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
                        
                    else:
                        print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA.")
                        conn.send("Demasiadas conexiones. Tendrás que esperar a que alguien se vaya.".encode(FORMAT))
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