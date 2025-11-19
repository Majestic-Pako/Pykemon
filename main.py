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

# ========== PANTALLA DE INICIO ==========
pantalla_inicio = PantallaInicio(ANCHO, ALTO)

# Loop de pantalla de inicio
while pantalla_inicio.esta_activa():
    delta_time = reloj.get_time()
    eventos = pygame.event.get()
    
    pantalla_inicio.actualizar(eventos, delta_time)
    pantalla_inicio.dibujar(ventana_juego, delta_time)
    
    pygame.display.flip()
    reloj.tick(60)

#print("[INFO] Cargando juego...")

# ========== INICIALIZACIÓN DEL JUEGO ==========
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
    """
    Verifica si hay encuentro en zonas de combate del mapa actual
    
    Returns:
        Pokemon enemigo si hay encuentro, None si no
    """
    for zona in zonas_combate:
        # Verificar colisión
        if player_rect.colliderect(zona["rect"]):
            # Tirar dado para encuentro
            if random.random() < zona["encounter_rate"]:
                
                # Obtener pokemon_ids (puede ser string o lista separada por comas)
                pokemon_ids_raw = zona.get("pokemon_ids", "")
                
                # Parsear múltiples pokémon si hay comas
                if "," in pokemon_ids_raw:
                    pokemon_ids = [p.strip().lower() for p in pokemon_ids_raw.split(",")]
                else:
                    pokemon_ids = [pokemon_ids_raw.strip().lower()]
                
                # Elegir uno aleatorio
                pokemon_id = random.choice(pokemon_ids)
                
                # Nivel aleatorio (min_level + 0 a 2)
                nivel_base = zona.get("min_level", 3)
                nivel = nivel_base + random.randint(0, 2)
                
                # Crear Pokémon enemigo
                try:
                    pokemon_enemigo = Pokemon(pokemon_id, nivel=nivel)
                    return pokemon_enemigo
                except ValueError as e:
                    print(f"Error creando Pokemon: {e}")
                    return None
    
    return None


# ========== GAME LOOP ==========
while jugando:
    eventos = pygame.event.get()
    
    # === MANEJO DE EVENTOS ===
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
    
    # ========== SISTEMA DE BATALLA ==========
    if batalla.activo or batalla.transicion_activa:
        batalla.actualizar_transicion()
        batalla.actualizar_animacion()
        
        if batalla.activo:
            resultado = batalla.procesar_eventos(eventos)

            # Manejar resultados de batalla
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

    # ========== MENÚS ==========
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

    # ========== EXPLORACIÓN ==========
    else:
        # Actualizar transición de portales
        portal_manager.actualizar_transicion()
        
        # Cambiar mapa cuando la pantalla esté negra
        if portal_manager.debe_cambiar_mapa():
            destino = portal_manager.obtener_destino()
            
            if destino:
                # Cargar nuevo mapa
                mapa = Mapa(f"assets/maps/{destino['mapa']}")
                
                # Reposicionar jugador
                player.rect.center = (destino['x'], destino['y'])
                
                # Actualizar dimensiones del mapa para límites
                player.ancho_mapa = mapa.ancho
                player.alto_mapa = mapa.alto

                camera = Camera(mapa.ancho, mapa.alto, ANCHO, ALTO)
                camera.update(player.rect)
        
        # Solo permitir movimiento si no hay transición activa
        if player.puede_moverse() and not portal_manager.transicion_activa:
            player.update(teclas)
            manejar_movimiento(player, teclas, mapa.colisiones, mapa.npcs)
            camera.update(player.rect)
        
            # Verificar portales (solo si no hay transición activa)
            if not portal_manager.transicion_activa:
                portal_info = portal_manager.verificar_portal(player.rect, mapa.portales)
                if portal_info:
                    portal_manager.cambiar_mapa(
                        portal_info["target_map"],
                        portal_info["target_x"],
                        portal_info["target_y"]
                    )
        
        # Manejar diálogos con NPCs (solo si no hay transición)
        if not portal_manager.transicion_activa:
            player.manejar_dialogo(teclas, mapa.npcs)
        
        # Encuentros Pokémon (solo si no hay transición de portal)
        if not portal_manager.transicion_activa:
            frame_count += 1
            if frame_count % 30 == 0:
                if not batalla.activo and not player.dialogo_box.activo:
                    pokemon_enemigo = verificar_encuentro_pokemon(player.rect, mapa.zonas_combate)
                    
                    if pokemon_enemigo:
                        batalla.iniciar_transicion(player, pokemon_enemigo)
    
    # ========== RENDERIZADO ==========
    ventana_juego.fill(BLACK)
    mapa.dibujar(ventana_juego, camera)
    player.dibujar(ventana_juego, camera)
    
    # UI (siempre al final)
    menu.dibujar(ventana_juego)
    pokemon_menu.dibujar(ventana_juego)
    bolsa_menu.dibujar(ventana_juego)
    usar_objeto_menu.dibujar(ventana_juego)
    batalla.dibujar(ventana_juego)
    
    # Transición de portales 
    portal_manager.dibujar_transicion(ventana_juego)
    
    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit() 
sys.exit()