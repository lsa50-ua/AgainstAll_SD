import socket 
import threading
import sys

HEADER = 64
FORMAT = 'utf-8'
MAX_CONEXIONES = 100     # nº conexiones que puede conectar a la vez
SERVER = socket.gethostbyname(socket.gethostname())

if (len(sys.argv) == 2):
    PORT = int(sys.argv[1])
    ADDR = (SERVER,PORT)

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

                    elif len(parametros) == 5:
                        ALIAS = parametros[0]
                        PASSWORD = parametros[1]
                        NIVEL = parametros[2]
                        EC = parametros[3]
                        EF = parametros[4]

                        cambiar = True

                        with open("Registro.txt", "r") as f:
                            lines = f.readlines()
                            lines.pop(0)

                        for line in lines:
                            particion = line.split(" ")
                            buscarAlias = particion[0].split(":")

                            if buscarAlias[1] == parametros[0]:
                                cambiar = False                  
                        
                        if cambiar == True:
                            f = open('Registro.txt','a')    # 'a' significa "append" y nos permite escribir en un fichero ya creado
                            f.write('\n')
                            f.write('ALIAS:'+ ALIAS + ' CONTRASEÑA:' + PASSWORD + ' NIVEL:' + NIVEL + ' EC:' + EC + ' EF:' + EF + ' TOKEN:' + repr(0))    # '\n' para escribir en un línea abajo
                            f.close()

                            print("")
                            print("El jugador '"+ ALIAS + "' se ha registrado en la base de datos.")
                            conn.send("El registro ha sido correcto.".encode(FORMAT))

                        else:
                            conn.send("El registro no se ha podido llevar a cabo. El alias ya existe.".encode(FORMAT))
                        
                    elif len(parametros) == 4:
                        if parametros[2] == "ec":
                            cambiadoEC = False

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

                                    if buscarAlias[1] == parametros[0] and buscarContraseña[1] == parametros[3]:
                                        buscarNivel = particion[2].split(":")
                                        buscarEC = particion[3].split(":")
                                        buscarEF = particion[4].split(":")
                                        buscarTOKEN = particion[5].split(":")

                                        f.write('ALIAS:' + buscarAlias[1] + ' CONTRASEÑA:' + buscarContraseña[1] + ' NIVEL:' + buscarNivel[1] + ' EC:' + parametros[1] + ' EF:' + buscarEF[1] + ' TOKEN:' + buscarTOKEN[1])

                                        print("")
                                        print("El jugador '" + buscarAlias[1] + "' se ha cambiado correctamente el EC.")
                                        conn.send("El cambio de EC ha sido correcto.".encode(FORMAT))
                                        cambiadoEC = True
                                        
                                    else:
                                        f.write(line)    

                            if cambiadoEC == False:
                                conn.send("El cambio de EC ha sufrido un error. Introduzca los parámetros correctos.".encode(FORMAT))

                        elif parametros[2] == "ef":
                            cambiadoEF = False

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

                                    if buscarAlias[1] == parametros[0] and buscarContraseña[1] == parametros[3]:
                                        buscarNivel = particion[2].split(":")
                                        buscarEC = particion[3].split(":")
                                        buscarEF = particion[4].split(":")
                                        buscarTOKEN = particion[5].split(":")

                                        f.write('ALIAS:' + buscarAlias[1] + ' CONTRASEÑA:' + buscarContraseña[1] + ' NIVEL:' + buscarNivel[1] + ' EC:' + buscarEC[1] + ' EF:' + parametros[1] + ' TOKEN:' + buscarTOKEN[1])

                                        print("")
                                        print("El jugador '" + buscarAlias[1] + "' se ha cambiado correctamente el EF.")
                                        conn.send("El cambio de EF ha sido correcto.".encode(FORMAT))
                                        cambiadoEF = True
                                        
                                    else:
                                        f.write(line)    

                            if cambiadoEF == False:
                                conn.send("El cambio de EF ha sufrido un error. Introduzca los parámetros correctos.".encode(FORMAT))

                        elif parametros[2] == "c":
                            cambiadaContraseña = False

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

                                    if buscarAlias[1] == parametros[0] and buscarContraseña[1] == parametros[3]:
                                        buscarNivel = particion[2].split(":")
                                        buscarEC = particion[3].split(":")
                                        buscarEF = particion[4].split(":")
                                        buscarTOKEN = particion[5].split(":")

                                        f.write('ALIAS:' + buscarAlias[1] + ' CONTRASEÑA:' + parametros[1] + ' NIVEL:' + buscarNivel[1] + ' EC:' + buscarEC[1] + ' EF:' + buscarEF[1] + ' TOKEN:' + buscarTOKEN[1])

                                        print("")
                                        print("El jugador '" + buscarAlias[1] + "' se ha cambiado correctamente la contraseña.")
                                        conn.send("El cambio de contraseña ha sido correcto.".encode(FORMAT))
                                        cambiadaContraseña = True
                                        
                                    else:
                                        f.write(line)    

                            if cambiadaContraseña == False:
                                conn.send("El cambio de contraseña ha sufrido un error. Introduzca los parámetros correctos.".encode(FORMAT))
                        
                        else:
                            print("")
                            print("Ha ocurrido un error inesperado.")

                    else:
                        connected = True
            
            print("")
            print(f"Cerrada la conexión en: {addr} ")
            print("")
            conn.close()

        except:
            print("")
            print(f"Se ha forzado la conexión y ha terminado en: {addr} ")
            print("")
            conn.close()
        
    def start():
        server.listen()
        print("")
        print(f"[LISTENING] Registry a la escucha en {SERVER}")
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

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    start()

else:
    print ("Parece que algo falló. Necesito estos argumentos para el AA_Registry: <Puerto>")