HOST = 'localhost'
PORT = 8010
#Se importa el módulo
import socket
 
#Creación de un objeto socket (lado cliente)
obj = socket.socket()
 
#Conexión con el servidor. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
obj.connect((HOST, PORT))
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
    print("El mapa esta compuesto por las siguientes ciudades: ")

    for i in range(len(lista_climas)):
        separados = lista_climas[i].split(sep=':')
        print(separados[0], separados[1], end="")
        print("ºC")
    
obj.close()

print("Conexión cerrada")