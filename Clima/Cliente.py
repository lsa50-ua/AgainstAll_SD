HOST = 'localhost'
PORT = 8010
#Se importa el módulo
import socket
 
#Creación de un objeto socket (lado cliente)
obj = socket.socket()
 
#Conexión con el servidor. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
obj.connect((HOST, PORT))
print("Conectado al servidor")
lista_climas = []
while len(lista_climas) != 4:
    #Con el método send, enviamos el mensaje
    obj.send("1".encode('utf-8'))

    #Cerramos la instancia del objeto servidor
    respuesta=obj.recv(4096)
    if len(lista_climas) == 0:
        lista_climas.append(respuesta.decode('utf-8'))
    else:
        repetido = False
        for i in range(len(lista_climas)):
            if lista_climas[i] == respuesta.decode('utf-8'):
                repetido = True

        if repetido == False:
            lista_climas.append(respuesta.decode('utf-8'))

obj.send("0".encode('utf-8'))

print(len(lista_climas))

for i in range(len(lista_climas)):
    separados = lista_climas[i].split(sep='/')
    print(separados[0], separados[1], end="")
    print("ºC")
obj.close()

print("Conexión cerrada")