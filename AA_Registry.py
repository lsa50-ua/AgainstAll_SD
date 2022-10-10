# recibe por parametro "puerto de escucha"
# La aplicación permanecerá a la espera hasta recibir una solicitud de registro de un jugador. 
# Los datos que puede guardar de un jugador son: alias, password, nivel, EF, EC

import socket 
import threading
from Jugador import * 

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
FIN = "FIN"

SERVER = socket.gethostbyname(socket.gethostname())     #Si imprimes la variable SERVER, imprime la ip del servidor
ADDR = (SERVER, PORT)
MAX_CONEXIONES = 5     #nº conexiones que puede conectar a la vez

def handle_client(conn, addr):
    #print(f"[NUEVA CONEXION] {addr} connected.")

    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == FIN:
                connected = False
            #print(f" He recibido del cliente [{addr}] el mensaje: {msg}")
            conn.send(f"Soy el servidor y he recibido tu mensaje: {msg} ".encode(FORMAT))
    #print("ADIOS. TE ESPERO EN OTRA OCASION")
    conn.close()
    
        

def start():
    server.listen()
    #print(f"[LISTENING] Servidor a la escucha en {SERVER}")
    CONEX_ACTIVAS = threading.active_count()-1
    #print(CONEX_ACTIVAS)

    while True:
        conn, addr = server.accept()
        CONEX_ACTIVAS = threading.active_count()

        if (CONEX_ACTIVAS <= MAX_CONEXIONES): 
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            #print(f"[CONEXIONES ACTIVAS] {CONEX_ACTIVAS}")
            #print("CONEXIONES RESTANTES PARA CERRAR EL SERVICIO", MAX_CONEXIONES-CONEX_ACTIVAS)
        else:
            #print("OOppsss... DEMASIADAS CONEXIONES. ESPERANDO A QUE ALGUIEN SE VAYA")
            conn.send("Demasiadas conexiones. Tendrás que esperar a que alguien se vaya".encode(FORMAT))
            conn.close()
            CONEX_ACTUALES = threading.active_count()-1
        
######################### MAIN ##########################

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
start()