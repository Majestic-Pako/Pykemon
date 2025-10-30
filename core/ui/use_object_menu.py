import pygame
from core.system.config import *

class UsarObjetoMenu:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        
        # Estado
        self.activo = False
        self.equipo_pokemon = []
        self.pokemon_seleccionado = 0
        self.item_nombre = ""
        
        # Dimensiones
        self.ancho_ventana = 350
        self.margen_derecho = 20
        self.x_ventana = ancho_pantalla - self.ancho_ventana - self.margen_derecho
        
        # Colores
        self.color_fondo = (16, 24, 40)
        self.color_borde_oscuro = (88, 152, 200)
        self.color_borde_claro = (152, 216, 248)
        self.color_texto = (255, 255, 255)
        self.color_seleccion = (80, 120, 200, 100)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 26)
        self.fuente_nombre = pygame.font.Font(None, 22)
        self.fuente_info = pygame.font.Font(None, 18)
        
        # Pixel para bordes
        self.pixel = 4
        
        # Control de input
        self._ultima_tecla = 0
        self.KEY_DELAY = 150
    
    def abrir(self, equipo_pokemon, item_nombre):
        """Abre el menú para seleccionar Pokémon"""
        self.activo = True
        self.equipo_pokemon = equipo_pokemon
        self.item_nombre = item_nombre
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
        
        # Bordes (versión compacta)
        rects_oscuro = [
            (x + p * 2, y, ancho - p * 4, p),
            (x + p * 2, y + alto - p, ancho - p * 4, p),
            (x, y + p * 2, p, alto - p * 4),
            (x + ancho - p, y + p * 2, p, alto - p * 4),
        ]
        for rect in rects_oscuro:
            pygame.draw.rect(superficie, self.color_borde_oscuro, rect)
        
        esquinas_ext = [
            (x + p, y + p), (x + ancho - p * 2, y + p),
            (x + p, y + alto - p * 2), (x + ancho - p * 2, y + alto - p * 2)
        ]
        for ex, ey in esquinas_ext:
            pygame.draw.rect(superficie, self.color_borde_oscuro, (ex, ey, p, p))
        
        rects_claro = [
            (x + p * 3, y + p, ancho - p * 6, p),
            (x + p * 3, y + alto - p * 2, ancho - p * 6, p),
            (x + p, y + p * 3, p, alto - p * 6),
            (x + ancho - p * 2, y + p * 3, p, alto - p * 6),
        ]
        for rect in rects_claro:
            pygame.draw.rect(superficie, self.color_borde_claro, rect)
        
        esquinas_int = [
            (x + p * 2, y + p * 2), (x + ancho - p * 3, y + p * 2),
            (x + p * 2, y + alto - p * 3), (x + ancho - p * 3, y + alto - p * 3)
        ]
        for ex, ey in esquinas_int:
            pygame.draw.rect(superficie, self.color_borde_claro, (ex, ey, p, p))
    
    def manejar_input(self, eventos):
        """Maneja la selección de Pokémon"""
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
                
                elif evento.key == pygame.K_z or evento.key == pygame.K_RETURN:
                    self._ultima_tecla = tiempo_actual
                    return ("CONFIRMAR", self.pokemon_seleccionado)
                
                elif evento.key == pygame.K_x:
                    self.cerrar()
                    self._ultima_tecla = tiempo_actual
                    return "CANCELAR"
        
        return None
    
    def dibujar(self, superficie):
        """Dibuja el menú de selección"""
        if not self.activo:
            return
        
        # Calcular altura
        slot_altura = 50
        titulo_espacio = 70
        instrucciones_espacio = 35
        padding = 15
        
        alto_ventana = titulo_espacio + (len(self.equipo_pokemon) * slot_altura) + instrucciones_espacio + padding
        alto_ventana = min(alto_ventana, self.alto_pantalla - 100)
        
        y_ventana = (self.alto_pantalla - alto_ventana) // 2
        
        # Dibujar ventana
        self._dibujar_borde_pokemon(superficie, self.x_ventana, y_ventana, 
                                        self.ancho_ventana, alto_ventana)
        
        # Título
        titulo = self.fuente_titulo.render(f"Usar {self.item_nombre}", True, self.color_texto)
        titulo_rect = titulo.get_rect(centerx=self.x_ventana + self.ancho_ventana // 2, 
                                        y=y_ventana + 15)
        superficie.blit(titulo, titulo_rect)
        
        subtitulo = self.fuente_info.render("Selecciona un Pokémon", True, (180, 180, 200))
        subtitulo_rect = subtitulo.get_rect(centerx=self.x_ventana + self.ancho_ventana // 2, 
                                            y=y_ventana + 40)
        superficie.blit(subtitulo, subtitulo_rect)
        
        # Línea separadora
        pygame.draw.line(superficie, self.color_borde_claro,
                        (self.x_ventana + 30, y_ventana + 60),
                        (self.x_ventana + self.ancho_ventana - 30, y_ventana + 60), 1)
        
        # Lista de Pokémon
        contenido_y = y_ventana + titulo_espacio
        
        for i, pokemon in enumerate(self.equipo_pokemon):
            seleccionado = (i == self.pokemon_seleccionado)
            
            # Fondo si está seleccionado
            if seleccionado:
                fondo_sel = pygame.Surface((self.ancho_ventana - 40, slot_altura - 5))
                fondo_sel.set_alpha(100)
                fondo_sel.fill(self.color_seleccion)
                superficie.blit(fondo_sel, (self.x_ventana + 20, contenido_y))
            
            # Nombre y nivel
            nombre_texto = f"{pokemon.nombre}  Nv.{pokemon.nivel}"
            nombre_render = self.fuente_nombre.render(nombre_texto, True, self.color_texto)
            superficie.blit(nombre_render, (self.x_ventana + 30, contenido_y + 8))
            
            # PS
            ps_texto = f"PS: {pokemon.ps_actual}/{pokemon.stats_actuales['ps']}"
            ps_render = self.fuente_info.render(ps_texto, True, (180, 180, 200))
            superficie.blit(ps_render, (self.x_ventana + 30, contenido_y + 28))
            
            contenido_y += slot_altura
        
        # Instrucciones
        if len(self.equipo_pokemon) > 1:
            instrucciones = "↑↓: Navegar  Z: Confirmar  X: Cancelar"
        else:
            instrucciones = "Z: Confirmar  X: Cancelar"
        
        inst_render = self.fuente_info.render(instrucciones, True, (200, 200, 100))
        superficie.blit(inst_render, (self.x_ventana + 20, 
                                        y_ventana + alto_ventana - 25))