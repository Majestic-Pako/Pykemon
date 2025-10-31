import pygame 
import sys
from core.entities.movement import manejar_movimiento
from core.entities.player import Player
from core.system.map import Mapa
from core.system.config import *
from core.system.camera import Camera
from core.ui.MenuManager import MenuManager
from core.ui.pokemon_menu import PokemonMenu
from core.ui.bolsa_menu import BolsaMenu
from core.ui.use_object_menu import UsarObjetoMenu
import random
from core.battle.battle_system import BattleSystem
from core.entities.pokemon import Pokemon

# Inicialización
pygame.init() 
ventana_juego = pygame.display.set_mode((ANCHO, ALTO)) 
pygame.display.set_caption("Pykemon")
reloj = pygame.time.Clock()

# Componentes del juego
mapa = Mapa("assets/maps/test_map.tmx")
player = Player(ANCHO, ALTO, mapa.ancho, mapa.alto)
camera = Camera(mapa.ancho, mapa.alto, ANCHO, ALTO)

# Menús
menu = MenuManager(ANCHO, ALTO)
pokemon_menu = PokemonMenu(ANCHO, ALTO)
bolsa_menu = BolsaMenu(ANCHO, ALTO)
usar_objeto_menu = UsarObjetoMenu(ANCHO, ALTO)

# Sistema de batalla
battle_system = BattleSystem(ANCHO, ALTO)

# Variables de control
jugando = True
frame_count = 0
objeto_a_usar = None

# Game Loop
while jugando:
    eventos = pygame.event.get()
    
    # === MANEJO DE EVENTOS ===
    for evento in eventos: 
        if evento.type == pygame.QUIT: 
            jugando = False
        
        # Si hay batalla activa, el sistema de batalla maneja los inputs
        if battle_system.active: 
            battle_system.manejar_input(evento)
            continue  # No procesar otros inputs durante batalla
        
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_c:
            if not player.dialogo_box.activo:
                menu.toggle()
    
    teclas = pygame.key.get_pressed()
    
    # === LÓGICA DE BATALLA ===
    if battle_system.active:
        battle_system.actualizar()
        
        # Verificar si la batalla terminó
        if not battle_system.active:
            resultado = battle_system.battle_result
            if resultado == 'win':
                player.dialogo_box.mostrar("¡Ganaste la batalla!", {})
            elif resultado == 'lose':
                player.dialogo_box.mostrar("Tus Pokémon se debilitaron...", {})
            elif resultado == 'escape':
                player.dialogo_box.mostrar("¡Escapaste!", {})
    
    # === LÓGICA DE MENÚS ===
    elif menu.activo:
        accion = menu.manejar_input(eventos)
        
        if accion == "POKEMON":
            pokemon_menu.abrir(player.equipo_pokemon)
            menu.activo = False
            continue
        
        elif accion == "BOLSA":
            bolsa_menu.abrir(player.bolsa)
            menu.activo = False
            continue
        
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
            # Guardar objeto y abrir menú de selección de Pokémon
            objeto_a_usar = resultado[1]
            item_nombre = bolsa_menu.objects_data[objeto_a_usar]["nombre"]
            usar_objeto_menu.abrir(player.equipo_pokemon, item_nombre)
            bolsa_menu.activo = False
            continue
    
    elif usar_objeto_menu.activo:
        resultado = usar_objeto_menu.manejar_input(eventos)
    
        if resultado == "CANCELAR":
            bolsa_menu.activo = True  # Volver a la bolsa
        elif resultado and resultado[0] == "CONFIRMAR":
            pokemon_index = resultado[1]
            pokemon_objetivo = player.equipo_pokemon[pokemon_index]
        
            resultado_uso = player.usar_objeto(objeto_a_usar, pokemon_objetivo)
            player.dialogo_box.mostrar(resultado_uso.get("mensaje", "No pasó nada"), {})
        
            usar_objeto_menu.cerrar()
            bolsa_menu.abrir(player.bolsa)
            objeto_a_usar = None
    
    # === LÓGICA NORMAL DEL JUEGO ===
    else:
        if player.puede_moverse():
            player.update(teclas)
            manejar_movimiento(player, teclas, mapa.colisiones, mapa.npcs)
            camera.update(player.rect)
        
        player.manejar_dialogo(teclas, mapa.npcs)
        
        # Detección de encuentros en zonas de combate
        frame_count += 1
        if frame_count % 30 == 0:  # Checkea cada 30 frames
            if not player.dialogo_box.activo and not battle_system.active:
                # Verificar si está en zona de combate
                for zona in mapa.zonas_combate:
                    if player.rect.colliderect(zona["rect"]):
                        # Probabilidad de encuentro según encounter_rate
                        if random.random() < zona["encounter_rate"]:
                            # Elegir Pokémon enemigo aleatorio de la zona
                            pokemon_id = random.choice(zona["pokemon_ids"]).strip()
                            nivel_enemigo = zona["min_level"] + random.randint(0, 2)
                            
                            # Crear Pokémon enemigo
                            enemigo = Pokemon(pokemon_id, nivel=nivel_enemigo)
                            
                            # Obtener Pokémon activo del jugador
                            pokemon_jugador = player.obtener_pokemon_activo()
                            
                            if pokemon_jugador:
                                # INICIAR BATALLA
                                battle_system.iniciar_batalla(pokemon_jugador, enemigo)
                                break  # Solo un encuentro a la vez
    
    # === RENDERIZADO ===
    ventana_juego.fill(BLACK)
    
    # Si hay batalla activa, solo dibujar la batalla
    if battle_system.active:
        battle_system.dibujar(ventana_juego)
    else:
        # Dibujar juego normal
        mapa.dibujar(ventana_juego, camera)
        player.dibujar(ventana_juego, camera)
        
        # UI (siempre al final)
        menu.dibujar(ventana_juego)
        pokemon_menu.dibujar(ventana_juego)
        bolsa_menu.dibujar(ventana_juego)
        usar_objeto_menu.dibujar(ventana_juego)
    
    pygame.display.flip()
    reloj.tick(FPS)

pygame.quit() 
sys.exit()