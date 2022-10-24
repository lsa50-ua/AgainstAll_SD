from Jugador import *
import sys


######################### MAIN ##########################

conexionesActivas = 0
seguir = True
if (len(sys.argv) == 4):

    while seguir:
        EnginePort = int(sys.argv[1])
        MAXjugadores = int(sys.argv[2])
        WeatherPort = int(sys.argv[3])
        print("Bienvenido, selecciona que quieres hacer acontinuación: ")
        print("Nueva partida (1)")
        print("Salir (2)")
        seleccion = int(input())

        if seleccion == 1:
            conexionesActivas += 1
            #si se pulsa la opción, "comenzar partida" empieza el juego

            Jugador()

            if conexionesActivas == MAXjugadores:
                #comienza la partida
                print("hello")
                
        elif seleccion == 2:
            seguir = False
        else:
            seguir = True



    #para pillar las teclas del jugador usamos en python, msvrct.getch()decode(FORMAT)
    # startime = time.time()
    # 
    # while True:
    #   msg = ""
    #   if  msvcrt SEGUIR CON LA FOTO DE LUIS