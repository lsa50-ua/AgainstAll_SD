import random

class Mapa:
    def __init__(self):
        self.matriz = []
        self.climas = []
        self.ciudades = []

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
                if self.matriz.getCelda(i,j) == 'J':
                    self.matriz.vaciarCelda(i,j)
    
    def Climas(self,climas):
        for i in range(len(climas)):
            self.climas.append(climas[i])     # El 0 será la zona arriba izquierda, el 1 será arriba derecha...
    
    def Ciudades(self,ciudades):
        for i in range(len(ciudades)):
            self.ciudades.append(ciudades[i])
