import Jugador
import random

class Mapa:
    def __init__(self):
        self.matriz = []
        #crea la estructura de la matriz
        for i in range(20):
            self.matriz.append([0]*20)

        #rellena la matriz(M, A, ' ')
        for i in range(20):
            for j in range(20):
                n = random.randint(0,3)
                if n == 0:
                    self.matriz[i][j] = 'M'
                elif n == 1:
                    self.matriz[i][j] = 'A'
                else:
                        self.matriz[i][j] = ' '

    #imprime el mapa del juego
    def printMapa(self):
        for i in range(20):
            if i > 0:
                print()
            for j in range(20):
                print(self.matriz[i][j], ',', end=" ")


