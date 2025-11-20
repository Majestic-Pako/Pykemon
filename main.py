import pygame 
import sys
import random
from core.entities.movement import manejar_movimiento
from core.entities.player import Player
from core.entities.pokemon import Pokemon
from core.system.map import Mapa
from core.system.config import *
from core.system.camera import Camera
from core.ui.MenuManager import MenuManager
from core.ui.pokemon_menu import PokemonMenu
from core.ui.bolsa_menu import BolsaMenu
from core.ui.use_object_menu import UsarObjetoMenu
from core.ui.pantalla_inicio import PantallaInicio
from core.system.batalla import Batalla
from core.system.portal_manager import PortalManager

pygame.init() 
ventana_juego = pygame.display.set_mode((ANCHO, ALTO)) 
pygame.display.set_caption("Pykemon")
reloj = pygame.time.Clock()

pantalla_inicio = PantallaInicio(ANCHO, ALTO)

while pantalla_inicio.esta_activa():
    delta_time = reloj.get_time()
    eventos = pygame.event.get()
    
    pantalla_inicio.actualizar(eventos, delta_time)
    pantalla_inicio.dibujar(ventana_juego, delta_time)
    
    pygame.display.flip()
    reloj.tick(60)


mapa = Mapa("assets/maps/pueblo_inicial.tmx")
player = Player(ANCHO, ALTO, mapa.ancho, mapa.alto)
camera = Camera(mapa.ancho, mapa.alto, ANCHO, ALTO)
batalla = Batalla(ANCHO, ALTO)

menu = MenuManager(ANCHO, ALTO)
pokemon_menu = PokemonMenu(ANCHO, ALTO)
bolsa_menu = BolsaMenu(ANCHO, ALTO)
usar_objeto_menu = UsarObjetoMenu(ANCHO, ALTO)
portal_manager = PortalManager()

jugando = True
frame_count = 0
objeto_a_usar = None
resultado = None


def verificar_encuentro_pokemon(player_rect, zonas_combate):
    for zona in zonas_combate:
        if player_rect.colliderect(zona["rect"]):
            if random.random() < zona["encounter_rate"]:
                
                pokemon_ids_raw = zona.get("pokemon_ids", "")
                
                if "," in pokemon_ids_raw:
                    pokemon_ids = [p.strip().lower() for p in pokemon_ids_raw.split(",")]
                else:
                    pokemon_ids = [pokemon_ids_raw.strip().lower()]
                
                pokemon_id = random.choice(pokemon_ids)
                
                nivel_base = zona.get("min_level", 3)
                nivel = nivel_base + random.randint(0, 2)
                
                try:
                    pokemon_enemigo = Pokemon(pokemon_id, nivel=nivel)
                    return pokemon_enemigo
                except ValueError as e:
                    print(f"Error creando Pokemon: {e}")
                    return None
    
    return None

