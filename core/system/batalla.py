import pygame
import json
import random

# Configuración de colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
GRIS_OSCURO = (50, 50, 50)
VERDE = (0, 200, 0)
ROJO = (220, 0, 0)
AZUL = (0, 100, 255)
AMARILLO = (255, 200, 0)

class Batalla:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.activo = False
        
        # Pokémon en batalla
        self.mi_pokemon = None
        self.pokemon_enemigo = None
        
        # Sistema de menús
        self.opciones_menu = ["ATACAR", "POKEMON", "BOLSA", "HUIR"]
        self.opcion_actual = 0
        self.estado_actual = "MENSAJE"
        
        # Datos del juego
        self.bolsa = None
        self.equipo = None
        self.mensaje = ""
        
        # Cargar información de objetos
        self.cargar_objetos()
        
        # Cargar imágenes (sprites de ejemplo)
        self.cargar_imagenes()

    def cargar_imagenes(self):
        """Carga las imágenes/sprites para la batalla"""
        try:
            # Fondo de batalla
            self.fondo_batalla = pygame.image.load('images/batalla_fondo.png').convert()
            self.fondo_batalla = pygame.transform.scale(self.fondo_batalla, (self.ancho, self.alto))
        except:
            print("No se pudo cargar fondo_batalla.png - usando fondo sólido")
            self.fondo_batalla = None

    def cargar_objetos(self):
        """Carga los objetos desde el archivo JSON"""
        try:
            with open('objects.json', 'r', encoding='utf-8') as archivo:
                self.objetos_data = json.load(archivo)
        except:
            print("No se pudo cargar objects.json")
            self.objetos_data = {}

    def empezar_batalla(self, mi_pokemon, pokemon_enemigo, bolsa, equipo=None):
        """Inicia una nueva batalla"""
        self.activo = True
        self.mi_pokemon = mi_pokemon
        self.pokemon_enemigo = pokemon_enemigo
        self.bolsa = bolsa
        self.equipo = equipo or [mi_pokemon]
        
        self.mensaje = f"¡Un {pokemon_enemigo.nombre} salvaje apareció!"
        self.estado_actual = "MENSAJE"
        self.opcion_actual = 0

    def procesar_eventos(self, eventos):
        """Procesa los eventos del teclado"""
        if not self.activo:
            return None

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                
                if self.estado_actual in ["MENSAJE", "POKEMON", "BOLSA"]:
                    if evento.key in [pygame.K_RETURN, pygame.K_z]:
                        if self.estado_actual == "MENSAJE":
                            self.estado_actual = "MENU"
                            self.mensaje = ""
                        else:
                            self.estado_actual = "MENU"

                elif self.estado_actual == "MENU":
                    if evento.key == pygame.K_UP:
                        self.opcion_actual = (self.opcion_actual - 1) % len(self.opciones_menu)
                    elif evento.key == pygame.K_DOWN:
                        self.opcion_actual = (self.opcion_actual + 1) % len(self.opciones_menu)
                    elif evento.key in [pygame.K_RETURN, pygame.K_z]:
                        return self.ejecutar_accion()

                elif self.estado_actual == "ATAQUES":
                    if evento.key == pygame.K_UP:
                        self.opcion_actual = (self.opcion_actual - 1) % len(self.mi_pokemon.movimientos)
                    elif evento.key == pygame.K_DOWN:
                        self.opcion_actual = (self.opcion_actual + 1) % len(self.mi_pokemon.movimientos)
                    elif evento.key in [pygame.K_RETURN, pygame.K_z]:
                        return self.usar_ataque()

        return None

    def ejecutar_accion(self):
        """Ejecuta la acción seleccionada en el menú principal"""
        accion = self.opciones_menu[self.opcion_actual]
        
        if accion == "ATACAR":
            self.estado_actual = "ATAQUES"
            self.opcion_actual = 0
        elif accion == "HUIR":
            self.mensaje = "¡Has huido!"
            self.estado_actual = "MENSAJE"
            return "HUIR"
        elif accion == "BOLSA":
            self.mensaje = "Bolsa de objetos"
            self.estado_actual = "BOLSA"
            return "BOLSA"
        elif accion == "POKEMON":
            self.mensaje = "Tu equipo Pokémon"
            self.estado_actual = "POKEMON"
            return "POKEMON"

    def usar_ataque(self):
        """Usa el ataque seleccionado"""
        ataque = self.mi_pokemon.movimientos[self.opcion_actual]
        danio = random.randint(5, 12)
        
        self.pokemon_enemigo.ps_actual -= danio
        self.mensaje = f"{self.mi_pokemon.nombre} usó {ataque['nombre']}!"
        self.estado_actual = "MENSAJE"

        if self.pokemon_enemigo.esta_debilitado():
            self.mensaje = f"¡{self.pokemon_enemigo.nombre} fue derrotado!"
            return "VICTORIA"
        
        return None

    def turno_enemigo(self):
        """El enemigo ataca"""
        if self.pokemon_enemigo and not self.pokemon_enemigo.esta_debilitado():
            danio = random.randint(3, 10)
            self.mi_pokemon.ps_actual -= danio
            self.mensaje = f"{self.pokemon_enemigo.nombre} atacó."
            self.estado_actual = "MENSAJE"
            
            if self.mi_pokemon.esta_debilitado():
                self.mensaje = f"¡{self.mi_pokemon.nombre} fue derrotado!"
                return "DERROTA"
        
        return None

    def dibujar(self, ventana):
        """Dibuja toda la interfaz de batalla"""
        if not self.activo:
            return

        # Fuentes para texto
        fuente_grande = pygame.font.SysFont("Arial", 24, bold=True)
        fuente_normal = pygame.font.SysFont("Arial", 20)
        fuente_pequena = pygame.font.SysFont("Arial", 16)

        # Fondo
        if self.fondo_batalla:
            ventana.blit(self.fondo_batalla, (0, 0))
        else:
            ventana.fill(AZUL)

        # ===== POKÉMON ENEMIGO =====
        # Caja del enemigo
        pygame.draw.rect(ventana, BLANCO, (self.ancho - 280, 40, 230, 90), 0, 10)
        pygame.draw.rect(ventana, GRIS_OSCURO, (self.ancho - 280, 40, 230, 90), 3, 10)
        
        # Nombre y nivel
        ventana.blit(fuente_normal.render(f"{self.pokemon_enemigo.nombre} Nv{self.pokemon_enemigo.nivel}", True, NEGRO), 
                    (self.ancho - 260, 50))
        
        # Barra de vida
        vida_porcentaje = self.pokemon_enemigo.ps_actual / self.pokemon_enemigo.stats_actuales["ps"]
        color_vida = VERDE if vida_porcentaje > 0.5 else AMARILLO if vida_porcentaje > 0.2 else ROJO
        
        pygame.draw.rect(ventana, GRIS_OSCURO, (self.ancho - 260, 80, 160, 12), 0, 5)
        pygame.draw.rect(ventana, color_vida, (self.ancho - 260, 80, int(160 * vida_porcentaje), 12), 0, 5)

        # Sprite Pokémon enemigo (posición ejemplo)
        try:
            sprite_enemigo = pygame.image.load(f'images/pokemon/{self.pokemon_enemigo.nombre.lower()}.png')
            sprite_enemigo = pygame.transform.scale(sprite_enemigo, (120, 120))
            ventana.blit(sprite_enemigo, (self.ancho - 400, 30))
        except:
            # Dibujo de placeholder si no hay sprite
            pygame.draw.rect(ventana, AMARILLO, (self.ancho - 400, 30, 120, 120), 0, 15)
            pygame.draw.rect(ventana, NEGRO, (self.ancho - 400, 30, 120, 120), 2, 15)

        # ===== POKÉMON JUGADOR =====
        # Caja del jugador
        pygame.draw.rect(ventana, BLANCO, (30, self.alto - 160, 280, 110), 0, 10)
        pygame.draw.rect(ventana, GRIS_OSCURO, (30, self.alto - 160, 280, 110), 3, 10)
        
        # Nombre y nivel
        ventana.blit(fuente_normal.render(f"{self.mi_pokemon.nombre} Nv{self.mi_pokemon.nivel}", True, NEGRO), 
                    (50, self.alto - 150))
        
        # Barra de vida
        vida_porcentaje = self.mi_pokemon.ps_actual / self.mi_pokemon.stats_actuales["ps"]
        color_vida = VERDE if vida_porcentaje > 0.5 else AMARILLO if vida_porcentaje > 0.2 else ROJO
        
        pygame.draw.rect(ventana, GRIS_OSCURO, (50, self.alto - 120, 200, 15), 0, 5)
        pygame.draw.rect(ventana, color_vida, (50, self.alto - 120, int(200 * vida_porcentaje), 15), 0, 5)
        
        # Texto de PS
        ventana.blit(fuente_pequena.render(f"PS: {self.mi_pokemon.ps_actual}/{self.mi_pokemon.stats_actuales['ps']}", True, NEGRO), 
                    (50, self.alto - 100))

        # Sprite Pokémon jugador (posición ejemplo)
        try:
            sprite_jugador = pygame.image.load(f'images/pokemon/{self.mi_pokemon.nombre.lower()}.png')
            sprite_jugador = pygame.transform.scale(sprite_jugador, (100, 100))
            ventana.blit(sprite_jugador, (200, self.alto - 250))
        except:
            # Dibujo de placeholder si no hay sprite
            pygame.draw.rect(ventana, VERDE, (200, self.alto - 250, 100, 100), 0, 10)
            pygame.draw.rect(ventana, NEGRO, (200, self.alto - 250, 100, 100), 2, 10)

        # ===== MENÚ PRINCIPAL =====
        if self.estado_actual == "MENU":
            pygame.draw.rect(ventana, BLANCO, (self.ancho - 220, self.alto - 160, 180, 110), 0, 10)
            pygame.draw.rect(ventana, GRIS_OSCURO, (self.ancho - 220, self.alto - 160, 180, 110), 3, 10)
            
            for i, opcion in enumerate(self.opciones_menu):
                color = AZUL if i == self.opcion_actual else NEGRO
                ventana.blit(fuente_normal.render(opcion, True, color), 
                           (self.ancho - 190, self.alto - 140 + i * 25))

        # ===== MENÚ DE ATAQUES =====
        elif self.estado_actual == "ATAQUES":
            pygame.draw.rect(ventana, BLANCO, (40, self.alto - 210, 400, 160), 0, 10)
            pygame.draw.rect(ventana, GRIS_OSCURO, (40, self.alto - 210, 400, 160), 3, 10)
            
            ventana.blit(fuente_grande.render("Elegir ataque:", True, AZUL), (60, self.alto - 190))
            
            for i, ataque in enumerate(self.mi_pokemon.movimientos):
                color = AZUL if i == self.opcion_actual else NEGRO
                ventana.blit(fuente_normal.render(f"{i+1}. {ataque['nombre']}", True, color), 
                           (60, self.alto - 160 + i * 30))

        # ===== MENÚ POKÉMON =====
        elif self.estado_actual == "POKEMON":
            pygame.draw.rect(ventana, BLANCO, (80, 80, self.ancho - 160, self.alto - 160), 0, 15)
            pygame.draw.rect(ventana, GRIS_OSCURO, (80, 80, self.ancho - 160, self.alto - 160), 3, 15)
            
            ventana.blit(fuente_grande.render("Tu equipo Pokémon:", True, AZUL), (100, 100))
            
            y = 140
            for i, pokemon in enumerate(self.equipo):
                estado = "DEBILITADO" if pokemon.esta_debilitado() else f"PS: {pokemon.ps_actual}/{pokemon.stats_actuales['ps']}"
                color_estado = ROJO if pokemon.esta_debilitado() else VERDE
                
                ventana.blit(fuente_normal.render(f"{i+1}. {pokemon.nombre} Nv{pokemon.nivel}", True, NEGRO), (100, y))
                ventana.blit(fuente_pequena.render(estado, True, color_estado), (120, y + 25))
                y += 60

        # ===== MENÚ BOLSA =====
        elif self.estado_actual == "BOLSA":
            pygame.draw.rect(ventana, BLANCO, (80, 80, self.ancho - 160, self.alto - 160), 0, 15)
            pygame.draw.rect(ventana, GRIS_OSCURO, (80, 80, self.ancho - 160, self.alto - 160), 3, 15)
            
            ventana.blit(fuente_grande.render("Tu bolsa:", True, AZUL), (100, 100))
            
            y = 140
            if self.bolsa:
                for objeto_id, cantidad in self.bolsa.items():
                    if objeto_id in self.objetos_data:
                        objeto = self.objetos_data[objeto_id]
                        ventana.blit(fuente_normal.render(f"{objeto['nombre']} x{cantidad}", True, NEGRO), (100, y))
                        ventana.blit(fuente_pequena.render(objeto['descripcion'], True, NEGRO), (120, y + 25))
                        y += 60
            else:
                ventana.blit(fuente_normal.render("Bolsa vacía", True, NEGRO), (100, 140))

        # ===== MENSAJES =====
        elif self.estado_actual == "MENSAJE":
            pygame.draw.rect(ventana, BLANCO, (40, self.alto - 110, self.ancho - 80, 60), 0, 10)
            pygame.draw.rect(ventana, GRIS_OSCURO, (40, self.alto - 110, self.ancho - 80, 60), 3, 10)
            
            ventana.blit(fuente_normal.render(self.mensaje, True, NEGRO), (60, self.alto - 90))
            ventana.blit(fuente_pequena.render("Presiona ENTER", True, GRIS_OSCURO), (60, self.alto - 60))

    def terminar_batalla(self):
        """Termina la batalla y limpia todo"""
        self.activo = False
        self.mi_pokemon = None
        self.pokemon_enemigo = None
        self.mensaje = ""
        self.estado_actual = "MENSAJE"