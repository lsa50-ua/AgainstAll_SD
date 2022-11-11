import random

class Mapa:
    def __init__(self):
        self.matriz = []
        self.climas = []
        self.ciudades = []

        # Crea la estructura de la matriz
        for i in range(20):
            self.matriz.append([0]*20)

        for i in range(20):
            for j in range(20):
                n = random.randint(0,10)
                if n == 3:
                    self.matriz[i][j] = 'M'     # M -> mina
                elif n == 8:
                    self.matriz[i][j] = 'A'     # A -> alimento
                else:
                    self.matriz[i][j] = ' '     # "espacio" -> nada/vacío
    
    def imprimir(self):
        if len(self.ciudades) == 0:     # Por si acaso, para que no pete
            print("#############################################AGAINST_ALL############################################")
            for i in self.matriz:
                print(i)
            print("####################################################################################################")
            print("")
        else:
            print("                    " + self.ciudades[0] + "                         " + "                    " + self.ciudades[1] + "                         ")
            print("                                                  "+"#"+"                                                  ")
            print("#############################################AGAINST_ALL############################################")
            for i in self.matriz:
                print(i)
            print("####################################################################################################")
            print("                                                  "+"#"+"                                                  ")
            print("                    " + self.ciudades[2] + "                         " + "                    " + self.ciudades[3] + "                         ")

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