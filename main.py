import pygame 
import sys
pygame.init() 

ancho = 700
alto = 550
ventana_juego = pygame.display.set_mode((ancho, alto)) 
pygame.display.set_caption("Pykemon")

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

cuadrado_tamano = 32
cuadrado_x = ancho // 2 - cuadrado_tamano // 2
cuadrado_y = alto // 2 - cuadrado_tamano // 2
velocidad = 4

reloj = pygame.time.Clock()
jugando = True

while jugando == True : 
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            jugando = False

    cuadrado_x = max(0, min(cuadrado_x, ancho - cuadrado_tamano))
    cuadrado_y = max(0, min(cuadrado_y, alto - cuadrado_tamano))

    ventana_juego.fill(black)  
    pygame.draw.rect(ventana_juego, red, (cuadrado_x, cuadrado_y, cuadrado_tamano, cuadrado_tamano))

    pygame.display.flip()

    reloj.tick(30)

pygame.quit() 
sys.exit()

