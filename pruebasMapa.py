import random
from Posicion import *
from Jugador import *

class Mapa:
    def __init__(self):
        self.matriz = []
        self.climas = []
        self.ciudades = []
        self.jugadores = []

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
          
    def getCelda(self,x,y):
        return self.matriz[x][y]

    def getJugadores(self):
        return self.jugadores
    
    def Climas(self,climas):
        for i in range(len(climas)):
            self.climas.append(climas[i])     # El 0 será la zona arriba izquierda, el 1 será arriba derecha...
    
    def Ciudades(self,ciudades):
        for i in range(len(ciudades)):
            self.ciudades.append(ciudades[i])

    def Jugadores(self,jugadores):
        for i in range(len(jugadores)):
            yaEsta = False

            for j in range(len(self.jugadores)):
                if self.jugadores[j] == jugadores[i]:
                    yaEsta = True
            
            if yaEsta == False:
                self.jugadores.append(jugadores[i])

    def matarJugadores(self):
        posiciones  = []

        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerMuerto() == "MUERTO":
                posiciones.append(i)

        for posicion in posiciones:
            self.jugadores.pop(posicion)
            
    def matrizToString(self):
        cadena = ""
        for i in range(20):
            for j in range(20):
                if j == 19:
                    cadena += self.matriz[i][j]
                else:
                    cadena += self.matriz[i][j] + ","
            if i != 19:
                cadena += ";"
        return cadena

    def Mina(self,token,posicionNueva):
        self.limpiarJugador(token)
        self.matriz[posicionNueva.getX()][posicionNueva.getY()] = ' '

        for j in range(len(self.jugadores)):
            if token == self.jugadores[j].obtenerTOKEN():
                self.jugadores[j].Muerto()
    
    def Alimento(self,token,posicionNueva,posJugador):
        self.limpiarJugador(token)
        self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

        self.jugadores[posJugador].asignarPosicion(posicionNueva)

        for j in range(len(self.jugadores)):
            if token == self.jugadores[j].obtenerTOKEN():
                self.jugadores[j].aumentarNivel(1)
    
    def JugadorVSJugador(self,token,posicionNueva):
        for j in range(len(self.jugadores)):
            if self.jugadores[j].obtenerPosicion().getX() == posicionNueva.getX() and self.jugadores[j].obtenerPosicion().getY() == posicionNueva.getY():     # Jugador que esta en la posicion
                for x in range(len(self.jugadores)):
                    if token == self.jugadores[x].obtenerTOKEN():     # Jugador que quiere ir a la posición

                        if self.jugadores[x].obtenerNivel() < self.jugadores[j].obtenerNivel():     # Gana el que ya estaba en la posición
                            self.limpiarJugador(token)
                            self.jugadores[x].Muerto()

                        if self.jugadores[x].obtenerNivel() > self.jugadores[j].obtenerNivel():     # Gana el que quiere ir a la posición
                            self.limpiarJugador(self.jugadores[j].obtenerTOKEN())
                            self.limpiarJugador(token)
                            self.jugadores[j].Muerto()

                            self.jugadores[x].asignarPosicion(posicionNueva)
                            self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

    def incorporarJugador(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:
                if self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] == ' ':
                    self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'     # Mirar como identificar en el mapa a los jugadores                           ##### IMPORTANTE #####
                else:
                    while 1:
                        nuevaPosicion = Posicion(random.randint(0,19),random.randint(0,19))

                        if self.matriz[nuevaPosicion.getX()][nuevaPosicion.getY()] == ' ':
                            self.jugadores[i].asignarPosicion(nuevaPosicion)
                            self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'     # Mirar como identificar en el mapa a los jugadores                   ##### IMPORTANTE #####
                            break

    def limpiarJugador(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:
                self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = ' '    

    def moduloW(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.jugadores[i].obtenerPosicion().getX(),self.jugadores[i].obtenerPosicion().getY())

                if posicionNueva.getX()-1 < 0:     
                        posicionNueva.setX(19)
                else:
                    posicionNueva.addX(-1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'M':
                    self.Mina(token,posicionNueva)
                
                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'A':
                    self.Alimento(token,posicionNueva,i)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                      

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

    def moduloS(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.jugadores[i].obtenerPosicion().getX(),self.jugadores[i].obtenerPosicion().getY())

                if posicionNueva.getX()+1 > 19:     
                        posicionNueva.setX(0)
                else:
                    posicionNueva.addX(1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'M':
                    self.Mina(token,posicionNueva)
                
                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'A':
                    self.Alimento(token,posicionNueva,i)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                         

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

    def moduloA(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.jugadores[i].obtenerPosicion().getX(),self.jugadores[i].obtenerPosicion().getY())

                if posicionNueva.getY()-1 < 0:     
                        posicionNueva.setY(19)
                else:
                    posicionNueva.addY(-1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'M':
                    self.Mina(token,posicionNueva)
                
                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'A':
                    self.Alimento(token,posicionNueva,i)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

    def moduloD(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.jugadores[i].obtenerPosicion().getX(),self.jugadores[i].obtenerPosicion().getY())

                if posicionNueva.getY()+1 > 19:     
                        posicionNueva.setY(0)
                else:
                    posicionNueva.addY(1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'M':
                    self.Mina(token,posicionNueva)
                
                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'A':
                    self.Alimento(token,posicionNueva,i)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

    def moduloE(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.jugadores[i].obtenerPosicion().getX(),self.jugadores[i].obtenerPosicion().getY())

                if posicionNueva.getX()-1 < 0: 
                    posicionNueva.setX(19)
                    posicionNueva.addY(1)    

                elif posicionNueva.getY()+1 > 19:
                    posicionNueva.setY(0)    
                    posicionNueva.addX(-1)

                else:
                    posicionNueva.addY(1)
                    posicionNueva.addX(-1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'M':
                    self.Mina(token,posicionNueva)
                
                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'A':
                    self.Alimento(token,posicionNueva,i)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

    def moduloQ(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.jugadores[i].obtenerPosicion().getX(),self.jugadores[i].obtenerPosicion().getY())

                if posicionNueva.getX()-1 < 0: 
                    posicionNueva.setX(19)
                    posicionNueva.addY(-1)    

                elif posicionNueva.getY()-1 < 0:
                    posicionNueva.setY(19)    
                    posicionNueva.addX(-1)

                else:
                    posicionNueva.addY(-1)
                    posicionNueva.addX(-1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'M':
                    self.Mina(token,posicionNueva)
                
                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'A':
                    self.Alimento(token,posicionNueva,i)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

    def moduloZ(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.jugadores[i].obtenerPosicion().getX(),self.jugadores[i].obtenerPosicion().getY())

                if posicionNueva.getX()+1 > 19: 
                    posicionNueva.setX(0)
                    posicionNueva.addY(-1)    

                elif posicionNueva.getY()-1 < 0:
                    posicionNueva.setY(19)    
                    posicionNueva.addX(1)

                else:
                    posicionNueva.addY(-1)
                    posicionNueva.addX(1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'M':
                    self.Mina(token,posicionNueva)
                
                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'A':
                    self.Alimento(token,posicionNueva,i)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

    def moduloC(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.jugadores[i].obtenerPosicion().getX(),self.jugadores[i].obtenerPosicion().getY())

                if posicionNueva.getX()+1 > 19: 
                    posicionNueva.setX(0)
                    posicionNueva.addY(1)    

                elif posicionNueva.getY()+1 > 19:
                    posicionNueva.setY(0)    
                    posicionNueva.addX(1)

                else:
                    posicionNueva.addY(1)
                    posicionNueva.addX(1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'M':
                    self.Mina(token,posicionNueva)
                
                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'A':
                    self.Alimento(token,posicionNueva,i)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'


""" game = Mapa()
jugador1 = Jugador()
jugador2 = Jugador()
jugadores = []
jugadores.append(jugador1)
jugadores.append(jugador2)
game.Jugadores(jugadores)
print(jugador1.obtenerMuerto())
jugador1.asignarTOKEN("1856")
print(jugador1.obtenerTOKEN())
game.Mina(jugador1.obtenerTOKEN(),Posicion(10,10))
print(jugador1.obtenerMuerto()) """