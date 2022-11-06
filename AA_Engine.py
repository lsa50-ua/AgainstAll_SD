import sys
import socket
import threading
import random

FORMAT = 'utf-8'
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
bootstrap_servers = ['localhost:9092']

def menuPrincipal():
    print("Nueva partida (1)")
    print("Salir (2)")

if (len(sys.argv) == 5):
    PUERTO = int(sys.argv[1])
    MAX_CONEXIONES = int(sys.argv[2])     # Número máximo de jugadores que se puede conectar a la partida

    WEATHER_IP = sys.argv[3]
    WEATHER_PUERTO = int(sys.argv[4])
    WEATHER_ADDR = (WEATHER_IP,WEATHER_PUERTO)


    ADDR_ESCUCHAR = (SERVER,PUERTO)

    def handle_client(conn,addr):
        print(f"[NUEVA CONEXION] {addr} connected.")

        connected = True

        try:
            while connected:
                msg_length = conn.recv(HEADER).decode(FORMAT)

                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    parametros = msg.split(":")

                    if msg == "FIN":
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
                            info = "Tu usuario ya tiene un TOKEN asignado. El TOKEN -> " + repr(YATIENETOKEN)
                            conn.send(info.encode(FORMAT))

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
                                        print("El jugador '" + buscarAlias[1] + "' ha se ha unido a la partida con el TOKEN-" + repr(TOKEN) + ".")
                                        mensaje = "Se te ha asignado el TOKEN -> '" + repr(TOKEN) + "'"
                                        conn.send(mensaje.encode(FORMAT))
                                        añadidoTOKEN = True
                                        
                                    else:
                                        f.write(line)    

                            if añadidoTOKEN == False:
                                conn.send("El usuario introducido no existe en la BBDD.".encode(FORMAT))

                        else:
                            conn.send("El usuario introducido no existe en la BBDD.".encode(FORMAT))

                    else:
                        connected = True
            
            print("")
            print(f"Cerrada la conexión en: {addr} ")
            print("")
            conn.close()

        except:
            print("")
            print(f"Se ha forzado la conexión y ha terminado en: {addr} ")
            conn.close()

    def start():
        server.listen()
        print("")
        print(f"[LISTENING] Engine a la escucha en {SERVER}")
        CONEX_ACTIVAS = threading.active_count()-1
        print("")

        while True:
            conn, addr = server.accept()
            CONEX_ACTIVAS = threading.active_count()

            if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
                thread = threading.Thread(target=handle_client, args=(conn, addr))
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

            eleccion = int(input("Por favor introduzca la eleccion: "))
            print("")

            if eleccion == 1:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.bind(ADDR_ESCUCHAR)
                start()

            elif eleccion == 2:
                seguir = False
            
            else:
                print("Introduce una opción correcta.")
                print("")
    except:
            print("")
            print("Por favor introduzca un carácter númerico.")
            print("")

else:
    print ("Parece que algo falló. Necesito estos argumentos para el Jugador: <Puerto_Escucha> <MAX_Jugadores> <Weather_IP> <Weather_Puerto> <GestorDeColas_IP> <GestorDeColas_Puerto>")