from Posicion import *
import random
import msvcrt
from os import system     # Para limpiar el terminal

# Jugador -> representado por un elemento que indica su identidad y nivel
# NPC -> representado por un elemento que indica su nivel
class Mapa:
    def __init__(self):
        self.matriz = []

        # Crea la estructura de la matriz
        for i in range(20):
            self.matriz.append([0]*20)

        # Rellena la matriz
            # M -> mina
            # A -> alimento
            # "espacio" -> nada/vacío
        for i in range(20):
            for j in range(20):
                n = random.randint(0,10)
                if n == 3:
                    self.matriz[i][j] = 'M'
                elif n == 8:
                    self.matriz[i][j] = 'A'
                else:
                    self.matriz[i][j] = ' '
    
    def imprimir(self):
        print("#############################################AGAINST_ALL############################################")
        for i in self.matriz:
            print(i)
        print("####################################################################################################")
        print("")
    
    def setCeldaJugador(self,x,y):
        self.matriz[x][y] = 'J'     # Esto cambiarlo       

    def vaciarCelda(self,x,y):
        self.matriz[x][y] = ' '         
    
    def getCelda(self,x,y):
        return self.matriz[x][y]
    
    def limpiar(self):
        for i in range(20):
            for j in range(20):
                if mapa.getCelda(i,j) == 'J':
                    mapa.vaciarCelda(i,j)

system("cls")     # Limpiar la pantalla
mapa = Mapa()
posicion = Posicion()
mapa.setCeldaJugador(posicion.getX(),posicion.getY())
mapa.imprimir()

while True: 
    if msvcrt.kbhit():     
            msg = msvcrt.getch()

            if ord(msg) != 27:     # 27 es ESCAPE
                if ord(msg) == 119 or ord(msg) == 87:     # w-W -> ARRIBA
                    mapa.limpiar()

                    if posicion.getX()-1 < 0:     # Esto hace que si se pasa del borde aparezca por el otro lado del tablero
                        posicion.setX(19)
                    else:
                        posicion.addX(-1)
                    
                    mapa.setCeldaJugador(posicion.getX(),posicion.getY())
                    system("cls")         
                    mapa.imprimir()

                elif ord(msg) == 115 or ord(msg) == 83:     # s-S -> ABAJO
                    mapa.limpiar()

                    if posicion.getX()+1 > 19:
                        posicion.setX(0)
                    else:
                        posicion.addX(1)

                    mapa.setCeldaJugador(posicion.getX(),posicion.getY())
                    system("cls")
                    mapa.imprimir()
        
                elif ord(msg) == 97 or ord(msg) == 65:     # a-A -> IZQUIERDA
                    mapa.limpiar()

                    if posicion.getY()-1 < 0:
                        posicion.setY(19)
                    else:
                        posicion.addY(-1)

                    mapa.setCeldaJugador(posicion.getX(),posicion.getY())
                    system("cls")
                    mapa.imprimir()

                elif ord(msg) == 100 or ord(msg) == 68:      # d-D -> DERECHA
                    mapa.limpiar()

                    if posicion.getY()+1 > 19:
                        posicion.setY(0)
                    else:
                        posicion.addY(1)

                    mapa.setCeldaJugador(posicion.getX(),posicion.getY())
                    system("cls")
                    mapa.imprimir()

                elif ord(msg) == 101 or ord(msg) == 69:      # e-E -> ARRIBA-DERECHA
                    mapa.limpiar()

                    if posicion.getX()-1 < 0:
                        posicion.setX(19)
                        posicion.addY(1)

                    elif posicion.getY()+1 > 19:
                        posicion.addX(-1)
                        posicion.setY(0)

                    else:
                        posicion.addX(-1)
                        posicion.addY(1)

                    mapa.setCeldaJugador(posicion.getX(),posicion.getY())
                    system("cls")
                    mapa.imprimir()

                elif ord(msg) == 113 or ord(msg) == 81:      # q-Q -> ARRIBA-IZQUIERDA
                    mapa.limpiar()

                    if posicion.getX()-1 < 0:
                        posicion.setX(19)
                        posicion.addY(-1)

                    elif posicion.getY()-1 < 0:
                        posicion.addX(-1)
                        posicion.setY(19)

                    else:
                        posicion.addX(-1)
                        posicion.addY(-1)

                    mapa.setCeldaJugador(posicion.getX(),posicion.getY())
                    system("cls")
                    mapa.imprimir()
                
                elif ord(msg) == 122 or ord(msg) == 90:      # z-Z -> ABAJO-IZQUIERDA
                    mapa.limpiar()

                    if posicion.getX()+1 > 19:
                        posicion.setX(0)
                        posicion.addY(-1)

                    elif posicion.getY()-1 < 0:
                        posicion.addX(1)    
                        posicion.setY(19)
                    else:
                        posicion.addX(1)
                        posicion.addY(-1)

                    mapa.setCeldaJugador(posicion.getX(),posicion.getY())
                    system("cls")
                    mapa.imprimir()

                elif ord(msg) == 99 or ord(msg) == 67:      # c-C -> ABAJO-DERECHA
                    mapa.limpiar()

                    if posicion.getX()+1 > 19:
                        posicion.setX(0)
                        posicion.addY(1)

                    elif posicion.getY()+1 > 19:
                        posicion.addX(1)   
                        posicion.setY(0)

                    else:
                        posicion.addX(1)
                        posicion.addY(1)

                    mapa.setCeldaJugador(posicion.getX(),posicion.getY())
                    system("cls")
                    mapa.imprimir()

                else:
                    print("Pulsa una tecla correcta.")
            else:
                break