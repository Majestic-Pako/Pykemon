import pygame 
import pytmx
import sys
from core.entities.movement import manejar_movimiento
from core.entities.player import Player
from core.system.map import Mapa
from core.system.config import *
from core.system.camera import Camera

pygame.init() 

ventana_juego = pygame.display.set_mode((ANCHO, ALTO)) 
pygame.display.set_caption("Pykemon")

reloj = pygame.time.Clock()
mapa = Mapa("assets/maps/test_map.tmx")
player = Player(ANCHO, ALTO, mapa.ancho, mapa.alto)
jugando = True
camera = Camera(mapa.ancho, mapa.alto, ANCHO, ALTO)
frame_count = 0

while jugando: 
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            jugando = False
    teclas = pygame.key.get_pressed()
    
    if player.puede_moverse():
        player.update(teclas)
        manejar_movimiento(player, teclas, mapa.colisiones, mapa.npcs)
        camera.update(player.rect)
    player.manejar_dialogo(teclas, mapa.npcs)
    # testeo pa saber si entra en combate
    frame_count += 1
    if frame_count % 30 == 0:
        if not player.dialogo_box.activo:
            player.testear_combate(mapa.zonas_combate)
    ventana_juego.fill(BLACK)
    mapa.dibujar(ventana_juego, camera)
    player.dibujar(ventana_juego, camera)

    pygame.display.flip()
    reloj.tick(FPS)
pygame.quit() 
sys.exit()

