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
        
        # Referencia al jugador (para acceder a su bolsa y equipo)
        self.jugador = None
        
        # Sistema de menús
        self.opciones_menu = ["ATACAR", "POKEMON", "BOLSA", "HUIR"]
        self.opcion_actual = 0
        self.estado_actual = "MENSAJE"
        self.categoria_bolsa_actual = "curacion"
        self.categorias_bolsa = ["curacion", "captura", "debug"]
        self.indice_categoria = 0
        
        self.mensaje = ""
        
        # Variables de resultado
        self.resultado_batalla = None
        self.frames_resultado = 0
        self.duracion_resultado = 120
        
        # Variables de animación
        self.animacion_activa = False
        self.animacion_tipo = None
        self.animacion_frame = 0
        self.animacion_duracion = 20
        
        # Cargar imágenes
        self.cargar_imagenes()

    def cargar_imagenes(self):
        """Carga las imágenes/sprites para la batalla"""
        try:
            self.fondo_batalla = pygame.image.load('assets/images/batalla_fondo.png').convert()
            self.fondo_batalla = pygame.transform.scale(self.fondo_batalla, (self.ancho, self.alto))
            #print("✓ Fondo de batalla cargado")
        except:
            try:
                # Intenta buscar en images/ directamente
                self.fondo_batalla = pygame.image.load('images/batalla_fondo.png').convert()
                self.fondo_batalla = pygame.transform.scale(self.fondo_batalla, (self.ancho, self.alto))
                #print("✓ Fondo de batalla cargado desde images/")
            except Exception as e:
                print(f"No se pudo cargar fondo_batalla.png: {e}")
                self.fondo_batalla = None

    def empezar_batalla(self, jugador, pokemon_enemigo):
        """Inicia una nueva batalla recibiendo el jugador completo"""
        self.activo = True
        self.jugador = jugador
        self.mi_pokemon = jugador.obtener_pokemon_activo()
        
        if not self.mi_pokemon:
            print("Error: No hay Pokémon disponibles para batalla")
            self.activo = False
            return
        
        self.pokemon_enemigo = pokemon_enemigo
        
        self.mensaje = f"¡Un {pokemon_enemigo.nombre} salvaje apareció!"
        self.estado_actual = "MENSAJE"
        self.opcion_actual = 0
        self.indice_categoria = 0
        self.categoria_bolsa_actual = "curacion"
        
        self.animacion_activa = False
        self.animacion_frame = 0

    def actualizar_animacion(self):
        """Actualiza la animación de ataque"""
        if self.animacion_activa:
            self.animacion_frame += 1
            if self.animacion_frame >= self.animacion_duracion:
                self.animacion_activa = False
                self.animacion_frame = 0
        
        if self.resultado_batalla:
            self.frames_resultado += 1

    def procesar_eventos(self, eventos):
        """Procesa los eventos del teclado"""
        if not self.activo:
            return None
        
        if self.resultado_batalla:
            if self.frames_resultado >= self.duracion_resultado:
                return self.resultado_batalla
            return None

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                
                if self.estado_actual == "MENSAJE":
                    if evento.key in [pygame.K_RETURN, pygame.K_z]:
                        self.estado_actual = "MENU"
                        self.mensaje = ""
                
                elif self.estado_actual == "POKEMON":
                    if evento.key == pygame.K_UP:
                        self.opcion_actual = (self.opcion_actual - 1) % len(self.jugador.equipo_pokemon)
                    elif evento.key == pygame.K_DOWN:
                        self.opcion_actual = (self.opcion_actual + 1) % len(self.jugador.equipo_pokemon)
                    elif evento.key in [pygame.K_RETURN, pygame.K_z]:
                        return self.cambiar_pokemon()
                    elif evento.key == pygame.K_ESCAPE:
                        self.estado_actual = "MENU"
                        self.opcion_actual = 0

                elif self.estado_actual == "BOLSA":
                    if evento.key == pygame.K_LEFT:
                        self.indice_categoria = (self.indice_categoria - 1) % len(self.categorias_bolsa)
                        self.categoria_bolsa_actual = self.categorias_bolsa[self.indice_categoria]
                        self.opcion_actual = 0
                    elif evento.key == pygame.K_RIGHT:
                        self.indice_categoria = (self.indice_categoria + 1) % len(self.categorias_bolsa)
                        self.categoria_bolsa_actual = self.categorias_bolsa[self.indice_categoria]
                        self.opcion_actual = 0
                    elif evento.key == pygame.K_UP:
                        objetos_categoria = list(self.jugador.bolsa[self.categoria_bolsa_actual].keys())
                        if objetos_categoria:
                            self.opcion_actual = (self.opcion_actual - 1) % len(objetos_categoria)
                    elif evento.key == pygame.K_DOWN:
                        objetos_categoria = list(self.jugador.bolsa[self.categoria_bolsa_actual].keys())
                        if objetos_categoria:
                            self.opcion_actual = (self.opcion_actual + 1) % len(objetos_categoria)
                    elif evento.key in [pygame.K_RETURN, pygame.K_z]:
                        return self.usar_objeto_seleccionado()
                    elif evento.key == pygame.K_ESCAPE:
                        self.estado_actual = "MENU"
                        self.opcion_actual = 0

                elif self.estado_actual == "MENU":
                    if evento.key == pygame.K_UP:
                        if self.opcion_actual >= 2:
                            self.opcion_actual -= 2
                    elif evento.key == pygame.K_DOWN:
                        if self.opcion_actual <= 1:
                            self.opcion_actual += 2
                    elif evento.key == pygame.K_LEFT:
                        if self.opcion_actual % 2 == 1:
                            self.opcion_actual -= 1
                    elif evento.key == pygame.K_RIGHT:
                        if self.opcion_actual % 2 == 0:
                            self.opcion_actual += 1
                    elif evento.key in [pygame.K_RETURN, pygame.K_z]:
                        return self.ejecutar_accion()

                elif self.estado_actual == "ATAQUES":
                    if evento.key == pygame.K_UP:
                        self.opcion_actual = (self.opcion_actual - 1) % len(self.mi_pokemon.movimientos)
                    elif evento.key == pygame.K_DOWN:
                        self.opcion_actual = (self.opcion_actual + 1) % len(self.mi_pokemon.movimientos)
                    elif evento.key in [pygame.K_RETURN, pygame.K_z]:
                        return self.usar_ataque()
                    elif evento.key == pygame.K_ESCAPE:
                        self.estado_actual = "MENU"
                        self.opcion_actual = 0

        return None

    def ejecutar_accion(self):
        """Ejecuta la acción seleccionada en el menú principal"""
        accion = self.opciones_menu[self.opcion_actual]
        
        if accion == "ATACAR":
            self.estado_actual = "ATAQUES"
            self.opcion_actual = 0
        elif accion == "HUIR":
            self.resultado_batalla = "ESCAPADO"
            self.frames_resultado = 0
            return None
        elif accion == "BOLSA":
            self.estado_actual = "BOLSA"
            self.opcion_actual = 0
            self.indice_categoria = 0
            self.categoria_bolsa_actual = "curacion"
            return None
        elif accion == "POKEMON":
            pokemon_disponibles = [p for p in self.jugador.equipo_pokemon if not p.esta_debilitado()]
            if len(pokemon_disponibles) <= 1:
                self.mensaje = "No hay otros Pokémon disponibles"
                self.estado_actual = "MENSAJE"
            else:
                self.estado_actual = "POKEMON"
                self.opcion_actual = 0
            return None

    def usar_ataque(self):
        """Usa el ataque seleccionado CON ANIMACIÓN"""
        ataque = self.mi_pokemon.movimientos[self.opcion_actual]
        danio = random.randint(5, 12)
        
        self.animacion_activa = True
        self.animacion_tipo = "ataque_jugador"
        self.animacion_frame = 0
        
        self.pokemon_enemigo.ps_actual -= danio
        self.mensaje = f"{self.mi_pokemon.nombre} usó {ataque['nombre']}!"
        self.estado_actual = "MENSAJE"

        if self.pokemon_enemigo.esta_debilitado():
            self.resultado_batalla = "VICTORIA"
            self.frames_resultado = 0
            return None
        
        return "TURNO_ENEMIGO"

    def cambiar_pokemon(self):
        """Cambia al Pokémon seleccionado"""
        pokemon_seleccionado = self.jugador.equipo_pokemon[self.opcion_actual]
        
        if pokemon_seleccionado == self.mi_pokemon:
            self.mensaje = f"¡{pokemon_seleccionado.nombre} ya está en batalla!"
            self.estado_actual = "MENSAJE"
            return None
        
        if pokemon_seleccionado.esta_debilitado():
            self.mensaje = f"¡{pokemon_seleccionado.nombre} está debilitado!"
            self.estado_actual = "MENSAJE"
            return None
        
        nombre_anterior = self.mi_pokemon.nombre
        self.mi_pokemon = pokemon_seleccionado
        self.mensaje = f"¡Adelante, {self.mi_pokemon.nombre}!"
        self.estado_actual = "MENSAJE"
        
        return "CAMBIO_POKEMON"

    def usar_objeto_seleccionado(self):
        """Usa el objeto seleccionado de la bolsa del jugador"""
        objetos_categoria = list(self.jugador.bolsa[self.categoria_bolsa_actual].keys())
        
        if not objetos_categoria:
            self.mensaje = "No tienes objetos en esta categoría"
            self.estado_actual = "MENSAJE"
            return None
        
        objeto_key = objetos_categoria[self.opcion_actual]
        
        if self.categoria_bolsa_actual == "curacion":
            resultado = self.jugador.usar_objeto(objeto_key, self.mi_pokemon)
            self.mensaje = resultado["mensaje"]
            self.estado_actual = "MENSAJE"
        elif self.categoria_bolsa_actual == "captura":
            resultado = self.jugador.usar_objeto(objeto_key)
            if resultado["exito"]:
                tasa = resultado["tasa_captura"]
                probabilidad = random.random()
                
                if probabilidad < tasa:
                    self.mensaje = f"¡Capturaste a {self.pokemon_enemigo.nombre}!"
                    self.jugador.agregar_pokemon(self.pokemon_enemigo)
                    self.resultado_batalla = "CAPTURA"
                    self.frames_resultado = 0
                    return None
                else:
                    self.mensaje = f"¡Casi lo has capturado!"
                    self.estado_actual = "MENSAJE"
                    return "TURNO_ENEMIGO"
            else:
                self.mensaje = resultado["mensaje"]
                self.estado_actual = "MENSAJE"
        elif self.categoria_bolsa_actual == "debug":
            resultado = self.jugador.usar_objeto(objeto_key, self.mi_pokemon)
            self.mensaje = resultado["mensaje"]
            self.estado_actual = "MENSAJE"
        
        return None

    def turno_enemigo(self):
        """El enemigo ataca CON ANIMACIÓN"""
        if self.pokemon_enemigo and not self.pokemon_enemigo.esta_debilitado():
            self.animacion_activa = True
            self.animacion_tipo = "ataque_enemigo"
            self.animacion_frame = 0
            
            danio = random.randint(3, 10)
            self.mi_pokemon.ps_actual -= danio
            self.mensaje = f"{self.pokemon_enemigo.nombre} atacó."
            self.estado_actual = "MENSAJE"
            
            if self.mi_pokemon.esta_debilitado():
                self.resultado_batalla = "DERROTA"
                self.frames_resultado = 0
        
        return None

    def dibujar(self, ventana):
        """Dibuja toda la interfaz de batalla"""
        if not self.activo:
            return

        fuente_grande = pygame.font.SysFont("Arial", 24, bold=True)
        fuente_normal = pygame.font.SysFont("Arial", 20)
        fuente_pequena = pygame.font.SysFont("Arial", 16)

        if self.fondo_batalla:
            ventana.blit(self.fondo_batalla, (0, 0))
        else:
            ventana.fill(AZUL)

        offset_x_jugador = 0
        offset_y_jugador = 0
        offset_x_enemigo = 0
        offset_y_enemigo = 0
        
        if self.animacion_activa:
            progreso = self.animacion_frame / self.animacion_duracion
            
            if self.animacion_tipo == "ataque_jugador":
                if progreso < 0.5:
                    offset_x_jugador = int(60 * (progreso * 2))
                else:
                    offset_x_jugador = int(60 * (2 - progreso * 2))
            
            elif self.animacion_tipo == "ataque_enemigo":
                if progreso < 0.5:
                    offset_x_enemigo = int(-60 * (progreso * 2))
                else:
                    offset_x_enemigo = int(-60 * (2 - progreso * 2))

        # SPRITE DEL ENEMIGO (BACK)
        try:
            ruta_enemigo = f'assets/images/pokemon/front/{self.pokemon_enemigo.nombre.lower()}.png'
            #print(f"Intentando cargar enemigo: {ruta_enemigo}")
            sprite_enemigo = pygame.image.load(ruta_enemigo)
            sprite_enemigo = pygame.transform.scale(sprite_enemigo, (120, 120))
            ventana.blit(sprite_enemigo, (self.ancho - 180 + offset_x_enemigo, 60 + offset_y_enemigo))
            #print("✓ Sprite enemigo cargado correctamente")
        except Exception as e:
            print(f"✗ Error cargando sprite enemigo: {e}")
            pygame.draw.rect(ventana, AMARILLO, (self.ancho - 180 + offset_x_enemigo, 60 + offset_y_enemigo, 120, 120), 0, 15)
            pygame.draw.rect(ventana, NEGRO, (self.ancho - 180 + offset_x_enemigo, 60 + offset_y_enemigo, 120, 120), 2, 15)
        
        pygame.draw.rect(ventana, BLANCO, (self.ancho - 440, 60, 230, 90), 0, 10)
        pygame.draw.rect(ventana, GRIS_OSCURO, (self.ancho - 440, 60, 230, 90), 3, 10)
        
        ventana.blit(fuente_normal.render(f"{self.pokemon_enemigo.nombre} Nv{self.pokemon_enemigo.nivel}", True, NEGRO), 
                    (self.ancho - 420, 70))
        
        vida_porcentaje = self.pokemon_enemigo.ps_actual / self.pokemon_enemigo.stats_actuales["ps"]
        color_vida = VERDE if vida_porcentaje > 0.5 else AMARILLO if vida_porcentaje > 0.2 else ROJO
        
        pygame.draw.rect(ventana, GRIS_OSCURO, (self.ancho - 420, 100, 160, 12), 0, 5)
        pygame.draw.rect(ventana, color_vida, (self.ancho - 420, 100, int(160 * vida_porcentaje), 12), 0, 5)

        # SPRITE DEL JUGADOR (FRONT)
        try:
            ruta_jugador = f'assets/images/pokemon/back/{self.mi_pokemon.nombre.lower()}.png'
            #print(f"Intentando cargar jugador: {ruta_jugador}")
            sprite_jugador = pygame.image.load(ruta_jugador)
            sprite_jugador = pygame.transform.scale(sprite_jugador, (120, 120))
            ventana.blit(sprite_jugador, (60 + offset_x_jugador, 230 + offset_y_jugador))
            #print("✓ Sprite jugador cargado correctamente")
        except Exception as e:
            print(f"✗ Error cargando sprite jugador: {e}")
            pygame.draw.rect(ventana, VERDE, (60 + offset_x_jugador, 230 + offset_y_jugador, 120, 120), 0, 10)
            pygame.draw.rect(ventana, NEGRO, (60 + offset_x_jugador, 230 + offset_y_jugador, 120, 120), 2, 10)
        
        pygame.draw.rect(ventana, BLANCO, (220, 230, 280, 110), 0, 10)
        pygame.draw.rect(ventana, GRIS_OSCURO, (220, 230, 280, 110), 3, 10)
        
        ventana.blit(fuente_normal.render(f"{self.mi_pokemon.nombre} Nv{self.mi_pokemon.nivel}", True, NEGRO), 
                    (240, 240))
        
        vida_porcentaje = self.mi_pokemon.ps_actual / self.mi_pokemon.stats_actuales["ps"]
        color_vida = VERDE if vida_porcentaje > 0.5 else AMARILLO if vida_porcentaje > 0.2 else ROJO
        
        pygame.draw.rect(ventana, GRIS_OSCURO, (240, 270, 200, 15), 0, 5)
        pygame.draw.rect(ventana, color_vida, (240, 270, int(200 * vida_porcentaje), 15), 0, 5)
        
        ventana.blit(fuente_pequena.render(f"PS: {self.mi_pokemon.ps_actual}/{self.mi_pokemon.stats_actuales['ps']}", True, NEGRO), 
                    (240, 290))

        if self.estado_actual == "MENU":
            menu_ancho = 340
            menu_alto = 100
            menu_x = self.ancho - menu_ancho - 40
            menu_y = self.alto - menu_alto - 50
            
            pygame.draw.rect(ventana, BLANCO, (menu_x, menu_y, menu_ancho, menu_alto), 0, 10)
            pygame.draw.rect(ventana, GRIS_OSCURO, (menu_x, menu_y, menu_ancho, menu_alto), 3, 10)
            
            pygame.draw.line(ventana, GRIS_OSCURO, 
                           (menu_x + menu_ancho // 2, menu_y), 
                           (menu_x + menu_ancho // 2, menu_y + menu_alto), 3)
            
            pygame.draw.line(ventana, GRIS_OSCURO, 
                           (menu_x, menu_y + menu_alto // 2), 
                           (menu_x + menu_ancho, menu_y + menu_alto // 2), 3)
            
            posiciones = [
                (menu_x + 30, menu_y + 15),
                (menu_x + menu_ancho // 2 + 30, menu_y + 15),
                (menu_x + 30, menu_y + menu_alto // 2 + 15),
                (menu_x + menu_ancho // 2 + 30, menu_y + menu_alto // 2 + 15)
            ]
            
            for i, opcion in enumerate(self.opciones_menu):
                color = AZUL if i == self.opcion_actual else NEGRO
                ventana.blit(fuente_normal.render(opcion, True, color), posiciones[i])

        elif self.estado_actual == "ATAQUES":
            pygame.draw.rect(ventana, BLANCO, (40, self.alto - 160, self.ancho - 80, 110), 0, 10)
            pygame.draw.rect(ventana, GRIS_OSCURO, (40, self.alto - 160, self.ancho - 80, 110), 3, 10)
            
            ventana.blit(fuente_grande.render("Elegir ataque:", True, AZUL), (60, self.alto - 140))
            
            for i, ataque in enumerate(self.mi_pokemon.movimientos):
                color = AZUL if i == self.opcion_actual else NEGRO
                ventana.blit(fuente_normal.render(f"{i+1}. {ataque['nombre']}", True, color), 
                           (60, self.alto - 110 + i * 30))

        elif self.estado_actual == "POKEMON":
            pygame.draw.rect(ventana, BLANCO, (80, 80, self.ancho - 160, self.alto - 160), 0, 15)
            pygame.draw.rect(ventana, GRIS_OSCURO, (80, 80, self.ancho - 160, self.alto - 160), 3, 15)
            
            ventana.blit(fuente_grande.render("Elige un Pokémon:", True, AZUL), (100, 100))
            
            y = 140
            for i, pokemon in enumerate(self.jugador.equipo_pokemon):
                if pokemon == self.mi_pokemon:
                    estado = "EN BATALLA"
                    color_estado = AZUL
                elif pokemon.esta_debilitado():
                    estado = "DEBILITADO"
                    color_estado = ROJO
                else:
                    estado = f"PS: {pokemon.ps_actual}/{pokemon.stats_actuales['ps']}"
                    color_estado = VERDE
                
                color_nombre = AZUL if i == self.opcion_actual else NEGRO
                
                ventana.blit(fuente_normal.render(f"{i+1}. {pokemon.nombre} Nv{pokemon.nivel}", True, color_nombre), (100, y))
                ventana.blit(fuente_pequena.render(estado, True, color_estado), (120, y + 25))
                y += 60
            
            ventana.blit(fuente_pequena.render("↑↓ Navegar | ENTER Cambiar | ESC Volver", True, GRIS_OSCURO), 
                        (100, self.alto - 120))

        elif self.estado_actual == "BOLSA":
            pygame.draw.rect(ventana, BLANCO, (80, 80, self.ancho - 160, self.alto - 160), 0, 15)
            pygame.draw.rect(ventana, GRIS_OSCURO, (80, 80, self.ancho - 160, self.alto - 160), 3, 15)
            
            ventana.blit(fuente_grande.render("Tu bolsa:", True, AZUL), (100, 100))
            
            tab_y = 140
            tab_width = 150
            for i, categoria in enumerate(self.categorias_bolsa):
                tab_x = 100 + i * (tab_width + 10)
                color_tab = AZUL if categoria == self.categoria_bolsa_actual else GRIS_OSCURO
                
                pygame.draw.rect(ventana, color_tab, (tab_x, tab_y, tab_width, 35), 0, 5)
                pygame.draw.rect(ventana, NEGRO, (tab_x, tab_y, tab_width, 35), 2, 5)
                
                nombre_categoria = categoria.upper()
                ventana.blit(fuente_pequena.render(nombre_categoria, True, BLANCO), (tab_x + 10, tab_y + 10))
            
            y = 190
            objetos_categoria = self.jugador.bolsa[self.categoria_bolsa_actual]
            
            if objetos_categoria:
                for i, (objeto_key, cantidad) in enumerate(objetos_categoria.items()):
                    if objeto_key in self.jugador.objects_data:
                        objeto = self.jugador.objects_data[objeto_key]
                        color = AZUL if i == self.opcion_actual else NEGRO
                        
                        ventana.blit(fuente_normal.render(f"{objeto['nombre']} x{cantidad}", True, color), (100, y))
                        ventana.blit(fuente_pequena.render(objeto['descripcion'], True, NEGRO), (120, y + 25))
                        y += 60
            else:
                ventana.blit(fuente_normal.render("No hay objetos en esta categoría", True, GRIS_OSCURO), (100, 190))
            
            ventana.blit(fuente_pequena.render("◄► Cambiar categoría | ↑↓ Navegar | ENTER Usar | ESC Volver", True, GRIS_OSCURO), 
                        (100, self.alto - 120))

        if self.estado_actual != "ATAQUES":
            menu_ancho = 340
            menu_x = self.ancho - menu_ancho - 40
            
            #Cambiar esto para que se modifique el tamaño del cuadro de dialogo de texto
            dialogo_ancho = menu_x - 41
            dialogo_alto = 100
            dialogo_x = 40
            dialogo_y = self.alto - dialogo_alto - 50
            
            pygame.draw.rect(ventana, BLANCO, (dialogo_x, dialogo_y, dialogo_ancho, dialogo_alto), 0, 10)
            pygame.draw.rect(ventana, GRIS_OSCURO, (dialogo_x, dialogo_y, dialogo_ancho, dialogo_alto), 3, 10)
            
            if self.mensaje:
                ventana.blit(fuente_normal.render(self.mensaje, True, NEGRO), (dialogo_x + 20, dialogo_y + 30))
            
            if self.estado_actual == "MENSAJE":
                ventana.blit(fuente_pequena.render("Presiona ENTER", True, GRIS_OSCURO), (dialogo_x + 20, dialogo_y + 60))
            elif self.estado_actual == "MENU":
                ventana.blit(fuente_pequena.render("Elige una acción", True, GRIS_OSCURO), (dialogo_x + 20, dialogo_y + 60))
        
        if self.resultado_batalla:
            overlay = pygame.Surface((self.ancho, self.alto))
            overlay.set_alpha(180)
            overlay.fill(NEGRO)
            ventana.blit(overlay, (0, 0))
            
            if self.resultado_batalla == "VICTORIA":
                texto = "¡VICTORIA!"
                color_texto = VERDE
            elif self.resultado_batalla == "DERROTA":
                texto = "DERROTA"
                color_texto = ROJO
            elif self.resultado_batalla == "ESCAPADO":
                texto = "¡ESCAPASTE!"
                color_texto = AMARILLO
            elif self.resultado_batalla == "CAPTURA":
                texto = f"¡CAPTURASTE A {self.pokemon_enemigo.nombre.upper()}!"
                color_texto = AMARILLO
            
            fuente_resultado = pygame.font.SysFont("Arial", 60, bold=True)
            texto_surface = fuente_resultado.render(texto, True, color_texto)
            texto_rect = texto_surface.get_rect(center=(self.ancho // 2, self.alto // 2))
            
            sombra = fuente_resultado.render(texto, True, NEGRO)
            sombra_rect = sombra.get_rect(center=(self.ancho // 2 + 4, self.alto // 2 + 4))
            ventana.blit(sombra, sombra_rect)
            
            ventana.blit(texto_surface, texto_rect)

    def terminar_batalla(self):
        """Termina la batalla y limpia todo"""
        self.activo = False
        self.mi_pokemon = None
        self.pokemon_enemigo = None
        self.jugador = None
        self.mensaje = ""
        self.estado_actual = "MENSAJE"
        self.animacion_activa = False
        self.animacion_frame = 0
        self.resultado_batalla = None
        self.frames_resultado = 0