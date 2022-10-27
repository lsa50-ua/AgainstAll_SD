import sys
import socket
import threading

FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())

if (len(sys.argv) == 7):
    PUERTO = int(sys.argv[1])
    MAX_CONEXIONES = int(sys.argv[2])

    WEATHER_IP = sys.argv[3]
    WEATHER_PUERTO = int(sys.argv[4])
    WEATHER_ADDR = (WEATHER_IP,WEATHER_PUERTO)

    GESTOR_IP = sys.argv[5]
    GESTOR_PUERTO = int(sys.argv[6])
    GESTOR_ADDR = (GESTOR_IP,GESTOR_PUERTO)

    ADDR_ESCUCHAR = (SERVER,PUERTO)

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

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR_ESCUCHAR)
    start()

else:
    print ("Parece que algo falló. Necesito estos argumentos para el Jugador: <Puerto_Escucha> <MAX_Jugadores> <Weather_IP> <Weather_Puerto> <GestorDeColas_IP> <GestorDeColas_Puerto>")







    #para pillar las teclas del jugador usamos en python, msvrct.getch()decode(FORMAT)
    # startime = time.time()
    # 
    # while True:
    #   msg = ""
    #   if  msvcrt SEGUIR CON LA FOTO DE LUIS