import pygame 
import pytmx
import sys
from core.entities.movement import manejar_movimiento
from core.entities.player import Player
from map import Mapa
from config import *
from camera import Camera

pygame.init() 

ventana_juego = pygame.display.set_mode((ANCHO, ALTO)) 
pygame.display.set_caption("Pykemon")

reloj = pygame.time.Clock()
mapa = Mapa("assets/maps/test_map.tmx")
player = Player(ANCHO, ALTO, mapa.ancho, mapa.alto)
jugando = True
camera = Camera(mapa.ancho, mapa.alto, ANCHO, ALTO)

while jugando: 
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            jugando = False
    teclas = pygame.key.get_pressed()
    
    player.update(teclas)
    manejar_movimiento(player, teclas, mapa.colisiones)
    camera.update(player.rect)
    ventana_juego.fill(BLACK)
    mapa.dibujar(ventana_juego, camera)
    player.dibujar(ventana_juego, camera)
    pygame.display.flip()
    reloj.tick(FPS)
pygame.quit() 
sys.exit()

