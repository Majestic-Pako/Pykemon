#Se importan todas las librerias y archivos, carpetas, clases
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
from core.system.batalla import Batalla #Se agrego esta linea de codigo
# Inicialización
pygame.init() 
ventana_juego = pygame.display.set_mode((ANCHO, ALTO)) 
pygame.display.set_caption("Pykemon")
reloj = pygame.time.Clock()

# Componentes del juego
mapa = Mapa("assets/maps/test_map.tmx")
player = Player(ANCHO, ALTO, mapa.ancho, mapa.alto)
camera = Camera(mapa.ancho, mapa.alto, ANCHO, ALTO)
# Instancia de la batalla
batalla = Batalla(ANCHO, ALTO) #Se agrego esta linea de codigo

# Menús
menu = MenuManager(ANCHO, ALTO)
pokemon_menu = PokemonMenu(ANCHO, ALTO)
bolsa_menu = BolsaMenu(ANCHO, ALTO)
usar_objeto_menu = UsarObjetoMenu(ANCHO, ALTO)

# Variables de control
jugando = True
frame_count = 0
objeto_a_usar = None
resultado = None
# Game Loop
while jugando:
    eventos = pygame.event.get()
    
    # === MANEJO DE EVENTOS ===
    for evento in eventos: 
        if evento.type == pygame.QUIT: 
            jugando = False
        
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_c:
            if not player.dialogo_box.activo:
                menu.toggle()
        #Se agrego estas lineas de codigo de logica
        if evento.type == pygame.USEREVENT + 1:
            if batalla.activo:
                batalla.turno_enemigo()
    
    teclas = pygame.key.get_pressed()
    #Se agrego estas lineas de codigo de logica de la batalla
    if batalla.activo:
        resultado = batalla.procesar_eventos(eventos)

    # Si el jugador decide atacar, huir o gana
    if resultado == "HUIR":
        print("Has huido del combate.")
        batalla.terminar_batalla()

    elif resultado == "VICTORIA":
        print("Has ganado la batalla.")
        batalla.terminar_batalla()

    # Evento del turno enemigo (programado dentro de batalla.py)
    for evento in eventos:
        if evento.type == pygame.USEREVENT + 1:
            batalla.turno_enemigo()


    if menu.activo:
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

    else:
        if player.puede_moverse():
            player.update(teclas)
            manejar_movimiento(player, teclas, mapa.colisiones, mapa.npcs)
            camera.update(player.rect)
        
        player.manejar_dialogo(teclas, mapa.npcs)
        
        # Testo de zona de combate
        frame_count += 1
        if frame_count % 30 == 0:
            #Esto estaba antes y se agrego lo siguiente

            #if not player.dialogo_box.activo:
                #player.testear_combate(mapa.zonas_combate)

            #Lo siguiente:
             if not batalla.activo and player.testear_combate(mapa.zonas_combate):
                    # Importar Pokemon si no está importado
                    from core.entities.pokemon import Pokemon
                    import random

                     # Pokémones disponibles según tu JSON
                    pokemons_disponibles = ["treecko", "torchic", "mudkip", "rattata", "pidgey"]
                    nombre_enemigo = random.choice(pokemons_disponibles)
                    pokemon_enemigo = Pokemon(nombre_enemigo, nivel=5)
                    
                   # Iniciar batalla con el primer Pokémon del jugador
                    if len(player.equipo_pokemon) > 0:
                        batalla.empezar_batalla(
                        player.equipo_pokemon[0],
                        pokemon_enemigo,
                        player.bolsa
            )

    # === RENDERIZADO ===
    ventana_juego.fill(BLACK)
    mapa.dibujar(ventana_juego, camera)
    player.dibujar(ventana_juego, camera)
    
    # UI (siempre al final)
    menu.dibujar(ventana_juego)
    pokemon_menu.dibujar(ventana_juego)
    bolsa_menu.dibujar(ventana_juego)
    usar_objeto_menu.dibujar(ventana_juego)
    batalla.dibujar(ventana_juego)#Se agrego esta linea de codigo
    pygame.display.flip()
    reloj.tick(FPS)
    continue
pygame.quit() 
sys.exit()