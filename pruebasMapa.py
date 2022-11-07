from Posicion import *
import random

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
        for i in self.matriz:
            print(i)

mapa = Mapa()
mapa.imprimir()

""" tablero = []

# Colocamos de manera aleatroria las minas y la comida
for fila in range(20):
    for columna in range(20):
        n = random.randint(0,16)

        if n == 8:
            tablero[fila][columna] = 'M'
        elif n == 15:
            tablero[fila][columna] = 'A'
        else:
            tablero[fila][columna] = ' '

posicion = Posicion(1,1)
tablero[posicion.getX()][posicion.getY()] = 1

# -------- Bucle Principal del Programa-----------
for i in range(20):
    for j in range(20):
        if tablero[i][j] == 1:
            tablero[i][j] = ' '

if tablero[fila][columna] == 'M':
    print("Acabas de pisar una mina. Estas muerto.")

if tablero[fila][columna] == 'A':
    print("Acabas de comer un alimento. Subes de nivel.")

tablero[fila][columna] = 1     # Poniendolo a 1 lo marcamos como negro. (Recuerda, los números de las filas y columnas empiezan en cero) """