import pygame

class BatallaUI:
    """Maneja toda la interfaz visual de la batalla"""
    
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        
        # Fuentes (sin anti-aliasing para efecto retro)
        self.fuente_grande = pygame.font.Font(None, 28)
        self.fuente_normal = pygame.font.Font(None, 22)
        self.fuente_pequena = pygame.font.Font(None, 18)
        
        # Colores estilo Pokémon GBA
        self.color_fondo = (248, 248, 248)
        self.color_fondo_sombra = (200, 200, 192)
        
        # Bordes
        self.color_borde_externo = (0, 0, 0)
        self.color_borde_claro = (248, 248, 248)
        self.color_borde_medio = (104, 104, 104)
        self.color_borde_oscuro = (56, 56, 56)
        
        # Texto
        self.color_texto = (80, 80, 80)
        self.color_texto_claro = (120, 120, 120)
        
        # HP
        self.color_hp_verde = (80, 200, 80)
        self.color_hp_amarillo = (240, 200, 60)
        self.color_hp_rojo = (220, 80, 80)
        self.color_hp_fondo = (200, 200, 192)
        self.color_hp_borde = (104, 104, 104)
        
        # Selecciones (diferentes por estado)
        self.color_menu_sel = (200, 120, 120)  # Rojo
        self.color_menu_sel_borde = (160, 80, 80)
        
        self.color_ataques_sel = (120, 160, 200)  # Azul
        self.color_ataques_sel_borde = (80, 120, 160)
        
        self.color_pokemon_sel = (160, 220, 160)  # Verde
        self.color_pokemon_sel_borde = (100, 180, 100)
        
        self.color_bolsa_sel = (240, 200, 120)  # Amarillo
        self.color_bolsa_sel_borde = (200, 160, 80)
        
        self.pixel = 4
        
        # Cache de sprites
        self.sprites_cargados = {}
        self.sprites_fallidos = set()
        
        # Cargar fondo
        self.fondo_batalla = self._cargar_fondo()
    
    def _cargar_fondo(self):
        """Carga el fondo de batalla"""
        rutas = ['assets/images/capaz.png', 'images/capaz.png']
        
        for ruta in rutas:
            try:
                fondo = pygame.image.load(ruta).convert()
                return pygame.transform.scale(fondo, (self.ancho, self.alto))
            except:
                continue
        
        return None
    
    def cargar_sprite_pokemon(self, pokemon, es_enemigo=True):
        """Carga el sprite de un Pokémon con cache"""
        ruta = pokemon.obtener_ruta_sprite(es_enemigo)
        
        if ruta in self.sprites_cargados:
            return self.sprites_cargados[ruta]
        
        if ruta in self.sprites_fallidos:
            return self._crear_placeholder(pokemon, es_enemigo)
        
        try:
            sprite = pygame.image.load(ruta)
            sprite = pygame.transform.scale(sprite, (120, 120))
            self.sprites_cargados[ruta] = sprite
            return sprite
        except:
            self.sprites_fallidos.add(ruta)
            placeholder = self._crear_placeholder(pokemon, es_enemigo)
            self.sprites_cargados[ruta] = placeholder
            return placeholder
    
    def _crear_placeholder(self, pokemon, es_enemigo):
        """Crea un placeholder para sprites faltantes"""
        placeholder = pygame.Surface((120, 120))
        placeholder.fill((240, 200, 120))
        pygame.draw.rect(placeholder, self.color_borde_externo, (0, 0, 120, 120), 3)
        
        texto = self.fuente_normal.render(pokemon.nombre[:8], False, self.color_texto)
        texto_rect = texto.get_rect(center=(60, 60))
        placeholder.blit(texto, texto_rect)
        
        return placeholder
    
    def _dibujar_borde_gba(self, superficie, x, y, ancho, alto):
        """Dibuja borde estilo Pokémon GBA"""
        p = self.pixel
        
        # Fondo
        fondo = pygame.Surface((ancho - p * 4, alto - p * 4))
        fondo.fill(self.color_fondo)
        superficie.blit(fondo, (x + p * 2, y + p * 2))
        
        # Sombra interna
        sombra = pygame.Surface((ancho - p * 6, alto - p * 6))
        sombra.fill(self.color_fondo_sombra)
        sombra.set_alpha(30)
        superficie.blit(sombra, (x + p * 4, y + p * 4))
        
        # Borde externo
        pygame.draw.rect(superficie, self.color_borde_externo, (x + p * 2, y, ancho - p * 4, p))
        pygame.draw.rect(superficie, self.color_borde_externo, (x + p * 2, y + alto - p, ancho - p * 4, p))
        pygame.draw.rect(superficie, self.color_borde_externo, (x, y + p * 2, p, alto - p * 4))
        pygame.draw.rect(superficie, self.color_borde_externo, (x + ancho - p, y + p * 2, p, alto - p * 4))
        
        esquinas_ext = [
            (x + p, y + p), (x + ancho - p * 2, y + p),
            (x + p, y + alto - p * 2), (x + ancho - p * 2, y + alto - p * 2)
        ]
        for ex, ey in esquinas_ext:
            pygame.draw.rect(superficie, self.color_borde_externo, (ex, ey, p, p))
        
        # Highlight
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p * 3, y + p, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p, y + p * 3, p, alto - p * 6))
        
        # Sombra
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + p * 3, y + alto - p * 2, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + ancho - p * 2, y + p * 3, p, alto - p * 6))
        
        # Borde medio
        pygame.draw.rect(superficie, self.color_borde_medio, (x + p * 4, y + p * 2, ancho - p * 8, p))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + p * 2, y + p * 4, p, alto - p * 8))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + p * 4, y + alto - p * 3, ancho - p * 8, p))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + ancho - p * 3, y + p * 4, p, alto - p * 8))
        
        esquinas_int = [
            (x + p * 2, y + p * 2), (x + ancho - p * 3, y + p * 2),
            (x + p * 2, y + alto - p * 3), (x + ancho - p * 3, y + alto - p * 3)
        ]
        for ex, ey in esquinas_int:
            pygame.draw.rect(superficie, self.color_borde_medio, (ex, ey, p, p))
    
    def dibujar_fondo(self, ventana):
        """Dibuja el fondo de batalla"""
        if self.fondo_batalla:
            ventana.blit(self.fondo_batalla, (0, 0))
        else:
            ventana.fill((120, 180, 220))
    
    def dibujar_pokemon_enemigo(self, ventana, pokemon, offset_x=0):
        """Dibuja el sprite y info del Pokémon enemigo"""
        sprite = self.cargar_sprite_pokemon(pokemon, es_enemigo=False)
        ventana.blit(sprite, (self.ancho - 295 + offset_x, 170))  
        
        # Info box
        info_x = self.ancho - 490  # 50px más a la izquierda (era -440)
        info_y = 80  # 20px más abajo (era 60)
        info_ancho = 230
        info_alto = 75
        
        self._dibujar_borde_gba(ventana, info_x, info_y, info_ancho, info_alto)
        
        # Nombre y nivel
        texto_nombre = self.fuente_normal.render(f"{pokemon.nombre} Nv{pokemon.nivel}", False, self.color_texto)
        ventana.blit(texto_nombre, (info_x + 15, info_y + 12))
        
        # Barra de vida
        vida_porcentaje = pokemon.ps_actual / pokemon.stats_actuales["ps"]
        color_vida = self._obtener_color_hp(vida_porcentaje)
        
        barra_x = info_x + 15
        barra_y = info_y + 40
        barra_ancho = 180
        barra_alto = 8
        
        pygame.draw.rect(ventana, self.color_hp_fondo, (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(ventana, self.color_hp_borde, (barra_x, barra_y, barra_ancho, barra_alto), 1)
        
        if vida_porcentaje > 0:
            pygame.draw.rect(ventana, color_vida, (barra_x + 1, barra_y + 1, int((barra_ancho - 2) * vida_porcentaje), barra_alto - 2))
    
    def dibujar_pokemon_jugador(self, ventana, pokemon, offset_x=0):
        """Dibuja el sprite y info del Pokémon del jugador"""
        # Calcular posición: muy cerca del menú sin colisionar
        interfaz_alto = 130
        interfaz_y = self.alto - interfaz_alto
        sprite_y = interfaz_y - 120 - 5  # Solo 5px de separación del menú
        
        sprite = self.cargar_sprite_pokemon(pokemon, es_enemigo=True)
        ventana.blit(sprite, (60 + offset_x, sprite_y))
        
        # Info box (más a la derecha)
        info_x = 280  # 60px más a la derecha que la posición original (era 220)
        info_y = sprite_y
        info_ancho = 280
        info_alto = 95
        
        self._dibujar_borde_gba(ventana, info_x, info_y, info_ancho, info_alto)
        
        # Nombre y nivel
        texto_nombre = self.fuente_normal.render(f"{pokemon.nombre} Nv{pokemon.nivel}", False, self.color_texto)
        ventana.blit(texto_nombre, (info_x + 15, info_y + 12))
        
        # Barra de vida
        vida_porcentaje = pokemon.ps_actual / pokemon.stats_actuales["ps"]
        color_vida = self._obtener_color_hp(vida_porcentaje)
        
        barra_x = info_x + 15
        barra_y = info_y + 40
        barra_ancho = 220
        barra_alto = 10
        
        pygame.draw.rect(ventana, self.color_hp_fondo, (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(ventana, self.color_hp_borde, (barra_x, barra_y, barra_ancho, barra_alto), 1)
        
        if vida_porcentaje > 0:
            pygame.draw.rect(ventana, color_vida, (barra_x + 1, barra_y + 1, int((barra_ancho - 2) * vida_porcentaje), barra_alto - 2))
        
        # PS numéricos
        texto_ps = self.fuente_pequena.render(f"PS: {pokemon.ps_actual}/{pokemon.stats_actuales['ps']}", False, self.color_texto)
        ventana.blit(texto_ps, (barra_x, barra_y + 18))
    
    def _obtener_color_hp(self, porcentaje):
        """Determina color de HP según porcentaje"""
        if porcentaje > 0.5:
            return self.color_hp_verde
        elif porcentaje > 0.2:
            return self.color_hp_amarillo
        else:
            return self.color_hp_rojo

    def dibujar_estado_actual(self, ventana, estado_actual, datos_estado):
        """Dibuja la interfaz según el estado actual"""
        if estado_actual == "MENU":
            self._dibujar_estado_menu(ventana, datos_estado)
        elif estado_actual == "MENSAJE":
            self._dibujar_estado_mensaje(ventana, datos_estado)
        elif estado_actual == "ATAQUES":
            self._dibujar_estado_ataques(ventana, datos_estado)
        elif estado_actual == "POKEMON":
            self._dibujar_estado_pokemon(ventana, datos_estado)
        elif estado_actual == "BOLSA":
            self._dibujar_estado_bolsa(ventana, datos_estado)

    def _dibujar_estado_menu(self, ventana, datos):
        """Dibuja el estado MENU (rojo)"""
        opciones = datos["opciones"]
        opcion_actual = datos["opcion_actual"]
        
        interfaz_alto = 130
        interfaz_y = self.alto - interfaz_alto
        
        contenedor_ancho = self.ancho - 40
        contenedor_alto = interfaz_alto - 20
        contenedor_x = 20
        contenedor_y = interfaz_y + 10
        
        # Contenedor principal
        self._dibujar_borde_gba(ventana, contenedor_x, contenedor_y, contenedor_ancho, contenedor_alto)
        
        # Texto
        panel_texto_ancho = int(contenedor_ancho * 2/3)
        texto_pregunta = self.fuente_normal.render("Que deberia hacer?", False, self.color_texto)
        ventana.blit(texto_pregunta, (contenedor_x + 20, contenedor_y + 20))
        
        instrucciones = self.fuente_pequena.render("Z: Aceptar  X: Volver", False, self.color_texto_claro)
        ventana.blit(instrucciones, (contenedor_x + 20, contenedor_y + contenedor_alto - 25))
        
        # División
        division_x = contenedor_x + panel_texto_ancho
        pygame.draw.line(ventana, self.color_borde_medio, 
                        (division_x, contenedor_y), 
                        (division_x, contenedor_y + contenedor_alto), 2)
        
        # Botones 2x2
        panel_botones_ancho = contenedor_ancho - panel_texto_ancho
        boton_ancho = panel_botones_ancho // 2
        boton_alto = contenedor_alto // 2
        
        linea_vertical_x = division_x + boton_ancho
        linea_horizontal_y = contenedor_y + boton_alto
        
        pygame.draw.line(ventana, self.color_borde_medio,
                        (division_x, linea_horizontal_y),
                        (division_x + panel_botones_ancho, linea_horizontal_y), 2)
        
        pygame.draw.line(ventana, self.color_borde_medio,
                        (linea_vertical_x, contenedor_y),
                        (linea_vertical_x, contenedor_y + contenedor_alto), 2)
        
        # Dibujar opciones
        for i, opcion in enumerate(opciones):
            fila = i // 2
            columna = i % 2
            
            boton_x = division_x + (columna * boton_ancho)
            boton_y = contenedor_y + (fila * boton_alto)
            
            centro_x = boton_x + boton_ancho // 2
            centro_y = boton_y + boton_alto // 2
            
            # Fondo seleccionado (rojo) con más margen
            if i == opcion_actual:
                margen_sel = 8
                pygame.draw.rect(ventana, self.color_menu_sel, 
                                (boton_x + margen_sel, boton_y + margen_sel, 
                                boton_ancho - margen_sel * 2, boton_alto - margen_sel * 2), 
                                border_radius=4)
                pygame.draw.rect(ventana, self.color_menu_sel_borde, 
                                (boton_x + margen_sel, boton_y + margen_sel, 
                                boton_ancho - margen_sel * 2, boton_alto - margen_sel * 2), 
                                2, border_radius=4)
            
            texto = self.fuente_normal.render(opcion, False, self.color_texto)
            texto_rect = texto.get_rect(center=(centro_x, centro_y))
            ventana.blit(texto, texto_rect)

    def _dibujar_estado_mensaje(self, ventana, datos):
        """Dibuja el estado MENSAJE"""
        mensaje = datos["mensaje"]
        
        interfaz_alto = 130
        interfaz_y = self.alto - interfaz_alto
        
        contenedor_ancho = self.ancho - 40
        contenedor_alto = interfaz_alto - 20
        contenedor_x = 20
        contenedor_y = interfaz_y + 10
        
        self._dibujar_borde_gba(ventana, contenedor_x, contenedor_y, contenedor_ancho, contenedor_alto)
        
        # Texto multilínea
        if mensaje:
            palabras = mensaje.split()
            lineas = []
            linea_actual = ""
            
            for palabra in palabras:
                prueba_linea = f"{linea_actual} {palabra}".strip()
                if self.fuente_normal.size(prueba_linea)[0] < contenedor_ancho - 40:
                    linea_actual = prueba_linea
                else:
                    if linea_actual:
                        lineas.append(linea_actual)
                    linea_actual = palabra
            
            if linea_actual:
                lineas.append(linea_actual)
            
            for i, linea in enumerate(lineas[:3]):
                texto_linea = self.fuente_normal.render(linea, False, self.color_texto)
                ventana.blit(texto_linea, (contenedor_x + 20, contenedor_y + 20 + i * 25))
        
        indicador = self.fuente_pequena.render("Presiona Z para continuar", False, self.color_texto_claro)
        ventana.blit(indicador, (contenedor_x + 20, contenedor_y + contenedor_alto - 25))

    def _dibujar_estado_ataques(self, ventana, datos):
        """Dibuja el estado ATAQUES (azul)"""
        movimientos = datos.get("movimientos", []) or []
        opcion_actual = datos.get("opcion_actual", 0) or 0

        if not isinstance(opcion_actual, int):
            try:
                opcion_actual = int(opcion_actual)
            except:
                opcion_actual = 0
        if opcion_actual < 0:
            opcion_actual = 0
        if movimientos and opcion_actual >= len(movimientos):
            opcion_actual = len(movimientos) - 1

        interfaz_alto = 160
        interfaz_y = self.alto - interfaz_alto

        contenedor_ancho = self.ancho - 40
        contenedor_alto = interfaz_alto - 20
        contenedor_x = 20
        contenedor_y = interfaz_y + 10

        self._dibujar_borde_gba(ventana, contenedor_x, contenedor_y, contenedor_ancho, contenedor_alto)

        # Panel movimientos
        panel_movimientos_ancho = int(contenedor_ancho * 2/3)
        division_x = contenedor_x + panel_movimientos_ancho
        
        pygame.draw.line(ventana, self.color_borde_medio,
                            (division_x, contenedor_y),
                            (division_x, contenedor_y + contenedor_alto), 2)

        # Cuadrícula 2x2
        boton_ancho = panel_movimientos_ancho // 2
        boton_alto = contenedor_alto // 2

        linea_vertical_x = contenedor_x + boton_ancho
        linea_horizontal_y = contenedor_y + boton_alto

        pygame.draw.line(ventana, self.color_borde_medio,
                            (contenedor_x, linea_horizontal_y),
                            (contenedor_x + panel_movimientos_ancho, linea_horizontal_y), 2)

        pygame.draw.line(ventana, self.color_borde_medio,
                            (linea_vertical_x, contenedor_y),
                            (linea_vertical_x, contenedor_y + contenedor_alto), 2)

        # Dibujar movimientos
        for i in range(4):
            fila = i // 2
            columna = i % 2

            mov_x = contenedor_x + (columna * boton_ancho)
            mov_y = contenedor_y + (fila * boton_alto)

            centro_x = mov_x + boton_ancho // 2
            centro_y = mov_y + boton_alto // 2

            # Fondo seleccionado (azul) con más margen
            if i == opcion_actual:
                margen_sel = 8
                pygame.draw.rect(ventana, self.color_ataques_sel, 
                               (mov_x + margen_sel, mov_y + margen_sel, 
                                boton_ancho - margen_sel * 2, boton_alto - margen_sel * 2),
                               border_radius=4)
                pygame.draw.rect(ventana, self.color_ataques_sel_borde, 
                               (mov_x + margen_sel, mov_y + margen_sel, 
                                boton_ancho - margen_sel * 2, boton_alto - margen_sel * 2), 
                               2, border_radius=4)

            if i < len(movimientos) and isinstance(movimientos[i], dict):
                nombre_movimiento = movimientos[i].get('nombre', '---')
                texto = self.fuente_normal.render(nombre_movimiento[:12], False, self.color_texto)
            else:
                texto = self.fuente_normal.render("-------", False, self.color_texto_claro)

            texto_rect = texto.get_rect(center=(centro_x, centro_y))
            ventana.blit(texto, texto_rect)

        # Panel de información
        panel_info_x = division_x + 15
        panel_info_y = contenedor_y + 15

        if movimientos and 0 <= opcion_actual < len(movimientos) and isinstance(movimientos[opcion_actual], dict):
            movimiento = movimientos[opcion_actual]

            tipo = movimiento.get('tipo', '—')
            texto_tipo = self.fuente_normal.render(f"Tipo: {tipo}", False, self.color_texto)
            ventana.blit(texto_tipo, (panel_info_x, panel_info_y))

            pp_max = movimiento.get('pp', 0) or 0
            pp_actual = movimiento.get('pp_actual', pp_max)
            try:
                pp_actual = int(pp_actual)
            except:
                pp_actual = pp_max
            texto_pp = self.fuente_normal.render(f"PP: {pp_actual}/{pp_max}", False, self.color_texto)
            ventana.blit(texto_pp, (panel_info_x, panel_info_y + 25))

            descripcion = movimiento.get('descripcion', '') or ''
            if descripcion:
                palabras = descripcion.split()
                lineas = []
                linea_actual = ""

                max_width = contenedor_ancho - panel_movimientos_ancho - 40
                for palabra in palabras:
                    prueba_linea = f"{linea_actual} {palabra}".strip()
                    if self.fuente_pequena.size(prueba_linea)[0] < max_width:
                        linea_actual = prueba_linea
                    else:
                        if linea_actual:
                            lineas.append(linea_actual)
                        linea_actual = palabra
                if linea_actual:
                    lineas.append(linea_actual)

                for idx, linea in enumerate(lineas[:4]):
                    texto_desc = self.fuente_pequena.render(linea, False, self.color_texto_claro)
                    ventana.blit(texto_desc, (panel_info_x, panel_info_y + 60 + idx * 18))

    def _dibujar_estado_pokemon(self, ventana, datos):
        """Dibuja el estado POKEMON con rejilla 2x3 centrada (verde)"""
        equipo_pokemon = datos["equipo_pokemon"]
        pokemon_actual = datos["pokemon_actual"]
        opcion_actual = datos["opcion_actual"]
    
        # Overlay
        overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        ventana.blit(overlay, (0, 0))
    
        # Rejilla 2x3 centrada
        casilla_ancho = 200
        casilla_alto = 140
        espacio = 20
        
        # Calcular ancho y alto total de la rejilla
        rejilla_ancho_total = 3 * casilla_ancho + 2 * espacio
        rejilla_alto_total = 2 * casilla_alto + espacio
        
        # Centrar la rejilla
        margen_x = (self.ancho - rejilla_ancho_total) // 2
        margen_y = (self.alto - rejilla_alto_total) // 2
    
        # Dibujar rejilla
        for i in range(6):
            fila = i // 3
            columna = i % 3
        
            x = margen_x + columna * (casilla_ancho + espacio)
            y = margen_y + fila * (casilla_alto + espacio)
        
            # Selección (verde)
            if i == opcion_actual:
                pygame.draw.rect(ventana, self.color_pokemon_sel, (x, y, casilla_ancho, casilla_alto), 0, 8)
                pygame.draw.rect(ventana, self.color_pokemon_sel_borde, (x, y, casilla_ancho, casilla_alto), 3, 8)
            else:
                self._dibujar_borde_gba(ventana, x, y, casilla_ancho, casilla_alto)
        
            if i < len(equipo_pokemon):
                pokemon = equipo_pokemon[i]
            
                # Sprite
                sprite = self.cargar_sprite_pokemon(pokemon, es_enemigo=False)
                sprite = pygame.transform.scale(sprite, (64, 64))
                ventana.blit(sprite, (x + (casilla_ancho - 64) // 2, y + 10))
            
                # Nombre y nivel
                texto_nombre = self.fuente_normal.render(pokemon.nombre, False, self.color_texto)
                ventana.blit(texto_nombre, (x + 10, y + 80))
            
                texto_nivel = self.fuente_pequena.render(f"Lv.{pokemon.nivel}", False, self.color_texto_claro)
                ventana.blit(texto_nivel, (x + casilla_ancho - 50, y + 80))
            
                # Barra HP
                vida_porcentaje = pokemon.ps_actual / pokemon.stats_actuales["ps"]
                color_vida = self._obtener_color_hp(vida_porcentaje)
            
                barra_ancho = casilla_ancho - 20
                barra_x = x + 10
                barra_y = y + 100
            
                pygame.draw.rect(ventana, self.color_hp_fondo, (barra_x, barra_y, barra_ancho, 8))
                pygame.draw.rect(ventana, self.color_hp_borde, (barra_x, barra_y, barra_ancho, 8), 1)
                
                if vida_porcentaje > 0:
                    pygame.draw.rect(ventana, color_vida, (barra_x + 1, barra_y + 1, int((barra_ancho - 2) * vida_porcentaje), 6))
            
                # HP numérico
                texto_hp = self.fuente_pequena.render(f"{pokemon.ps_actual}/{pokemon.stats_actuales['ps']}", False, self.color_texto_claro)
                ventana.blit(texto_hp, (x + 10, y + 112))
            
                # Estado
                if pokemon == pokemon_actual:
                    texto_estado = self.fuente_pequena.render("BATALLA", False, self.color_ataques_sel_borde)
                    ventana.blit(texto_estado, (x + casilla_ancho - 55, y + 112))
                elif pokemon.esta_debilitado():
                    texto_estado = self.fuente_pequena.render("DEBIL", False, self.color_hp_rojo)
                    ventana.blit(texto_estado, (x + casilla_ancho - 45, y + 112))
            else:
                texto_vacio = self.fuente_normal.render("--- VACIO ---", False, self.color_texto_claro)
                ventana.blit(texto_vacio, (x + casilla_ancho // 2 - 50, y + casilla_alto // 2 - 10))
    
        # Instrucciones
        instrucciones = self.fuente_pequena.render("Z: Cambiar Pokemon  |  X: Volver", False, self.color_fondo)
        ventana.blit(instrucciones, (margen_x, self.alto - 30))

    def _dibujar_estado_bolsa(self, ventana, datos):
        """Dibuja el estado BOLSA con overlay (amarillo)"""
        bolsa = datos.get("bolsa", {}) or {}
        categorias = datos.get("categorias", []) or []
        categoria_actual = datos.get("categoria_actual", 0) or 0
        opcion_actual = datos.get("opcion_actual", 0) or 0
        objects_data = datos.get("objects_data", {}) or {}
        
        if not isinstance(opcion_actual, int):
            try:
                opcion_actual = int(opcion_actual)
            except:
                opcion_actual = 0
        if opcion_actual < 0:
            opcion_actual = 0
        
        # Overlay
        overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        ventana.blit(overlay, (0, 0))
        
        # Contenedor principal
        contenedor_ancho = 400
        contenedor_alto = 320
        contenedor_x = (self.ancho - contenedor_ancho) // 2
        contenedor_y = (self.alto - contenedor_alto) // 2
        
        self._dibujar_borde_gba(ventana, contenedor_x, contenedor_y, contenedor_ancho, contenedor_alto)
        
        # Título
        titulo = self.fuente_grande.render("TU BOLSA", False, self.color_texto)
        titulo_x = contenedor_x + (contenedor_ancho - titulo.get_width()) // 2
        ventana.blit(titulo, (titulo_x, contenedor_y + 15))
        
        # Línea divisoria
        pygame.draw.line(ventana, self.color_borde_medio,
                        (contenedor_x + 20, contenedor_y + 45),
                        (contenedor_x + contenedor_ancho - 20, contenedor_y + 45), 2)
        
        # Filtrar items usables
        items_usables = {}
        categorias_usables = ["curacion", "captura", "debug"]
        
        for categoria in categorias_usables:
            if categoria in bolsa and isinstance(bolsa[categoria], dict):
                for item_key, cantidad in bolsa[categoria].items():
                    try:
                        cantidad = int(cantidad) if cantidad else 0
                    except:
                        cantidad = 0
                    
                    if cantidad > 0 and item_key in objects_data:
                        item_data = objects_data[item_key]
                        if isinstance(item_data, dict):
                            items_usables[item_key] = {
                                'data': item_data,
                                'cantidad': cantidad
                            }
        
        items_lista = list(items_usables.keys())
        
        if items_lista and opcion_actual >= len(items_lista):
            opcion_actual = len(items_lista) - 1
        
        # Lista de items
        lista_x = contenedor_x + 20
        lista_y = contenedor_y + 60
        item_alto = 30
        max_items_visibles = 6
        
        inicio = max(0, min(opcion_actual, len(items_lista) - max_items_visibles)) if items_lista else 0
        fin = min(len(items_lista), inicio + max_items_visibles) if items_lista else 0
        
        for i in range(inicio, fin):
            if i >= len(items_lista):
                break
            
            item_key = items_lista[i]
            if item_key not in items_usables:
                continue
            
            item_info = items_usables[item_key]
            item_data = item_info.get('data', {})
            cantidad = item_info.get('cantidad', 0)
            
            pos_y = lista_y + (i - inicio) * item_alto
            
            # Selección (amarillo)
            if i == opcion_actual:
                pygame.draw.rect(ventana, self.color_bolsa_sel, 
                               (lista_x - 5, pos_y - 2, contenedor_ancho - 40, item_alto - 2))
                pygame.draw.rect(ventana, self.color_bolsa_sel_borde, 
                               (lista_x - 5, pos_y - 2, contenedor_ancho - 40, item_alto - 2), 2)
                color_texto = self.color_texto
                indicador = self.fuente_pequena.render(">", False, self.color_texto)
                ventana.blit(indicador, (lista_x - 15, pos_y + 5))
            else:
                color_texto = self.color_texto
            
            # Nombre
            nombre_item = item_data.get('nombre', '---')
            texto_nombre = self.fuente_normal.render(str(nombre_item)[:30], False, color_texto)
            ventana.blit(texto_nombre, (lista_x, pos_y + 5))
            
            # Cantidad
            texto_cantidad = self.fuente_normal.render(f"x{cantidad}", False, color_texto)
            cantidad_x = contenedor_x + contenedor_ancho - 50
            ventana.blit(texto_cantidad, (cantidad_x, pos_y + 5))
        
        # Panel de descripción
        desc_panel_y = contenedor_y + contenedor_alto - 75
        desc_panel_alto = 55
        
        pygame.draw.rect(ventana, self.color_fondo_sombra, 
                        (contenedor_x + 15, desc_panel_y, contenedor_ancho - 30, desc_panel_alto))
        pygame.draw.rect(ventana, self.color_borde_medio, 
                        (contenedor_x + 15, desc_panel_y, contenedor_ancho - 30, desc_panel_alto), 2)
        
        # Descripción
        if items_lista and 0 <= opcion_actual < len(items_lista):
            item_seleccionado_key = items_lista[opcion_actual]
            if item_seleccionado_key in items_usables:
                item_seleccionado = items_usables[item_seleccionado_key].get('data', {})
                descripcion = item_seleccionado.get('descripcion', '') or ''
                
                if descripcion:
                    palabras = descripcion.split()
                    lineas = []
                    linea_actual = ""
                    
                    for palabra in palabras:
                        prueba_linea = f"{linea_actual} {palabra}".strip()
                        if self.fuente_pequena.size(prueba_linea)[0] < contenedor_ancho - 60:
                            linea_actual = prueba_linea
                        else:
                            if linea_actual:
                                lineas.append(linea_actual)
                            linea_actual = palabra
                    
                    if linea_actual:
                        lineas.append(linea_actual)
                    
                    for j, linea in enumerate(lineas[:2]):
                        texto_desc = self.fuente_pequena.render(linea, False, self.color_texto)
                        ventana.blit(texto_desc, (contenedor_x + 25, desc_panel_y + 10 + j * 18))
                else:
                    texto_sin_desc = self.fuente_pequena.render("Sin descripcion", False, self.color_texto_claro)
                    ventana.blit(texto_sin_desc, (contenedor_x + 25, desc_panel_y + 20))
        else:
            texto_vacio = self.fuente_pequena.render("No hay items usables", False, self.color_texto_claro)
            ventana.blit(texto_vacio, (contenedor_x + 25, desc_panel_y + 20))