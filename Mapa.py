import random
from Posicion import *
from Jugador import *
from NPC import *

class Mapa:
    def __init__(self):
        self.matriz = []
        self.climas = []
        self.ciudades = []
        self.jugadores = []
        self.NPCs = []

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
    
    def getNPCs(self):
        return self.NPCs
    
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

    def añadirNPC(self, NPC):
        self.NPCs.append(NPC)

    def matarJugadores(self): 
        posiciones  = []
        listaMsgMuertos = []
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerMuerto() == "MUERTO":
                posiciones.append(i)

        for posicion in posiciones:
            listaMsgMuertos.append(self.jugadores[posicion].obtenerTOKEN() + ":FIN")
            self.jugadores.pop(posicion)

        return listaMsgMuertos

    def matarNPCs(self): 
        posiciones  = []
        listaMsgMuertos = []
        for i in range(len(self.NPCs)):
            if self.NPCs[i].vivoOmuerto() == True:
                posiciones.append(i)

        for posicion in posiciones:
            listaMsgMuertos.append(self.NPCs[posicion].obtenerTOKEN() + "-FIN")
            self.NPCs.pop(posicion)

        return listaMsgMuertos
            
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

    def infoPlayers(self):
        info = "INFOP:"
        for i in range(len(self.jugadores)):
            info = info + "Jugador " + self.jugadores[i].getAlias() + " Posicion(" + str(self.jugadores[i].obtenerPosicion().getY()) + "," + str(self.jugadores[i].obtenerPosicion().getX()) + ") Nivel-> " + str(self.jugadores[i].obtenerNivel()) + " Zona -> "
            if self.jugadores[i].getCiudad() == "ARRIBA-IZQUIERDA":
                info = info +  self.jugadores[i].getCiudad() + " Ciudad -> "+self.ciudades[0] + " Clima -> " + self.climas[0] + " ºC"
            elif self.jugadores[i].getCiudad() == "ARRIBA-DERECHA":
                info = info +  self.jugadores[i].getCiudad() + " Ciudad -> "+self.ciudades[1] + " Clima -> " + self.climas[1] + " ºC"
            elif self.jugadores[i].getCiudad() == "ABAJO-IZQUIERDA":
                info = info +  self.jugadores[i].getCiudad() + " Ciudad -> "+self.ciudades[2] + " Clima -> " + self.climas[2] + " ºC"
            elif self.jugadores[i].getCiudad() == "ABAJO-DERECHA":
                info = info +  self.jugadores[i].getCiudad() + " Ciudad -> "+self.ciudades[3] + " Clima -> " + self.climas[3] + " ºC"
            
            if i < (len(self.jugadores) - 1):
                info = info + ";"
        return info

    def Mina(self,token,posicionNueva):
        self.limpiarJugador(token)
        self.matriz[posicionNueva.getX()][posicionNueva.getY()] = ' '

        for j in range(len(self.jugadores)):
            if token == self.jugadores[j].obtenerTOKEN():
                self.jugadores[j].Muerto()
    
    def Alimento(self,token,posicionNueva):
        self.limpiarJugador(token)
        self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

        for j in range(len(self.jugadores)):
            if token == self.jugadores[j].obtenerTOKEN():
                self.jugadores[j].asignarPosicion(posicionNueva)
                self.jugadores[j].aumentarNivel(1)

        self.comprobarClima(posicionNueva,token)
    
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

                            self.comprobarClima(posicionNueva,token)

    def NPCVSJugador(self,tokenNPC,posicionNueva):
        for j in range(len(self.jugadores)):
            if self.jugadores[j].obtenerPosicion().getX() == posicionNueva.getX() and self.jugadores[j].obtenerPosicion().getY() == posicionNueva.getY():     # Jugador que esta en la posicion
                for x in range(len(self.NPCs)):
                    if tokenNPC == self.NPCs[x].obtenerTOKEN():     # Jugador que quiere ir a la posición

                        if self.NPCs[x].obtenerNivel() < self.jugadores[j].obtenerNivel():     # Gana el que ya estaba en la posición
                            self.limpiarNPC(tokenNPC)
                            self.NPCs[x].matar()


                        if self.NPCs[x].obtenerNivel() > self.jugadores[j].obtenerNivel():     # Gana el que quiere ir a la posición
                            self.limpiarJugador(self.jugadores[j].obtenerTOKEN())
                            self.limpiarNPC(tokenNPC)
                            self.jugadores[j].Muerto()

                            self.NPCs[x].asignarPosicion(posicionNueva)
                            self.matriz[posicionNueva.getX()][posicionNueva.getY()] = self.NPCs[x].obtenerNivel_Char()
                     
    def JugadorVSNPC(self,token,posicionNueva):
        for j in range(len(self.NPCs)):
            if self.NPCs[j].obtenerPosicion().getX() == posicionNueva.getX() and self.NPCs[j].obtenerPosicion().getY() == posicionNueva.getY():     # Jugador que esta en la posicion
                for x in range(len(self.jugadores)):
                    if token == self.jugadores[x].obtenerTOKEN():     # Jugador que quiere ir a la posición

                        if self.jugadores[x].obtenerNivel() < self.NPCs[j].obtenerNivel():     # Gana el que ya estaba en la posición
                            self.limpiarJugador(token)
                            self.jugadores[x].Muerto()

                        if self.jugadores[x].obtenerNivel() > self.NPCs[j].obtenerNivel():     # Gana el que quiere ir a la posición
                            self.limpiarNPC(self.NPCs[j].obtenerTOKEN())
                            self.limpiarJugador(token)
                            self.NPCs[j].matar()

                            self.jugadores[x].asignarPosicion(posicionNueva)
                            self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'

                            self.comprobarClima(posicionNueva,token)

    def NPCVSNPC(self,token,posicionNueva):
        for j in range(len(self.NPCs)):
            if self.NPCs[j].obtenerPosicion().getX() == posicionNueva.getX() and self.NPCs[j].obtenerPosicion().getY() == posicionNueva.getY():     # Jugador que esta en la posicion
                for x in range(len(self.NPCs)):
                    if token == self.NPCs[x].obtenerTOKEN():     # Jugador que quiere ir a la posición

                        if self.NPCs[x].obtenerNivel() < self.NPCs[j].obtenerNivel():     # Gana el que ya estaba en la posición
                            self.limpiarNPC(token)
                            self.NPCs[x].matar()

                        if self.NPCs[x].obtenerNivel() > self.NPCs[j].obtenerNivel():     # Gana el que quiere ir a la posición
                            self.limpiarNPC(self.NPCs[j].obtenerTOKEN())
                            self.limpiarNPC(token)
                            self.NPCs[j].matar()

                            self.NPCs[x].asignarPosicion(posicionNueva)
                            self.matriz[posicionNueva.getX()][posicionNueva.getY()] = self.NPCs[x].obtenerNivel_Char()


    def comprobarClima(self,posicion,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:
                if self.jugadores[i].getCiudad() == "Ninguna":     # Para cuando se colocan en el tablero por primera vez
                    if posicion.getX() < 10 and posicion.getY() < 10:     # Ciudad ARRIBA-IZQUIERDA
                        frio = False
                        calor = False

                        if int(self.climas[0]) <= 10:
                            frio = True
                        if int(self.climas[0]) >= 25:
                            calor = True

                        if frio:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEF())
                        if calor:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEC())

                        self.jugadores[i].setCiudad("ARRIBA-IZQUIERDA")

                    elif (posicion.getY() >= 10 and posicion.getY() < 20) and posicion.getX() < 10:     # Ciudad ARRIBA-DERECHA
                        frio = False
                        calor = False

                        if int(self.climas[1]) <= 10:
                            frio = True
                        if int(self.climas[1]) >= 25:
                            calor = True

                        if frio:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEF())
                        if calor:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEC())

                        self.jugadores[i].setCiudad("ARRIBA-DERECHA")
                    
                    elif (posicion.getX() >= 10 and posicion.getX() < 20) and posicion.getY() < 10:     # Ciudad ABAJO-IZQUIERDA
                        frio = False
                        calor = False

                        if int(self.climas[2]) <= 10:
                            frio = True
                        if int(self.climas[2]) >= 25:
                            calor = True

                        if frio:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEF())
                        if calor:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEC())

                        self.jugadores[i].setCiudad("ABAJO-IZQUIERDA")
                    
                    else:     # Ciudad ABAJO-DERECHA
                        frio = False
                        calor = False

                        if int(self.climas[3]) <= 10:
                            frio = True
                        if int(self.climas[3]) >= 25:
                            calor = True

                        if frio:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEF())
                        if calor:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEC())

                        self.jugadores[i].setCiudad("ABAJO-DERECHA")

                else:     # Cuando pasa de ciudad a otra (o no, si no se mete en ninugn if)
                    if posicion.getX() < 10 and posicion.getY() < 10 and self.jugadores[i].getCiudad() != "ARRIBA-IZQUIERDA":     # Ciudad ARRIBA-IZQUIERDA
                        frio = False
                        calor = False

                        if int(self.climas[0]) <= 10:
                            frio = True
                        if int(self.climas[0]) >= 25:
                            calor = True

                        if frio:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEF())
                        if calor:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEC())

                        self.jugadores[i].setCiudad("ARRIBA-IZQUIERDA")

                    if (posicion.getY() >= 10 and posicion.getY() < 20) and posicion.getX() < 10 and self.jugadores[i].getCiudad() != "ARRIBA-DERECHA":     # Ciudad ARRIBA-DERECHA
                        frio = False
                        calor = False

                        if int(self.climas[1]) <= 10:
                            frio = True
                        if int(self.climas[1]) >= 25:
                            calor = True

                        if frio:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEF())
                        if calor:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEC())

                        self.jugadores[i].setCiudad("ARRIBA-DERECHA")
                    
                    if (posicion.getX() >= 10 and posicion.getX() < 20) and posicion.getY() < 10 and self.jugadores[i].getCiudad() != "ABAJO-IZQUIERDA":     # Ciudad ABAJO-IZQUIERDA
                        frio = False
                        calor = False

                        if int(self.climas[2]) <= 10:
                            frio = True
                        if int(self.climas[2]) >= 25:
                            calor = True

                        if frio:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEF())
                        if calor:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEC())

                        self.jugadores[i].setCiudad("ABAJO-IZQUIERDA")
                    
                    if (posicion.getX() >= 10 and posicion.getX() < 20) and (posicion.getY() >= 10 and posicion.getY() < 20) and self.jugadores[i].getCiudad() != "ABAJO-DERECHA":     # Ciudad ABAJO-DERECHA
                        frio = False
                        calor = False

                        if int(self.climas[3]) <= 10:
                            frio = True
                        if int(self.climas[3]) >= 25:
                            calor = True

                        if frio:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEF())
                        if calor:
                            self.jugadores[i].aumentarNivel(self.jugadores[i].obtenerEC())

                        self.jugadores[i].setCiudad("ABAJO-DERECHA")

    def incorporarJugador(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:
                if self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] == ' ':
                    self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'     # Mirar como identificar en el mapa a los jugadores

                    self.comprobarClima(Posicion(self.jugadores[i].obtenerPosicion().getX(),self.jugadores[i].obtenerPosicion().getY()),token)

                else:
                    while 1:
                        nuevaPosicion = Posicion(random.randint(0,19),random.randint(0,19))

                        if self.matriz[nuevaPosicion.getX()][nuevaPosicion.getY()] == ' ':
                            self.jugadores[i].asignarPosicion(nuevaPosicion)
                            self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = 'J'     # Mirar como identificar en el mapa a los jugadores

                            self.comprobarClima(nuevaPosicion,token)

                            break

    def incorporarNPC(self,token):
        for i in range(len(self.NPCs)):
            if self.NPCs[i].obtenerTOKEN() == token:
                if self.matriz[self.NPCs[i].obtenerPosicion().getX()][self.NPCs[i].obtenerPosicion().getY()] == ' ':
                    self.matriz[self.NPCs[i].obtenerPosicion().getX()][self.NPCs[i].obtenerPosicion().getY()] = self.NPCs[i].obtenerNivel_Char()    # Mirar como identificar en el mapa a los jugadores
                else:
                    while 1:
                        nuevaPosicion = Posicion(random.randint(0,19),random.randint(0,19))

                        if self.matriz[nuevaPosicion.getX()][nuevaPosicion.getY()] == ' ':
                            self.NPCs[i].asignarPosicion(nuevaPosicion)
                            self.matriz[self.NPCs[i].obtenerPosicion().getX()][self.NPCs[i].obtenerPosicion().getY()] = self.NPCs[i].obtenerNivel_Char()    # Mirar como identificar en el mapa a los jugadores
                            break        

    def limpiarJugador(self,token):
        for i in range(len(self.jugadores)):
            if self.jugadores[i].obtenerTOKEN() == token:
                self.matriz[self.jugadores[i].obtenerPosicion().getX()][self.jugadores[i].obtenerPosicion().getY()] = ' '  

    def limpiarNPC(self,token):
        for i in range(len(self.NPCs)):
            if self.NPCs[i].obtenerTOKEN() == token:
                self.matriz[self.NPCs[i].obtenerPosicion().getX()][self.NPCs[i].obtenerPosicion().getY()] = ' '     

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
                    self.Alimento(token,posicionNueva)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva) 

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.JugadorVSNPC(token, posicionNueva)                 

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'
                    self.comprobarClima(posicionNueva,token)

    def moduloW_N(self,token):
        for i in range(len(self.NPCs)):
            if self.NPCs[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.NPCs[i].obtenerPosicion().getX(),self.NPCs[i].obtenerPosicion().getY())

                if posicionNueva.getX()-1 < 0:     
                        posicionNueva.setX(19)
                else:
                    posicionNueva.addX(-1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.NPCVSJugador(token,posicionNueva)

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.NPCVSNPC(token, posicionNueva)                      
                else:
                    self.limpiarNPC(token)
                    self.NPCs[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = self.NPCs[i].obtenerNivel_Char()

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
                    self.Alimento(token,posicionNueva)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)           

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.JugadorVSNPC(token, posicionNueva) 

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'
                    self.comprobarClima(posicionNueva,token)

    def moduloS_N(self,token):
        for i in range(len(self.NPCs)):
            if self.NPCs[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.NPCs[i].obtenerPosicion().getX(),self.NPCs[i].obtenerPosicion().getY())

                if posicionNueva.getX()+1 > 19:     
                        posicionNueva.setX(0)
                else:
                    posicionNueva.addX(1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.NPCVSJugador(token,posicionNueva) 

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.NPCVSNPC(token, posicionNueva) 
                else:
                    self.limpiarNPC(token)
                    self.NPCs[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = self.NPCs[i].obtenerNivel_Char()


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
                    self.Alimento(token,posicionNueva)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.JugadorVSNPC(token, posicionNueva) 

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'
                    self.comprobarClima(posicionNueva,token)

    def moduloA_N(self,token):
        for i in range(len(self.NPCs)):
            if self.NPCs[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.NPCs[i].obtenerPosicion().getX(),self.NPCs[i].obtenerPosicion().getY())

                if posicionNueva.getY()-1 < 0:     
                        posicionNueva.setY(19)
                else:
                    posicionNueva.addY(-1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.NPCVSJugador(token,posicionNueva)    

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.NPCVSNPC(token, posicionNueva) 
                
                else:
                    self.limpiarNPC(token)
                    self.NPCs[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = self.NPCs[i].obtenerNivel_Char()


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
                    self.Alimento(token,posicionNueva)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.JugadorVSNPC(token, posicionNueva) 

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'
                    self.comprobarClima(posicionNueva,token)

    def moduloD_N(self,token):
        for i in range(len(self.NPCs)):
            if self.NPCs[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.NPCs[i].obtenerPosicion().getX(),self.NPCs[i].obtenerPosicion().getY())

                if posicionNueva.getY()+1 > 19:     
                        posicionNueva.setY(0)
                else:
                    posicionNueva.addY(1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.NPCVSJugador(token,posicionNueva)   

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.NPCVSNPC(token, posicionNueva) 

                else:
                    self.limpiarNPC(token)
                    self.NPCs[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = self.NPCs[i].obtenerNivel_Char()


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
                    self.Alimento(token,posicionNueva)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.JugadorVSNPC(token, posicionNueva) 

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'
                    self.comprobarClima(posicionNueva,token)

    def moduloE_N(self,token):
        for i in range(len(self.NPCs)):
            if self.NPCs[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.NPCs[i].obtenerPosicion().getX(),self.NPCs[i].obtenerPosicion().getY())

                if posicionNueva.getX()-1 < 0: 
                    posicionNueva.setX(19)
                    posicionNueva.addY(1)    

                elif posicionNueva.getY()+1 > 19:
                    posicionNueva.setY(0)    
                    posicionNueva.addX(-1)

                else:
                    posicionNueva.addY(1)
                    posicionNueva.addX(-1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.NPCVSJugador(token,posicionNueva)

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.NPCVSNPC(token, posicionNueva) 

                else:
                    self.limpiarNPC(token)
                    self.NPCs[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = self.NPCs[i].obtenerNivel_Char()


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
                    self.Alimento(token,posicionNueva)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.JugadorVSNPC(token, posicionNueva) 

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'
                    self.comprobarClima(posicionNueva,token)

    def moduloQ_N(self,token):
        for i in range(len(self.NPCs)):
            if self.NPCs[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.NPCs[i].obtenerPosicion().getX(),self.NPCs[i].obtenerPosicion().getY())

                if posicionNueva.getX()-1 < 0: 
                    posicionNueva.setX(19)
                    posicionNueva.addY(-1)    

                elif posicionNueva.getY()-1 < 0:
                    posicionNueva.setY(19)    
                    posicionNueva.addX(-1)

                else:
                    posicionNueva.addY(-1)
                    posicionNueva.addX(-1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.NPCVSJugador(token,posicionNueva)

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.NPCVSNPC(token, posicionNueva)     

                else:
                    self.limpiarNPC(token)
                    self.NPCs[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = self.NPCs[i].obtenerNivel_Char()


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
                    self.Alimento(token,posicionNueva)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.JugadorVSNPC(token, posicionNueva) 

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'
                    self.comprobarClima(posicionNueva,token)

    def moduloZ_N(self,token):
        for i in range(len(self.NPCs)):
            if self.NPCs[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.NPCs[i].obtenerPosicion().getX(),self.NPCs[i].obtenerPosicion().getY())

                if posicionNueva.getX()+1 > 19: 
                    posicionNueva.setX(0)
                    posicionNueva.addY(-1)    

                elif posicionNueva.getY()-1 < 0:
                    posicionNueva.setY(19)    
                    posicionNueva.addX(1)

                else:
                    posicionNueva.addY(-1)
                    posicionNueva.addX(1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.NPCVSJugador(token,posicionNueva) 

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.NPCVSNPC(token, posicionNueva) 

                else:
                    self.limpiarNPC(token)
                    self.NPCs[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = self.NPCs[i].obtenerNivel_Char()


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
                    self.Alimento(token,posicionNueva)

                elif self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.JugadorVSJugador(token,posicionNueva)                                      

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.JugadorVSNPC(token, posicionNueva) 

                else:
                    self.limpiarJugador(token)
                    self.jugadores[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = 'J'
                    self.comprobarClima(posicionNueva,token)

    def moduloC_N(self,token):
        for i in range(len(self.NPCs)):
            if self.NPCs[i].obtenerTOKEN() == token:

                posicionNueva = Posicion(self.NPCs[i].obtenerPosicion().getX(),self.NPCs[i].obtenerPosicion().getY())

                if posicionNueva.getX()+1 > 19: 
                    posicionNueva.setX(0)
                    posicionNueva.addY(1)    

                elif posicionNueva.getY()+1 > 19:
                    posicionNueva.setY(0)    
                    posicionNueva.addX(1)

                else:
                    posicionNueva.addY(1)
                    posicionNueva.addX(1)

                if self.matriz[posicionNueva.getX()][posicionNueva.getY()] == 'J':
                    self.NPCVSJugador(token,posicionNueva)

                elif (self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '1' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '2' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '3'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '4' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '5' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '6'
                or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '7' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '8' or self.matriz[posicionNueva.getX()][posicionNueva.getY()] == '9'):
                    
                    self.NPCVSNPC(token, posicionNueva) 

                else:
                    self.limpiarNPC(token)
                    self.NPCs[i].asignarPosicion(posicionNueva)
                    self.matriz[posicionNueva.getX()][posicionNueva.getY()] = self.NPCs[i].obtenerNivel_Char()