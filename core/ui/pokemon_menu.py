import pygame
from core.system.config import *

class PokemonMenu:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        
        # Estado
        self.activo = False
        self.equipo_pokemon = []
        self.pokemon_seleccionado = 0
        
        # Dimensiones de la ventana (lateral derecho)
        self.ancho_ventana = 350
        self.margen_derecho = 20
        self.x_ventana = ancho_pantalla - self.ancho_ventana - self.margen_derecho
        
        # Colores estilo Pokémon
        self.color_fondo = (16, 24, 40)
        self.color_borde_oscuro = (88, 152, 200)
        self.color_borde_claro = (152, 216, 248)
        self.color_texto = (255, 255, 255)
        self.color_ps_verde = (40, 200, 80)
        self.color_ps_amarillo = (240, 200, 40)
        self.color_ps_rojo = (220, 60, 60)
        self.color_ps_fondo = (60, 60, 80)
        self.color_seleccion = (80, 120, 200, 100)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 28)
        self.fuente_nombre = pygame.font.Font(None, 24)
        self.fuente_info = pygame.font.Font(None, 20)
        self.fuente_pequeña = pygame.font.Font(None, 18)
        
        # Tamaño del pixel para bordes
        self.pixel = 4
        
        # Tamaño del sprite
        self.tamaño_sprite = 48
        
        # Control de input
        self._ultima_tecla = 0
        self.KEY_DELAY = 150
    
    def abrir(self, equipo_pokemon):
        """Abre el menú con el equipo del jugador"""
        self.activo = True
        self.equipo_pokemon = equipo_pokemon
        self.pokemon_seleccionado = 0
        self._ultima_tecla = pygame.time.get_ticks()
    
    def cerrar(self):
        """Cierra el menú"""
        self.activo = False
    
    def _dibujar_borde_pokemon(self, superficie, x, y, ancho, alto):
        """Dibuja el borde estilo Pokémon GBA"""
        p = self.pixel
        
        # Fondo
        fondo = pygame.Surface((ancho - p * 4, alto - p * 4))
        fondo.fill(self.color_fondo)
        fondo.set_alpha(245)
        superficie.blit(fondo, (x + p * 2, y + p * 2))
        
        # Borde exterior (oscuro)
        rects_oscuro = [
            (x + p * 2, y, ancho - p * 4, p),
            (x + p * 2, y + alto - p, ancho - p * 4, p),
            (x, y + p * 2, p, alto - p * 4),
            (x + ancho - p, y + p * 2, p, alto - p * 4),
        ]
        for rect in rects_oscuro:
            pygame.draw.rect(superficie, self.color_borde_oscuro, rect)
        
        # Esquinas exteriores
        esquinas_ext = [
            (x + p, y + p), (x + ancho - p * 2, y + p),
            (x + p, y + alto - p * 2), (x + ancho - p * 2, y + alto - p * 2)
        ]
        for ex, ey in esquinas_ext:
            pygame.draw.rect(superficie, self.color_borde_oscuro, (ex, ey, p, p))
        
        # Borde interior (claro)
        rects_claro = [
            (x + p * 3, y + p, ancho - p * 6, p),
            (x + p * 3, y + alto - p * 2, ancho - p * 6, p),
            (x + p, y + p * 3, p, alto - p * 6),
            (x + ancho - p * 2, y + p * 3, p, alto - p * 6),
        ]
        for rect in rects_claro:
            pygame.draw.rect(superficie, self.color_borde_claro, rect)
        
        # Esquinas interiores
        esquinas_int = [
            (x + p * 2, y + p * 2), (x + ancho - p * 3, y + p * 2),
            (x + p * 2, y + alto - p * 3), (x + ancho - p * 3, y + alto - p * 3)
        ]
        for ex, ey in esquinas_int:
            pygame.draw.rect(superficie, self.color_borde_claro, (ex, ey, p, p))
    
    def _obtener_color_ps(self, ps_actual, ps_max):
        """Determina el color de la barra de PS según porcentaje"""
        porcentaje = ps_actual / ps_max if ps_max > 0 else 0
        if porcentaje > 0.5:
            return self.color_ps_verde
        elif porcentaje > 0.2:
            return self.color_ps_amarillo
        else:
            return self.color_ps_rojo
    
    def _dibujar_pokemon_slot(self, superficie, pokemon, x, y, seleccionado=False):
        """Dibuja un slot de Pokémon"""
        slot_alto = 75
        
        # Fondo si está seleccionado
        if seleccionado:
            fondo_sel = pygame.Surface((self.ancho_ventana - 40, slot_alto - 5))
            fondo_sel.set_alpha(100)
            fondo_sel.fill(self.color_seleccion)
            superficie.blit(fondo_sel, (x, y))
        
        # Recuadro para el sprite
        sprite_x = x + 8
        sprite_y = y + (slot_alto - self.tamaño_sprite) // 2
        pygame.draw.rect(superficie, self.color_borde_oscuro, 
                        (sprite_x - 2, sprite_y - 2, self.tamaño_sprite + 4, self.tamaño_sprite + 4))
        pygame.draw.rect(superficie, self.color_fondo, 
                        (sprite_x, sprite_y, self.tamaño_sprite, self.tamaño_sprite))
        
        # Sprite placeholder
        sprite_placeholder = pygame.Surface((self.tamaño_sprite, self.tamaño_sprite))
        sprite_placeholder.fill((100, 100, 100))
        superficie.blit(sprite_placeholder, (sprite_x, sprite_y))
        
        # Información compacta
        info_x = sprite_x + self.tamaño_sprite + 12
        info_y = y + 8
        
        # Nombre y nivel
        nombre_texto = f"{pokemon.nombre}  Nv.{pokemon.nivel}"
        nombre_render = self.fuente_nombre.render(nombre_texto, True, self.color_texto)
        superficie.blit(nombre_render, (info_x, info_y))
        
        # PS texto
        ps_texto = f"PS: {pokemon.ps_actual}/{pokemon.stats_actuales['ps']}"
        ps_render = self.fuente_info.render(ps_texto, True, self.color_texto)
        superficie.blit(ps_render, (info_x, info_y + 24))
        
        # Barra de PS
        barra_x = info_x
        barra_y = info_y + 45
        barra_ancho = 180
        barra_alto = 10
        
        # Fondo de la barra
        pygame.draw.rect(superficie, self.color_ps_fondo, 
                        (barra_x, barra_y, barra_ancho, barra_alto), border_radius=3)
        
        # Barra de PS actual
        ps_porcentaje = pokemon.ps_actual / pokemon.stats_actuales['ps']
        barra_ps_ancho = int(barra_ancho * ps_porcentaje)
        color_ps = self._obtener_color_ps(pokemon.ps_actual, pokemon.stats_actuales['ps'])
        
        if barra_ps_ancho > 0:
            pygame.draw.rect(superficie, color_ps, 
                            (barra_x, barra_y, barra_ps_ancho, barra_alto), border_radius=3)
        
        # Borde de la barra
        pygame.draw.rect(superficie, self.color_borde_oscuro, 
                        (barra_x, barra_y, barra_ancho, barra_alto), 2, border_radius=3)
        
        return slot_alto
    
    def manejar_input(self, eventos):
        """Maneja la navegación y cierre del menú"""
        if not self.activo:
            return
        
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
    
    def dibujar(self, superficie):
        """Dibuja el menú de Pokémon"""
        if not self.activo:
            return
        
        # Calcular altura dinámica según cantidad de Pokémon
        slot_altura = 80
        titulo_espacio = 50
        instrucciones_espacio = 35
        padding = 15
        
        if not self.equipo_pokemon:
            alto_ventana = 150
        else:
            alto_ventana = titulo_espacio + (len(self.equipo_pokemon) * slot_altura) + instrucciones_espacio + padding
        
        # Limitar altura máxima
        alto_ventana = min(alto_ventana, self.alto_pantalla - 100)
        
        # Centrar verticalmente
        y_ventana = (self.alto_pantalla - alto_ventana) // 2
        
        # Dibujar ventana
        self._dibujar_borde_pokemon(superficie, self.x_ventana, y_ventana, 
                                        self.ancho_ventana, alto_ventana)
        
        # Título con indicador
        if self.equipo_pokemon:
            titulo = self.fuente_titulo.render(
                f"EQUIPO POKEMON ({self.pokemon_seleccionado + 1}/{len(self.equipo_pokemon)})", 
                True, self.color_texto
            )
        else:
            titulo = self.fuente_titulo.render("EQUIPO POKEMON", True, self.color_texto)
        
        titulo_rect = titulo.get_rect(centerx=self.x_ventana + self.ancho_ventana // 2, 
                                        y=y_ventana + 15)
        superficie.blit(titulo, titulo_rect)
        
        # Línea separadora
        pygame.draw.line(superficie, self.color_borde_claro,
                        (self.x_ventana + 30, y_ventana + 45),
                        (self.x_ventana + self.ancho_ventana - 30, y_ventana + 45), 1)
        
        # Verificar si hay Pokémon
        if not self.equipo_pokemon:
            texto = self.fuente_info.render("No tienes Pokémon en tu equipo", True, self.color_texto)
            texto_rect = texto.get_rect(center=(self.x_ventana + self.ancho_ventana // 2, 
                                                 y_ventana + alto_ventana // 2))
            superficie.blit(texto, texto_rect)
        else:
            # Dibujar todos los Pokémon
            contenido_y = y_ventana + titulo_espacio
            
            for i, pokemon in enumerate(self.equipo_pokemon):
                seleccionado = (i == self.pokemon_seleccionado)
                self._dibujar_pokemon_slot(superficie, pokemon, 
                                            self.x_ventana + 20, contenido_y, 
                                            seleccionado)
                contenido_y += slot_altura
        
        # Instrucciones
        if len(self.equipo_pokemon) > 1:
            instrucciones = "↑↓: Navegar  X/Z: Cerrar"
        else:
            instrucciones = "X/Z: Cerrar"
        
        inst_render = self.fuente_pequeña.render(instrucciones, True, (200, 200, 100))
        superficie.blit(inst_render, (self.x_ventana + 30, 
                                        y_ventana + alto_ventana - 30))