from Jugador import *

MAXJUGADORES = 5

######################### MAIN ##########################

conexionesActivas = 0
seguir = True

while seguir:
    print("Bienvenido, selecciona que quieres hacer acontinuación: ")
    print("Nueva partida (1)")
    print("Salir (2)")
    seleccion = int(input())

    if seleccion == 1:
        conexionesActivas += 1
        #si se pulsa la opción, "comenzar partida" empieza el juego

        Jugador()

        if conexionesActivas == MAXJUGADORES:
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