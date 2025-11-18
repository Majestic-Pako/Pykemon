import pygame
import random
from core.ui.batalla_ui import BatallaUI


class Batalla:
    """Maneja la lógica de batalla (separada de la UI)"""
    
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.activo = False
        
        # Pokémon en batalla
        self.mi_pokemon = None
        self.pokemon_enemigo = None
        self.jugador = None
        
        # Sistema de menús
        self.opciones_menu = ["ATACAR", "POKEMON", "BOLSA", "HUIR"]
        self.opcion_actual = 0
        self.estado_actual = "MENSAJE"
        self.categoria_bolsa_actual = "curacion"
        self.categorias_bolsa = ["curacion", "captura", "debug"]
        self.indice_categoria = 0
        self.mensaje = ""
        
        # Variables de animación
        self.animacion_activa = False
        self.animacion_tipo = None
        self.animacion_frame = 0
        self.animacion_duracion = 20
        
        # Sistema de captura
        self.captura_en_progreso = False
        self.captura_mensajes = []
        self.captura_indice = 0
        self.captura_exitosa = False
        self.ocultar_enemigo = False
        
        # Sistema de transiciones
        self.transicion_activa = False
        self.transicion_alpha = 0
        self.transicion_estado = None  # "FADE_OUT", "FADE_IN", "FLASH"
        self.transicion_velocidad = 15
        self.transicion_tipo = None  # "batalla", "huir"
        self.flash_counter = 0
        self.flash_max = 4  # Número de parpadeos
        
        # Guardar datos pendientes de batalla
        self.batalla_pendiente_jugador = None
        self.batalla_pendiente_enemigo = None
        
        # UI (separada)
        self.ui = BatallaUI(ancho, alto)
    
    # ==================== SISTEMA DE TRANSICIONES ====================
    
    def iniciar_transicion(self, jugador, pokemon_enemigo):
        """Inicia la transición de entrada a batalla (con flash)"""
        self.transicion_activa = True
        self.transicion_alpha = 0
        self.transicion_estado = "FLASH"
        self.transicion_tipo = "batalla"
        self.flash_counter = 0
        
        # Guardar datos para después del flash
        self.batalla_pendiente_jugador = jugador
        self.batalla_pendiente_enemigo = pokemon_enemigo
    
    def iniciar_transicion_huir(self):
        """Inicia la transición de salida (fade out simple)"""
        self.transicion_activa = True
        self.transicion_alpha = 0
        self.transicion_estado = "FADE_OUT"
        self.transicion_tipo = "huir"
    
    def actualizar_transicion(self):
        """Actualiza el fade de transición"""
        if not self.transicion_activa:
            return
        
        if self.transicion_tipo == "batalla":
            # Animación de encuentro (flash blanco)
            if self.transicion_estado == "FLASH":
                self.flash_counter += 1
                
                # Alternar entre blanco y transparente
                if self.flash_counter % 8 < 4:
                    self.transicion_alpha = 255
                else:
                    self.transicion_alpha = 0
                
                # Después de varios flashes, hacer fade in normal
                if self.flash_counter >= (self.flash_max * 8):
                    self.empezar_batalla(
                        self.batalla_pendiente_jugador,
                        self.batalla_pendiente_enemigo
                    )
                    self.transicion_estado = "FADE_IN"
                    self.transicion_alpha = 255
            
            elif self.transicion_estado == "FADE_IN":
                # Aclarar pantalla después del encuentro
                self.transicion_alpha -= self.transicion_velocidad
                
                if self.transicion_alpha <= 0:
                    self.transicion_alpha = 0
                    self.transicion_activa = False
                    self.transicion_estado = None
        
        elif self.transicion_tipo == "huir":
            # Animación de huida (fade out)
            if self.transicion_estado == "FADE_OUT":
                self.transicion_alpha += self.transicion_velocidad
                
                if self.transicion_alpha >= 255:
                    self.transicion_alpha = 255
                    # Terminar batalla cuando está completamente oscuro
                    self.terminar_batalla()
                    self.transicion_activa = False
    
    def dibujar_transicion(self, ventana):
        """Dibuja la capa de transición sobre todo"""
        if self.transicion_activa or self.transicion_alpha > 0:
            # Color depende del tipo de transición
            color = (255, 255, 255) if self.transicion_tipo == "batalla" and self.transicion_estado == "FLASH" else (0, 0, 0)
            
            # Crear superficie semi-transparente
            overlay = pygame.Surface((self.ancho, self.alto))
            overlay.fill(color)
            overlay.set_alpha(self.transicion_alpha)
            ventana.blit(overlay, (0, 0))
    
    # ==================== CONTROL DE BATALLA ====================
    
    def empezar_batalla(self, jugador, pokemon_enemigo):
        """Inicia una nueva batalla"""
        self.activo = True
        self.jugador = jugador
        self.mi_pokemon = jugador.obtener_pokemon_activo()
        
        if not self.mi_pokemon:
            self.activo = False
            return
        
        self.pokemon_enemigo = pokemon_enemigo
        
        # Cargar movimientos del enemigo
        if not self.pokemon_enemigo.movimientos:
            self.pokemon_enemigo.cargar_movimientos()
        
        self.mensaje = f"Un {pokemon_enemigo.nombre} salvaje aparecio!"
        self.estado_actual = "MENSAJE"
        self.opcion_actual = 0
        self.indice_categoria = 0
        self.categoria_bolsa_actual = "curacion"
        self.animacion_activa = False
        self.animacion_frame = 0
        
        # Reset captura
        self.captura_en_progreso = False
        self.captura_mensajes = []
        self.captura_indice = 0
        self.captura_exitosa = False
        self.ocultar_enemigo = False
    
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
        self.transicion_activa = False
        self.transicion_alpha = 0
    
    # ==================== ANIMACIONES ====================
    
    def actualizar_animacion(self):
        """Actualiza la animación de ataque"""
        if self.animacion_activa:
            self.animacion_frame += 1
            if self.animacion_frame >= self.animacion_duracion:
                self.animacion_activa = False
                self.animacion_frame = 0
    
    def obtener_offset_animacion(self):
        """Calcula los offsets para animación de ataque"""
        offset_x_jugador = 0
        offset_x_enemigo = 0
        
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
        
        return offset_x_jugador, offset_x_enemigo
    
    # ==================== PROCESAMIENTO DE EVENTOS ====================
    
    def procesar_eventos(self, eventos):
        """Procesa los eventos del teclado"""
        if not self.activo:
            return None

        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                
                if self.estado_actual == "MENSAJE":
                    if evento.key in [pygame.K_RETURN, pygame.K_z]:
                        # Si estamos en secuencia de captura
                        if self.captura_en_progreso:
                            self.captura_indice += 1
                            if self.captura_indice < len(self.captura_mensajes):
                                self.mensaje = self.captura_mensajes[self.captura_indice]
                            else:
                                # Fin de la secuencia
                                self.captura_en_progreso = False
                                self.ocultar_enemigo = False
                                if self.captura_exitosa:
                                    return "CAPTURA"
                                else:
                                    return "TURNO_ENEMIGO"
                        # Mensajes de VICTORIA/DERROTA
                        elif "Ganaste" in self.mensaje or "derrotado" in self.mensaje.lower():
                            self.terminar_batalla()
                            return None
                        elif "fue derrotado" in self.mensaje and self.mi_pokemon.nombre in self.mensaje:
                            self.terminar_batalla()
                            return None
                        else:
                            self.estado_actual = "MENU"
                            self.mensaje = ""
                
                elif self.estado_actual == "POKEMON":
                    return self._manejar_input_pokemon(evento.key)
                
                elif self.estado_actual == "BOLSA":
                    return self._manejar_input_bolsa(evento.key)
                
                elif self.estado_actual == "MENU":
                    return self._manejar_input_menu(evento.key)
                
                elif self.estado_actual == "ATAQUES":
                    return self._manejar_input_ataques(evento.key)
        
        return None
    
    def _manejar_input_menu(self, tecla):
        """Maneja input del menú principal (2x2)"""
        if tecla == pygame.K_UP:
            if self.opcion_actual >= 2:
                self.opcion_actual -= 2
        elif tecla == pygame.K_DOWN:
            if self.opcion_actual <= 1:
                self.opcion_actual += 2
        elif tecla == pygame.K_LEFT:
            if self.opcion_actual % 2 == 1:
                self.opcion_actual -= 1
        elif tecla == pygame.K_RIGHT:
            if self.opcion_actual % 2 == 0:
                self.opcion_actual += 1
        elif tecla in [pygame.K_RETURN, pygame.K_z]:
            return self.ejecutar_accion()
        
        return None
    
    def _manejar_input_ataques(self, tecla):
        """Maneja input del menú de ataques (2x2)"""
        num_movimientos = len(self.mi_pokemon.movimientos)
        
        if tecla == pygame.K_UP:
            if self.opcion_actual >= 2:
                self.opcion_actual -= 2
        elif tecla == pygame.K_DOWN:
            if self.opcion_actual <= 1 and self.opcion_actual + 2 < num_movimientos:
                self.opcion_actual += 2
        elif tecla == pygame.K_LEFT:
            if self.opcion_actual % 2 == 1:
                self.opcion_actual -= 1
        elif tecla == pygame.K_RIGHT:
            if self.opcion_actual % 2 == 0 and self.opcion_actual + 1 < num_movimientos:
                self.opcion_actual += 1
        elif tecla in [pygame.K_RETURN, pygame.K_z]:
            return self.usar_ataque()
        elif tecla == pygame.K_x:
            self.estado_actual = "MENU"
            self.opcion_actual = 0
        
        return None
    
    def _manejar_input_pokemon(self, tecla):
        """Maneja input del menú de Pokémon (2x3 dinámico)"""
        num_pokemon = len(self.jugador.equipo_pokemon)
        
        if tecla == pygame.K_UP:
            nueva_opcion = self.opcion_actual - 3
            if nueva_opcion >= 0:
                self.opcion_actual = nueva_opcion
        elif tecla == pygame.K_DOWN:
            nueva_opcion = self.opcion_actual + 3
            if nueva_opcion < num_pokemon:
                self.opcion_actual = nueva_opcion
        elif tecla == pygame.K_LEFT:
            if self.opcion_actual % 3 != 0:
                self.opcion_actual -= 1
        elif tecla == pygame.K_RIGHT:
            if self.opcion_actual % 3 != 2 and self.opcion_actual < num_pokemon - 1:
                self.opcion_actual += 1
        elif tecla in [pygame.K_RETURN, pygame.K_z]:
            return self.cambiar_pokemon()
        elif tecla == pygame.K_x:
            self.estado_actual = "MENU"
            self.opcion_actual = 0
        
        return None
    
    def _manejar_input_bolsa(self, tecla):
        """Maneja input del menú de bolsa (lista simple)"""
        items_usables = {}
        categorias_usables = ["curacion", "captura", "debug"]
        
        for categoria in categorias_usables:
            if categoria in self.jugador.bolsa:
                for item_key, cantidad in self.jugador.bolsa[categoria].items():
                    if cantidad > 0 and item_key in self.jugador.objects_data:
                        items_usables[item_key] = cantidad
        
        items_lista = list(items_usables.keys())
        
        if tecla == pygame.K_UP:
            if items_lista:
                self.opcion_actual = max(0, self.opcion_actual - 1)
        elif tecla == pygame.K_DOWN:
            if items_lista:
                self.opcion_actual = min(len(items_lista) - 1, self.opcion_actual + 1)
        elif tecla in [pygame.K_RETURN, pygame.K_z]:
            if items_lista and self.opcion_actual < len(items_lista):
                return self.usar_objeto_seleccionado()
        elif tecla in [pygame.K_ESCAPE, pygame.K_x]:
            self.estado_actual = "MENU"
            self.opcion_actual = 0
        
        return None
    
    # ==================== ACCIONES DE BATALLA ====================
    
    def ejecutar_accion(self):
        """Ejecuta la acción seleccionada en el menú principal"""
        accion = self.opciones_menu[self.opcion_actual]
        
        if accion == "ATACAR":
            self.estado_actual = "ATAQUES"
            self.opcion_actual = 0
        
        elif accion == "HUIR":
            # Iniciar transición de huida
            self.mensaje = "Escapaste con exito!"
            self.estado_actual = "MENSAJE"
            self.iniciar_transicion_huir()
            return "ESCAPADO"
        
        elif accion == "BOLSA":
            self.estado_actual = "BOLSA"
            self.opcion_actual = 0
            self.indice_categoria = 0
            self.categoria_bolsa_actual = "curacion"
        
        elif accion == "POKEMON":
            pokemon_disponibles = [p for p in self.jugador.equipo_pokemon if not p.esta_debilitado()]
            if len(pokemon_disponibles) <= 1:
                self.mensaje = "No hay otros Pokemon disponibles"
                self.estado_actual = "MENSAJE"
            else:
                self.estado_actual = "POKEMON"
                self.opcion_actual = 0
        
        return None
    
    def usar_ataque(self):
        """Usa el ataque seleccionado"""
        ataque = self.mi_pokemon.movimientos[self.opcion_actual]
        
        # Verificar PP
        if ataque.get("pp_actual", 0) <= 0:
            self.mensaje = f"{ataque['nombre']} no tiene PP!"
            self.estado_actual = "MENSAJE"
            return None
        
        danio = random.randint(5, 12)
        
        self.animacion_activa = True
        self.animacion_tipo = "ataque_jugador"
        self.animacion_frame = 0
        
        self.pokemon_enemigo.ps_actual -= danio
        ataque["pp_actual"] -= 1  # Reducir PP
        
        self.mensaje = f"{self.mi_pokemon.nombre} uso {ataque['nombre']}!"
        self.estado_actual = "MENSAJE"

        if self.pokemon_enemigo.esta_debilitado():
            self.mensaje = f"El {self.pokemon_enemigo.nombre} enemigo fue derrotado! Ganaste!"
            self.estado_actual = "MENSAJE"
            return "VICTORIA"
        
        return "TURNO_ENEMIGO"
    
    def cambiar_pokemon(self):
        """Cambia al Pokémon seleccionado"""
        pokemon_seleccionado = self.jugador.equipo_pokemon[self.opcion_actual]
        
        if pokemon_seleccionado == self.mi_pokemon:
            self.mensaje = f"{pokemon_seleccionado.nombre} ya esta en batalla!"
            self.estado_actual = "MENSAJE"
            return None
        
        if pokemon_seleccionado.esta_debilitado():
            self.mensaje = f"{pokemon_seleccionado.nombre} esta debilitado!"
            self.estado_actual = "MENSAJE"
            return None
        
        self.mi_pokemon = pokemon_seleccionado
        self.mensaje = f"Adelante, {self.mi_pokemon.nombre}!"
        self.estado_actual = "MENSAJE"
        
        return "CAMBIO_POKEMON"
    
    def usar_objeto_seleccionado(self):
        """Usa el objeto seleccionado de la bolsa"""
        items_usables = {}
        categorias_usables = ["curacion", "captura", "debug"]
    
        for categoria in categorias_usables:
            if categoria in self.jugador.bolsa:
                for item_key, cantidad in self.jugador.bolsa[categoria].items():
                    if cantidad > 0 and item_key in self.jugador.objects_data:
                        items_usables[item_key] = cantidad
    
        items_lista = list(items_usables.keys())
    
        if not items_lista or self.opcion_actual >= len(items_lista):
            self.mensaje = "No hay objetos usables"
            self.estado_actual = "MENSAJE"
            return None
    
        objeto_key = items_lista[self.opcion_actual]
    
        # Usar según categoría
        if objeto_key in self.jugador.bolsa.get("curacion", {}):
            resultado = self.jugador.usar_objeto(objeto_key, self.mi_pokemon)
            self.mensaje = resultado["mensaje"]
            self.estado_actual = "MENSAJE"
            return "TURNO_ENEMIGO"
    
        elif objeto_key in self.jugador.bolsa.get("captura", {}):
            resultado = self.jugador.usar_objeto(objeto_key)
            if resultado["exito"]:
                # Iniciar secuencia de captura
                self.captura_en_progreso = True
                self.captura_indice = 0
                self.ocultar_enemigo = True
                
                # Fórmula de captura con bonus por vida baja
                vida_porcentaje = self.pokemon_enemigo.ps_actual / self.pokemon_enemigo.stats_actuales["ps"]
                bonus_vida = (1 - vida_porcentaje) * 0.3
                
                tasa_base = resultado["tasa_captura"]
                probabilidad_captura = tasa_base + bonus_vida
                
                probabilidad = random.random()
                captura_exitosa = probabilidad < probabilidad_captura
                
                # Crear secuencia de mensajes
                nombre_ball = self.jugador.objects_data[objeto_key]["nombre"]
                self.captura_mensajes = [
                    f"Lanzaste una {nombre_ball}!",
                    f"Golpeo a {self.pokemon_enemigo.nombre}!"
                ]
                
                # Agitaciones (1-3 veces)
                num_agitaciones = random.randint(1, 3)
                for i in range(num_agitaciones):
                    self.captura_mensajes.append("La Pokeball se agita...")
                
                # Resultado final
                if captura_exitosa:
                    self.jugador.agregar_pokemon(self.pokemon_enemigo)
                    self.captura_mensajes.append(f"Capturaste a {self.pokemon_enemigo.nombre}!")
                    self.captura_exitosa = True
                else:
                    self.captura_mensajes.append(f"{self.pokemon_enemigo.nombre} escapo de la ball!")
                    self.captura_exitosa = False
                
                self.mensaje = self.captura_mensajes[0]
                self.estado_actual = "MENSAJE"
                return None
            else:
                self.mensaje = resultado["mensaje"]
                self.estado_actual = "MENSAJE"
    
        elif objeto_key in self.jugador.bolsa.get("debug", {}):
            resultado = self.jugador.usar_objeto(objeto_key, self.mi_pokemon)
            self.mensaje = resultado["mensaje"]
            self.estado_actual = "MENSAJE"
            return "TURNO_ENEMIGO"
        
        return None
    
    def turno_enemigo(self):
        """El enemigo ataca"""
        if self.pokemon_enemigo and not self.pokemon_enemigo.esta_debilitado():
            if not self.pokemon_enemigo.movimientos:
                self.pokemon_enemigo.cargar_movimientos()
            
            # Filtrar movimientos con PP disponible
            movimientos_disponibles = [m for m in self.pokemon_enemigo.movimientos if m.get("pp_actual", 0) > 0]
            
            if not movimientos_disponibles:
                # Sin PP, el enemigo no puede atacar
                self.mensaje = f"{self.pokemon_enemigo.nombre} no tiene PP!"
                self.estado_actual = "MENSAJE"
                return None
            
            self.animacion_activa = True
            self.animacion_tipo = "ataque_enemigo"
            self.animacion_frame = 0
            
            ataque = random.choice(movimientos_disponibles)
            ataque["pp_actual"] -= 1  # Reducir PP
            
            danio = random.randint(3, 10)
            self.mi_pokemon.ps_actual -= danio
            self.mensaje = f"{self.pokemon_enemigo.nombre} uso {ataque['nombre']}!"
            self.estado_actual = "MENSAJE"
            
            if self.mi_pokemon.esta_debilitado():
                self.mensaje = f"{self.mi_pokemon.nombre} fue derrotado! Perdiste..."
                self.estado_actual = "MENSAJE"
                return "DERROTA"
        
        return None
    
    # ==================== RENDERIZADO ====================
    
    def dibujar(self, ventana):
        """Dibuja toda la interfaz de batalla"""
        if not self.activo:
            # Si hay transición pero no hay batalla activa (durante fade out)
            if self.transicion_activa:
                self.dibujar_transicion(ventana)
            return
    
        # Fondo
        self.ui.dibujar_fondo(ventana)
    
        # Obtener offsets de animación
        offset_jugador, offset_enemigo = self.obtener_offset_animacion()
    
        # Pokémon (ocultar enemigo durante captura)
        if not self.ocultar_enemigo:
            self.ui.dibujar_pokemon_enemigo(ventana, self.pokemon_enemigo, offset_enemigo)
        self.ui.dibujar_pokemon_jugador(ventana, self.mi_pokemon, offset_jugador)
    
        # Preparar datos para el estado actual
        datos_estado = {}
    
        if self.estado_actual == "MENU":
            datos_estado = {
                "opciones": self.opciones_menu,
                "opcion_actual": self.opcion_actual,
                "pokemon_activo": self.mi_pokemon
            }
    
        elif self.estado_actual == "MENSAJE":
            datos_estado = {
                "mensaje": self.mensaje
            }
    
        elif self.estado_actual == "ATAQUES":
            datos_estado = {
                "movimientos": self.mi_pokemon.movimientos,
                "opcion_actual": self.opcion_actual
            }
    
        elif self.estado_actual == "POKEMON":
            datos_estado = {
                "equipo_pokemon": self.jugador.equipo_pokemon,
                "pokemon_actual": self.mi_pokemon,
                "opcion_actual": self.opcion_actual
            }
    
        elif self.estado_actual == "BOLSA":
            datos_estado = {
                "bolsa": self.jugador.bolsa,
                "categorias": self.categorias_bolsa,
                "categoria_actual": self.categoria_bolsa_actual,
                "opcion_actual": self.opcion_actual,
                "objects_data": self.jugador.objects_data
            }
    
        # Llamar a la UI para que dibuje el estado correspondiente
        try:
            self.ui.dibujar_estado_actual(ventana, self.estado_actual, datos_estado)
        except Exception as e:
            # Fallback mínimo: dibujar el mensaje si hay problemas en la UI
            if self.estado_actual == "MENSAJE" and self.mensaje:
                try:
                    pygame.draw.rect(ventana, (240,240,240), (20, self.alto-140, self.ancho-40, 120))
                    texto = self.ui.fuente_normal.render(str(self.mensaje), False, self.ui.color_texto)
                    ventana.blit(texto, (40, self.alto-120))
                except:
                    pass

        # Dibujar transición encima de todo (si está activa)
        self.dibujar_transicion(ventana)