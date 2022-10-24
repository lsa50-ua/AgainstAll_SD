import socket

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
            marcador = False
            for i in range(len(lineas)):
                separador =lineas[i].split(sep=':')
                if pet.decode() == separador[0]:
                    linea = lineas[i]
                    marcador = True
            if(marcador == True):
                conexion.send(linea.rstrip().encode('utf-8'))
            else:
                conexion.send("ERROR".encode('utf-8'))
    print("Finalizada conexion con el cliente")
    print("Servidor activo...")
    conexion.close()