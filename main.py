import pygame 
import pytmx
import sys
from core.entities.movement import manejar_movimiento
from core.entities.player import Player
from core.system.map import Mapa
from core.system.config import *
from core.system.camera import Camera
from core.system.MenuManager import MenuManager

pygame.init() 

ventana_juego = pygame.display.set_mode((ANCHO, ALTO)) 
pygame.display.set_caption("Pykemon")
reloj = pygame.time.Clock()
mapa = Mapa("assets/maps/test_map.tmx")
player = Player(ANCHO, ALTO, mapa.ancho, mapa.alto)
jugando = True
camera = Camera(mapa.ancho, mapa.alto, ANCHO, ALTO)
frame_count = 0
menu = MenuManager(ANCHO, ALTO)

while jugando:
    eventos = pygame.event.get()
    
    for evento in eventos: 
        if evento.type == pygame.QUIT: 
            jugando = False
        
        # Abrir/cerrar menú con C
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_c:
            print("Tecla C detectada")  # Debug
            print(f"Diálogo activo: {player.dialogo_box.activo}")  # Debug
            if not player.dialogo_box.activo:
                menu.toggle()
                print(f"Menu activo: {menu.activo}")
    
    teclas = pygame.key.get_pressed()
    
    # Procesar input del menú si está activo
    if menu.activo:
        accion = menu.manejar_input(eventos)
        
        if accion == "POKEMON":
            # TODO: Abrir pantalla de Pokémon
            print("Abriendo equipo Pokémon...")
            menu.activo = False
        
        elif accion == "BOLSA":
            # TODO: Abrir pantalla de objetos
            print("Abriendo bolsa...")
            menu.activo = False
        
        elif accion == "SALIR":
            jugando = False
    
    else:
        # Solo procesar movimiento si el menú NO está activo
        if player.puede_moverse():
            player.update(teclas)
            manejar_movimiento(player, teclas, mapa.colisiones, mapa.npcs)
            camera.update(player.rect)
        
        player.manejar_dialogo(teclas, mapa.npcs)
        
        # Testeo de combate
        frame_count += 1
        if frame_count % 30 == 0:
            if not player.dialogo_box.activo:
                player.testear_combate(mapa.zonas_combate)
    
    # Renderizado
    ventana_juego.fill(BLACK)
    mapa.dibujar(ventana_juego, camera)
    player.dibujar(ventana_juego, camera)
    menu.dibujar(ventana_juego)

    pygame.display.flip()
    reloj.tick(FPS)
pygame.quit() 
sys.exit()

