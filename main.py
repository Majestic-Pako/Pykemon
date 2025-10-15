import pygame 
import pytmx
import sys
from core.entities.movement import manejar_movimiento
from core.entities.player import Player
from map import Mapa
from config import *

pygame.init() 

ventana_juego = pygame.display.set_mode((ANCHO, ALTO)) 
pygame.display.set_caption("Pykemon")

reloj = pygame.time.Clock()
player = Player(ANCHO, ALTO)
jugando = True
mapa = Mapa("assets/maps/test_map.tmx")

while jugando: 
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            jugando = False
    teclas = pygame.key.get_pressed()
    
    # Actualizar
    player.update(teclas)
    
    #Renderizado
    ventana_juego.fill(BLACK)
    mapa.dibujar(ventana_juego)
    player.dibujar(ventana_juego)
    pygame.display.flip()
    reloj.tick(FPS)
pygame.quit() 
sys.exit()

