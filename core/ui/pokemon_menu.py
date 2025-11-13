import pygame
from core.system.config import *

class PokemonMenu:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        
        self.activo = False
        self.equipo_pokemon = []
        self.pokemon_seleccionado = 0
        
        self.ancho_ventana = 350
        self.margen_derecho = 20
        self.x_ventana = ancho_pantalla - self.ancho_ventana - self.margen_derecho
        
        self.color_fondo = (248, 248, 248)  
        self.color_fondo_sombra = (200, 200, 192)
        
        self.color_borde_externo = (0, 0, 0)
        self.color_borde_claro = (248, 248, 248)
        self.color_borde_medio = (104, 104, 104)
        self.color_borde_oscuro = (56, 56, 56)
        
        self.color_texto = (80, 80, 80)
        self.color_texto_claro = (120, 120, 120)
        self.color_seleccion = (160, 220, 160)  
        self.color_seleccion_borde = (100, 180, 100)  
        
        self.color_ps_verde = (80, 200, 80)
        self.color_ps_amarillo = (240, 200, 60)
        self.color_ps_rojo = (220, 80, 80)
        self.color_ps_fondo = (200, 200, 192)
        self.color_ps_borde = (104, 104, 104)
        
        self.color_sprite_fondo = (232, 232, 224)
        self.color_sprite_borde = (80, 80, 80)
        
        self.fuente_titulo = pygame.font.Font(None, 26)
        self.fuente_nombre = pygame.font.Font(None, 22)
        self.fuente_info = pygame.font.Font(None, 18)
        self.fuente_pequeña = pygame.font.Font(None, 16)
        
        self.pixel = 4
        self.tamaño_sprite = 48
        
        # Cache de sprites
        self.sprites_cargados = {}
        self.sprites_fallidos = set()
        
        self._ultima_tecla = 0
        self.KEY_DELAY = 150
    
    def abrir(self, equipo_pokemon):
        self.activo = True
        self.equipo_pokemon = equipo_pokemon
        self.pokemon_seleccionado = 0
        self._ultima_tecla = pygame.time.get_ticks()
    
    def cerrar(self):
        self.activo = False
    
    def _cargar_sprite_pokemon(self, pokemon):
        """Carga el sprite del Pokémon desde assets/pokemon/front con cache"""
        ruta = f"assets/pokemon/front/{pokemon.id}.png"
        
        # Verificar cache
        if ruta in self.sprites_cargados:
            return self.sprites_cargados[ruta]
        
        # Si ya falló, retornar None
        if ruta in self.sprites_fallidos:
            return None
        
        try:
            sprite = pygame.image.load(ruta)
            # Escalar al tamaño del slot
            sprite = pygame.transform.scale(sprite, (self.tamaño_sprite - 8, self.tamaño_sprite - 8))
            self.sprites_cargados[ruta] = sprite
            return sprite
        except:
            self.sprites_fallidos.add(ruta)
            return None
    
    def _dibujar_borde_pokemon_gba(self, superficie, x, y, ancho, alto):
        p = self.pixel
        
        # Fondo principal
        fondo = pygame.Surface((ancho - p * 4, alto - p * 4))
        fondo.fill(self.color_fondo)
        superficie.blit(fondo, (x + p * 2, y + p * 2))
        
        # Sombra interna
        sombra = pygame.Surface((ancho - p * 6, alto - p * 6))
        sombra.fill(self.color_fondo_sombra)
        sombra.set_alpha(30)
        superficie.blit(sombra, (x + p * 4, y + p * 4))
        
        # === BORDE EXTERNO (Negro) ===
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
        
        # === HIGHLIGHT ===
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p * 3, y + p, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p, y + p * 3, p, alto - p * 6))
        
        # === SOMBRA ===
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + p * 3, y + alto - p * 2, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + ancho - p * 2, y + p * 3, p, alto - p * 6))
        
        # === BORDE MEDIO ===
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
    
    def _obtener_color_ps(self, ps_actual, ps_max):
        porcentaje = ps_actual / ps_max if ps_max > 0 else 0
        if porcentaje > 0.5:
            return self.color_ps_verde
        elif porcentaje > 0.2:
            return self.color_ps_amarillo
        else:
            return self.color_ps_rojo
    
    def _dibujar_pokemon_slot(self, superficie, pokemon, x, y, seleccionado=False):
        slot_alto = 72
        
        if seleccionado:
            rect_sel = pygame.Rect(x - 2, y - 2, self.ancho_ventana - 36, slot_alto)
            pygame.draw.rect(superficie, self.color_seleccion, rect_sel)
            pygame.draw.rect(superficie, self.color_seleccion_borde, rect_sel, 2)
        
        # Sprite del Pokémon
        sprite_x = x + 6
        sprite_y = y + (slot_alto - self.tamaño_sprite) // 2
        
        pygame.draw.rect(superficie, self.color_sprite_fondo, 
                        (sprite_x, sprite_y, self.tamaño_sprite, self.tamaño_sprite))
        pygame.draw.rect(superficie, self.color_sprite_borde, 
                        (sprite_x, sprite_y, self.tamaño_sprite, self.tamaño_sprite), 2)
        pygame.draw.rect(superficie, self.color_borde_claro, 
                        (sprite_x + 2, sprite_y + 2, self.tamaño_sprite - 4, self.tamaño_sprite - 4), 1)
        
        # Intentar cargar sprite real
        sprite = self._cargar_sprite_pokemon(pokemon)
        if sprite:
            superficie.blit(sprite, (sprite_x + 4, sprite_y + 4))
        else:
            # Placeholder si no se encuentra el sprite
            sprite_placeholder = pygame.Surface((self.tamaño_sprite - 8, self.tamaño_sprite - 8))
            sprite_placeholder.fill((140, 140, 140))
            superficie.blit(sprite_placeholder, (sprite_x + 4, sprite_y + 4))
        
        # Información del Pokémon
        info_x = sprite_x + self.tamaño_sprite + 10
        info_y = y + 8
        
        # Nombre del Pokémon
        nombre_texto = f"{pokemon.nombre}"
        nombre_render = self.fuente_nombre.render(nombre_texto, False, self.color_texto)
        superficie.blit(nombre_render, (info_x, info_y))
        
        # Nivel (a la derecha del nombre)
        nivel_texto = f"Nv.{pokemon.nivel}"
        nivel_render = self.fuente_info.render(nivel_texto, False, self.color_texto_claro)
        nivel_x = info_x + nombre_render.get_width() + 10
        superficie.blit(nivel_render, (nivel_x, info_y + 2))
        
        # Barra de PS (más abajo)
        barra_x = info_x
        barra_y = info_y + 30
        barra_ancho = 180
        barra_alto = 8
        
        # Label "PS" encima de la barra
        label_ps = self.fuente_pequeña.render("PS", False, self.color_texto_claro)
        superficie.blit(label_ps, (barra_x, barra_y - 14))
        
        # Dibujar barra de fondo
        pygame.draw.rect(superficie, self.color_ps_fondo, 
                        (barra_x, barra_y, barra_ancho, barra_alto))
        pygame.draw.rect(superficie, self.color_ps_borde, 
                        (barra_x, barra_y, barra_ancho, barra_alto), 1)
        
        # Dibujar barra de PS actual
        ps_porcentaje = pokemon.ps_actual / pokemon.stats_actuales['ps']
        barra_ps_ancho = int((barra_ancho - 2) * ps_porcentaje)
        color_ps = self._obtener_color_ps(pokemon.ps_actual, pokemon.stats_actuales['ps'])
        
        if barra_ps_ancho > 0:
            pygame.draw.rect(superficie, color_ps, 
                            (barra_x + 1, barra_y + 1, barra_ps_ancho, barra_alto - 2))
        
        # Texto numérico de PS (a la derecha de la barra)
        ps_texto = f"{pokemon.ps_actual}/{pokemon.stats_actuales['ps']}"
        ps_render = self.fuente_pequeña.render(ps_texto, False, self.color_texto_claro)
        superficie.blit(ps_render, (barra_x + barra_ancho + 5, barra_y - 2))
        
        return slot_alto
    
    def manejar_input(self, eventos):
        if not self.activo:
            return None
        
        tiempo_actual = pygame.time.get_ticks()
        
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if tiempo_actual - self._ultima_tecla < self.KEY_DELAY:
                    continue
                
                if evento.key == pygame.K_UP:
                    self.pokemon_seleccionado = (self.pokemon_seleccionado - 1) % len(self.equipo_pokemon)
                    self._ultima_tecla = tiempo_actual
                
                elif evento.key == pygame.K_DOWN:
                    self.pokemon_seleccionado = (self.pokemon_seleccionado + 1) % len(self.equipo_pokemon)
                    self._ultima_tecla = tiempo_actual
                
                elif evento.key == pygame.K_x or evento.key == pygame.K_z:
                    self.cerrar()
                    self._ultima_tecla = tiempo_actual
                    return "VOLVER"
        
        return None
    
    def dibujar(self, superficie):
        if not self.activo:
            return
        
        slot_altura = 76
        titulo_espacio = 50
        instrucciones_espacio = 32
        padding = 15
        
        if not self.equipo_pokemon:
            alto_ventana = 150
        else:
            alto_ventana = titulo_espacio + (len(self.equipo_pokemon) * slot_altura) + instrucciones_espacio + padding
        
        alto_ventana = min(alto_ventana, self.alto_pantalla - 100)
        y_ventana = (self.alto_pantalla - alto_ventana) // 2
        
        self._dibujar_borde_pokemon_gba(superficie, self.x_ventana, y_ventana, 
                                        self.ancho_ventana, alto_ventana)
        
        if self.equipo_pokemon:
            titulo = self.fuente_titulo.render(
                f"EQUIPO ({self.pokemon_seleccionado + 1}/{len(self.equipo_pokemon)})", 
                False, self.color_texto
            )
        else:
            titulo = self.fuente_titulo.render("EQUIPO", False, self.color_texto)
        
        titulo_rect = titulo.get_rect(centerx=self.x_ventana + self.ancho_ventana // 2, 
                                        y=y_ventana + 12)
        superficie.blit(titulo, titulo_rect)
        
        pygame.draw.line(superficie, self.color_borde_medio,
                        (self.x_ventana + 25, y_ventana + 40),
                        (self.x_ventana + self.ancho_ventana - 25, y_ventana + 40), 2)
        
        if not self.equipo_pokemon:
            texto = self.fuente_info.render("No tienes Pokemon", False, self.color_texto)
            texto_rect = texto.get_rect(center=(self.x_ventana + self.ancho_ventana // 2, 
                                                 y_ventana + alto_ventana // 2))
            superficie.blit(texto, texto_rect)
        else:
            contenido_y = y_ventana + titulo_espacio
            
            for i, pokemon in enumerate(self.equipo_pokemon):
                seleccionado = (i == self.pokemon_seleccionado)
                self._dibujar_pokemon_slot(superficie, pokemon, 
                                            self.x_ventana + 22, contenido_y, 
                                            seleccionado)
                contenido_y += slot_altura
        
        if len(self.equipo_pokemon) > 1:
            instrucciones = "X/Z: Cerrar"
        else:
            instrucciones = "X/Z: Cerrar"
        
        inst_render = self.fuente_pequeña.render(instrucciones, False, self.color_texto_claro)
        superficie.blit(inst_render, (self.x_ventana + 22, 
                                        y_ventana + alto_ventana - 25))