from Posicion import *
import random
import pygame

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
VERDE = ( 0, 255, 0)
ROJO = (255, 0, 0)
 
LARGO  = 20     # LARGO de cada celda de la retícula
ALTO = 20     # ALTO de cada celda de la retícula 
MARGEN = 5     # MARGEN entre las celdas
DIMENSION_VENTANA = [505,505]     # Establecemos el LARGO y ALTO de la pantalla

X = 0
Y = 0

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
                n = random.randint(0,15)
                if n == 7:
                    self.matriz[i][j] = 'M'
                elif n == 14:
                    self.matriz[i][j] = 'A'
                else:
                        self.matriz[i][j] = ' '
 
# Creamos un array bidimensional (una lista de listas)
tablero = []
for fila in range(20):
    # Añadimos un array vacío que contendrá cada celda en esta fila
    tablero.append([])
    for columna in range(20):
        tablero[fila].append(0) # Añade una celda

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
  
pygame.init()
pygame.display.set_caption("AGAINST ALL")     # Establecemos el título de la pantalla

pantalla = pygame.display.set_mode(DIMENSION_VENTANA)
 
reloj = pygame.time.Clock()     # Para establecer cuán rápido de refresca la pantalla

hecho = False     # Iteramos hasta que el usuario pulse el botón de salir
posicion = Posicion(X,Y)
tablero[posicion.getX()][posicion.getY()] = 1

# -------- Bucle Principal del Programa-----------
while not hecho:
    try:
        for evento in pygame.event.get(): 
            if evento.type == pygame.QUIT: 
                hecho = True

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    print("Key A has been pressed")
                    posicion.addX(-25)

                elif evento.key == pygame.K_w:
                    print("Key W has been pressed")
                    posicion.addY(-25)

                elif evento.key == pygame.K_s:
                    print("Key S has been pressed")
                    posicion.addY(25)

                elif evento.key == pygame.K_d:
                    print("Key D has been pressed")
                    posicion.addX(25)

                else:
                    print("Por favor pulse las teclas: A (Izquierda) W (Arriba) S (Abajo) D (Derecha)")

                # Cambia las coordenadas x/y de la pantalla por coordenadas reticulares
                columna = posicion.getX() // (LARGO + MARGEN)
                fila = posicion.getY() // (ALTO + MARGEN)

                for i in range(20):
                    for j in range(20):
                        if tablero[i][j] == 1:
                            tablero[i][j] = 0

                if tablero[fila][columna] == 'M':
                    print("Acabas de pisar una mina. Estas muerto.")
                
                if tablero[fila][columna] == 'A':
                    print("Acabas de comer un alimento. Subes de nivel.")

                tablero[fila][columna] = 1     # Poniendolo a 1 lo marcamos como negro. (Recuerda, los números de las filas y columnas empiezan en cero)
    except:
        print("")
        print("Por favor no pulses en el borde.")
        print("")
 
    pantalla.fill(NEGRO)         # Establecemos el color del fondo
 
    # Dibujamos la retícula
    for fila in range(20):
        for columna in range(20):
            color = BLANCO

            if tablero[fila][columna] == 1:
                color = NEGRO
            
            if tablero[fila][columna] == 'M':
                color = ROJO

            if tablero[fila][columna] == 'A':
                color = VERDE

            pygame.draw.rect(pantalla, color, [(MARGEN+LARGO) * columna + MARGEN, (MARGEN+ALTO) * fila + MARGEN, LARGO, ALTO])

    reloj.tick(60)     # Limitamos los fps
 
    pygame.display.flip()     # Avanzamos y actualizamos la pantalla con lo que hemos dibujado
     
pygame.quit()     # Cerramos