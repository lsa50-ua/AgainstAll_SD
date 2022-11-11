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
                    self.limpiarJugador(token)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = ' '

                    for j in range(len(self.jugadores)):
                        if token == self.jugadores[j].obtenerTOKEN():
                            self.jugadores.pop(j)
                
                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'A':
                    self.limpiarJugador(token)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

                    self.jugadores[i].asignarPosicion(posicionNueva)

                    for j in range(len(self.jugadores)):
                        if token == self.jugadores[j].obtenerTOKEN():
                            self.jugadores[j].aumentarNivel(1)

                #elif self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] == 'J':
                    ######## SEGUIR

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

    def moduloS(self,token):
        self.limpiarJugador(token)

        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                if self.jugadores[i].obtenerPosicion().getX()+1 > 19:     
                        self.jugadores[i].asignarPosicionX(0)
                else:
                    self.jugadores[i].añadirPosicionX(1)
                    
                self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'
    
    def moduloA(self,token):
        self.limpiarJugador(token)

        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                if self.jugadores[i].obtenerPosicion().getY()-1 < 0:     
                        self.jugadores[i].asignarPosicionY(19)
                else:
                    self.jugadores[i].añadirPosicionY(-1)
                    
                self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'

    def moduloD(self,token):
        self.limpiarJugador(token)

        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                if self.jugadores[i].obtenerPosicion().getY()+1 > 19:     
                        self.jugadores[i].asignarPosicionY(0)
                else:
                    self.jugadores[i].añadirPosicionY(1)
                    
                self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'

    def moduloE(self,token):
        self.limpiarJugador(token)

        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                if self.jugadores[i].obtenerPosicion().getX()-1 < 0:     
                        self.jugadores[i].asignarPosicionX(19)
                        self.jugadores[i].añadirPosicionY(1)

                elif self.jugadores[i].obtenerPosicion().getY()+1 > 19:     
                        self.jugadores[i].asignarPosicionY(0)
                        self.jugadores[i].añadirPosicionX(-1)

                else:
                    self.jugadores[i].añadirPosicionY(1)
                    self.jugadores[i].añadirPosicionX(-1)
                    
                self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'

    def moduloQ(self,token):
        self.limpiarJugador(token)

        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                if self.jugadores[i].obtenerPosicion().getX()-1 < 0:     
                        self.jugadores[i].asignarPosicionX(19)
                        self.jugadores[i].añadirPosicionY(-1)

                elif self.jugadores[i].obtenerPosicion().getY()-1 < 0:     
                        self.jugadores[i].asignarPosicionY(19)
                        self.jugadores[i].añadirPosicionX(-1)

                else:
                    self.jugadores[i].añadirPosicionY(-1)
                    self.jugadores[i].añadirPosicionX(-1)
                    
                self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'

    def moduloZ(self,token):
        self.limpiarJugador(token)

        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                if self.jugadores[i].obtenerPosicion().getX()+1 > 19:     
                        self.jugadores[i].asignarPosicionX(0)
                        self.jugadores[i].añadirPosicionY(-1)

                elif self.jugadores[i].obtenerPosicion().getY()-1 < 0:     
                        self.jugadores[i].asignarPosicionY(19)
                        self.jugadores[i].añadirPosicionX(1)

                else:
                    self.jugadores[i].añadirPosicionY(-1)
                    self.jugadores[i].añadirPosicionX(1)
                    
                self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'

    def moduloC(self,token):
        self.limpiarJugador(token)

        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:

                if self.jugadores[i].obtenerPosicion().getX()+1 > 19:     
                        self.jugadores[i].asignarPosicionX(0)
                        self.jugadores[i].añadirPosicionY(1)

                elif self.jugadores[i].obtenerPosicion().getY()+1 > 19:     
                        self.jugadores[i].asignarPosicionY(0)
                        self.jugadores[i].añadirPosicionX(1)

                else:
                    self.jugadores[i].añadirPosicionY(1)
                    self.jugadores[i].añadirPosicionX(1)
                    
                self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'


""" game = Mapa()
jugador1 = Jugador()
jugador2 = Jugador()
jugador1.asignarTOKEN("198")
jugador2.asignarTOKEN("9848")

jugadores = []

jugadores.append(jugador1)
jugadores.append(jugador2)

game.Jugadores(jugadores)

game.imprimir()

game.incorporarJugador("198")

game.imprimir()

game.incorporarJugador("9848")

game.imprimir() """



""" system("cls")     # Limpiar la pantalla
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
                break """