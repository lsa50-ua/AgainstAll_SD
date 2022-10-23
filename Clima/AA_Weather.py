import socket
import random

HOST = 'localhost'
PORT = 8010

my_socket=socket.socket()
my_socket.bind((HOST, PORT))
my_socket.listen(5)

print ("Servidor a la escucha...")

while True:
    conexion, addr = my_socket.accept()
    print("Conexion con el cliente aceptada")

    while True:
        pet=conexion.recv(4096)
        if pet.decode() == "0":
            break
        else:
            fichero = open('BDClima.txt', 'r')
            lineas = fichero.readlines()
            n = random.randint(0, len(lineas) - 1)
            conexion.send(lineas[n].rstrip().encode('utf-8'))
    print("Finalizada conexion con el cliente")
    print("Servidor activo...")
    conexion.close()