while jugando:
    eventos = pygame.event.get()
    
    for evento in eventos: 
        if evento.type == pygame.QUIT: 
            jugando = False
        
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_c:
            if not player.dialogo_box.activo and not batalla.activo and not portal_manager.transicion_activa:
                menu.toggle()
        
        if evento.type == pygame.USEREVENT + 1:
            if batalla.activo:
                batalla.turno_enemigo()
    
    teclas = pygame.key.get_pressed()
    
    if batalla.activo or batalla.transicion_activa:
        batalla.actualizar_transicion()
        batalla.actualizar_animacion()
        
        if batalla.activo:
            resultado = batalla.procesar_eventos(eventos)
            if resultado == "VICTORIA":
                pass
            
            elif resultado == "DERROTA":
                pass
            
            elif resultado == "CAPTURA":
                if batalla.estado_actual == "MENSAJE":
                    pygame.time.wait(800)
                    batalla.terminar_batalla()
            
            elif resultado == "ESCAPADO":
                pass
            
            elif resultado == "TURNO_ENEMIGO":
                while batalla.animacion_activa:
                    batalla.actualizar_animacion()
                    ventana_juego.fill(BLACK)
                    mapa.dibujar(ventana_juego, camera)
                    player.dibujar(ventana_juego, camera)
                    batalla.dibujar(ventana_juego)
                    pygame.display.flip()
                    reloj.tick(FPS)
                
                pygame.time.wait(800)
                resultado_enemigo = batalla.turno_enemigo()
                
                if resultado_enemigo == "DERROTA":
                    pass
            
            elif resultado == "CAMBIO_POKEMON":
                pygame.time.wait(500)
                batalla.turno_enemigo()

    elif menu.activo:
        accion = menu.manejar_input(eventos)
        
        if accion == "POKEMON":
            pokemon_menu.abrir(player.equipo_pokemon)
            menu.activo = False
        
        elif accion == "BOLSA":
            bolsa_menu.abrir(player.bolsa)
            menu.activo = False
        
        elif accion == "SALIR":
            jugando = False
    
    elif pokemon_menu.activo: 
        resultado = pokemon_menu.manejar_input(eventos)
        if resultado == "VOLVER":
            menu.toggle()
    
    elif bolsa_menu.activo:
        resultado = bolsa_menu.manejar_input(eventos)
        if resultado == "VOLVER":
            menu.toggle()
        elif resultado and resultado[0] == "USAR_OBJETO":
            objeto_a_usar = resultado[1]
            item_nombre = bolsa_menu.objects_data[objeto_a_usar]["nombre"]
            usar_objeto_menu.abrir(player.equipo_pokemon, item_nombre)
            bolsa_menu.activo = False
    
    elif usar_objeto_menu.activo:
        resultado = usar_objeto_menu.manejar_input(eventos)
    
        if resultado == "CANCELAR":
            bolsa_menu.activo = True
        elif resultado and resultado[0] == "CONFIRMAR":
            pokemon_index = resultado[1]
            pokemon_objetivo = player.equipo_pokemon[pokemon_index]
        
            resultado_uso = player.usar_objeto(objeto_a_usar, pokemon_objetivo)
            player.dialogo_box.mostrar(resultado_uso.get("mensaje", "No pasó nada"), {})
        
            usar_objeto_menu.cerrar()
            bolsa_menu.abrir(player.bolsa)
            objeto_a_usar = None

    else:
        portal_manager.actualizar_transicion()
        
        if portal_manager.debe_cambiar_mapa():
            destino = portal_manager.obtener_destino()
            
            if destino:
                mapa = Mapa(f"assets/maps/{destino['mapa']}")
                
                player.rect.center = (destino['x'], destino['y'])
                
                player.ancho_mapa = mapa.ancho
                player.alto_mapa = mapa.alto

                camera = Camera(mapa.ancho, mapa.alto, ANCHO, ALTO)
                camera.update(player.rect)
        
        if player.puede_moverse() and not portal_manager.transicion_activa:
            player.update(teclas)
            manejar_movimiento(player, teclas, mapa.colisiones, mapa.npcs)
            camera.update(player.rect)
        
            if not portal_manager.transicion_activa:
                portal_info = portal_manager.verificar_portal(player.rect, mapa.portales)
                if portal_info:
                    portal_manager.cambiar_mapa(
                        portal_info["target_map"],
                        portal_info["target_x"],
                        portal_info["target_y"]
                    )
        
        if not portal_manager.transicion_activa:
            player.manejar_dialogo(teclas, mapa.npcs)
        
        if not portal_manager.transicion_activa:
            frame_count += 1
            if frame_count % 30 == 0:
                if not batalla.activo and not player.dialogo_box.activo:
                    pokemon_enemigo = verificar_encuentro_pokemon(player.rect, mapa.zonas_combate)
                    
                    if pokemon_enemigo:
                        batalla.iniciar_transicion(player, pokemon_enemigo)
    
    ventana_juego.fill(BLACK)
    mapa.dibujar(ventana_juego, camera)
    player.dibujar(ventana_juego, camera)
    
    menu.dibujar(ventana_juego)
    pokemon_menu.dibujar(ventana_juego)
    bolsa_menu.dibujar(ventana_juego)
    usar_objeto_menu.dibujar(ventana_juego)
    batalla.dibujar(ventana_juego)
    
    portal_manager.dibujar_transicion(ventana_juego)
    
    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit() 
sys.exit()