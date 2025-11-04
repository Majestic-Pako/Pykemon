import pygame
import json
import random

# Colores básicos
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
GRIS = (200, 200, 200)

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
        self.estado_actual = "MENSAJE"  # Puede ser: MENSAJE, MENU, ATAQUES, POKEMON, BOLSA
        
        # Datos del juego
        self.bolsa = None
        self.equipo = None
        self.mensaje = ""
        
        # Cargar información de objetos
        self.cargar_objetos()

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
                
                # Presionar ENTER para continuar mensajes
                if self.estado_actual in ["MENSAJE", "POKEMON", "BOLSA"]:
                    if evento.key in [pygame.K_RETURN, pygame.K_z]:
                        if self.estado_actual == "MENSAJE":
                            self.estado_actual = "MENU"
                            self.mensaje = ""
                        else:
                            self.estado_actual = "MENU"

                # Navegar por menús
                elif self.estado_actual == "MENU":
                    if evento.key == pygame.K_UP:
                        self.opcion_actual = (self.opcion_actual - 1) % len(self.opciones_menu)
                    elif evento.key == pygame.K_DOWN:
                        self.opcion_actual = (self.opcion_actual + 1) % len(self.opciones_menu)
                    elif evento.key in [pygame.K_RETURN, pygame.K_z]:
                        return self.ejecutar_accion()

                # Navegar por ataques
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

        # Verificar si el enemigo fue derrotado
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
            
            # Verificar si nuestro Pokémon fue derrotado
            if self.mi_pokemon.esta_debilitado():
                self.mensaje = f"¡{self.mi_pokemon.nombre} fue derrotado!"
                return "DERROTA"
        
        return None

    def dibujar(self, ventana):
        """Dibuja toda la interfaz de batalla"""
        if not self.activo:
            return

        # Fuentes para texto
        fuente_grande = pygame.font.SysFont("Arial", 24)
        fuente_normal = pygame.font.SysFont("Arial", 20)
        fuente_pequena = pygame.font.SysFont("Arial", 16)

        # Fondo simple
        ventana.fill(BLANCO)

        # ===== INFORMACIÓN DEL ENEMIGO =====
        # Caja del enemigo
        pygame.draw.rect(ventana, GRIS, (self.ancho - 250, 50, 200, 80))
        pygame.draw.rect(ventana, NEGRO, (self.ancho - 250, 50, 200, 80), 2)
        
        # Nombre y nivel
        ventana.blit(fuente_normal.render(f"{self.pokemon_enemigo.nombre} Nv{self.pokemon_enemigo.nivel}", True, NEGRO), 
                    (self.ancho - 230, 60))
        
        # Barra de vida
        vida_porcentaje = self.pokemon_enemigo.ps_actual / self.pokemon_enemigo.stats_actuales["ps"]
        color_vida = VERDE if vida_porcentaje > 0.5 else AMARILLO if vida_porcentaje > 0.2 else ROJO
        
        pygame.draw.rect(ventana, GRIS, (self.ancho - 230, 90, 150, 15))
        pygame.draw.rect(ventana, color_vida, (self.ancho - 230, 90, int(150 * vida_porcentaje), 15))
        pygame.draw.rect(ventana, NEGRO, (self.ancho - 230, 90, 150, 15), 1)

        # ===== INFORMACIÓN DEL JUGADOR =====
        # Caja del jugador
        pygame.draw.rect(ventana, GRIS, (50, self.alto - 150, 250, 100))
        pygame.draw.rect(ventana, NEGRO, (50, self.alto - 150, 250, 100), 2)
        
        # Nombre y nivel
        ventana.blit(fuente_normal.render(f"{self.mi_pokemon.nombre} Nv{self.mi_pokemon.nivel}", True, NEGRO), 
                    (70, self.alto - 140))
        
        # Barra de vida
        vida_porcentaje = self.mi_pokemon.ps_actual / self.mi_pokemon.stats_actuales["ps"]
        color_vida = VERDE if vida_porcentaje > 0.5 else AMARILLO if vida_porcentaje > 0.2 else ROJO
        
        pygame.draw.rect(ventana, GRIS, (70, self.alto - 110, 200, 15))
        pygame.draw.rect(ventana, color_vida, (70, self.alto - 110, int(200 * vida_porcentaje), 15))
        pygame.draw.rect(ventana, NEGRO, (70, self.alto - 110, 200, 15), 1)
        
        # Texto de PS
        ventana.blit(fuente_pequena.render(f"PS: {self.mi_pokemon.ps_actual}/{self.mi_pokemon.stats_actuales['ps']}", True, NEGRO), 
                    (70, self.alto - 90))

        # ===== MENÚ PRINCIPAL =====
        if self.estado_actual == "MENU":
            pygame.draw.rect(ventana, GRIS, (self.ancho - 200, self.alto - 150, 150, 100))
            pygame.draw.rect(ventana, NEGRO, (self.ancho - 200, self.alto - 150, 150, 100), 2)
            
            for i, opcion in enumerate(self.opciones_menu):
                color = ROJO if i == self.opcion_actual else NEGRO
                ventana.blit(fuente_normal.render(opcion, True, color), 
                           (self.ancho - 180, self.alto - 130 + i * 25))

        # ===== MENÚ DE ATAQUES =====
        elif self.estado_actual == "ATAQUES":
            pygame.draw.rect(ventana, GRIS, (50, self.alto - 200, 400, 150))
            pygame.draw.rect(ventana, NEGRO, (50, self.alto - 200, 400, 150), 2)
            
            ventana.blit(fuente_grande.render("Elegir ataque:", True, AZUL), (70, self.alto - 180))
            
            for i, ataque in enumerate(self.mi_pokemon.movimientos):
                color = ROJO if i == self.opcion_actual else NEGRO
                ventana.blit(fuente_normal.render(f"{i+1}. {ataque['nombre']}", True, color), 
                           (70, self.alto - 150 + i * 30))

        # ===== MENÚ POKÉMON =====
        elif self.estado_actual == "POKEMON":
            pygame.draw.rect(ventana, GRIS, (100, 100, self.ancho - 200, self.alto - 200))
            pygame.draw.rect(ventana, NEGRO, (100, 100, self.ancho - 200, self.alto - 200), 2)
            
            ventana.blit(fuente_grande.render("Tu equipo Pokémon:", True, AZUL), (120, 120))
            
            # Mostrar cada Pokémon del equipo
            y = 160
            for i, pokemon in enumerate(self.equipo):
                estado = "DEBILITADO" if pokemon.esta_debilitado() else f"PS: {pokemon.ps_actual}/{pokemon.stats_actuales['ps']}"
                color_estado = ROJO if pokemon.esta_debilitado() else VERDE
                
                ventana.blit(fuente_normal.render(f"{i+1}. {pokemon.nombre} Nv{pokemon.nivel}", True, NEGRO), (120, y))
                ventana.blit(fuente_pequena.render(estado, True, color_estado), (140, y + 25))
                y += 60

        # ===== MENÚ BOLSA =====
        elif self.estado_actual == "BOLSA":
            pygame.draw.rect(ventana, GRIS, (100, 100, self.ancho - 200, self.alto - 200))
            pygame.draw.rect(ventana, NEGRO, (100, 100, self.ancho - 200, self.alto - 200), 2)
            
            ventana.blit(fuente_grande.render("Tu bolsa:", True, AZUL), (120, 120))
            
            # Mostrar objetos
            y = 160
            if self.bolsa:
                for objeto_id, cantidad in self.bolsa.items():
                    if objeto_id in self.objetos_data:
                        objeto = self.objetos_data[objeto_id]
                        ventana.blit(fuente_normal.render(f"{objeto['nombre']} x{cantidad}", True, NEGRO), (120, y))
                        ventana.blit(fuente_pequena.render(objeto['descripcion'], True, NEGRO), (140, y + 25))
                        y += 60
            else:
                ventana.blit(fuente_normal.render("Bolsa vacía", True, NEGRO), (120, 160))

        # ===== MENSAJES =====
        elif self.estado_actual == "MENSAJE":
            pygame.draw.rect(ventana, GRIS, (50, self.alto - 100, self.ancho - 100, 50))
            pygame.draw.rect(ventana, NEGRO, (50, self.alto - 100, self.ancho - 100, 50), 2)
            
            ventana.blit(fuente_normal.render(self.mensaje, True, NEGRO), (70, self.alto - 80))
            ventana.blit(fuente_pequena.render("Presiona ENTER", True, NEGRO), (70, self.alto - 50))

    def terminar_batalla(self):
        """Termina la batalla y limpia todo"""
        self.activo = False
        self.mi_pokemon = None
        self.pokemon_enemigo = None
        self.mensaje = ""
        self.estado_actual = "MENSAJE"