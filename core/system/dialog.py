import pygame
from core.system.config import *

class DialogoBox:
    def __init__(self):
        self.activo = False
        self.texto = ""
        self.metadata = {}
        self.fuente_texto = pygame.font.Font(None, 26)
        self.fuente_info = pygame.font.Font(None, 18)
        
        # Colores estilo Pokémon
        self.color_fondo = (16, 24, 40)
        self.color_borde_oscuro = (88, 152, 200)
        self.color_borde_claro = (152, 216, 248)
        self.color_texto = (255, 255, 255)
        self.color_info = (200, 200, 100)
    
    def mostrar(self, texto, metadata=None):
        self.activo = True
        self.texto = texto
        self.metadata = metadata if metadata else {}
    
    def cerrar(self):
        self.activo = False
        self.texto = ""
        self.metadata = {}
    
    def toggle(self):
        if self.activo:
            self.cerrar()
        return self.activo
    
    def _dibujar_borde_pokemon(self, superficie, x, y, ancho, alto, pixel):
        fondo = pygame.Surface((ancho - pixel * 4, alto - pixel * 4))
        fondo.fill(self.color_fondo)
        fondo.set_alpha(240)
        superficie.blit(fondo, (x + pixel * 2, y + pixel * 2))
        
        rects_oscuro = [
            (x + pixel * 2, y, ancho - pixel * 4, pixel),  # Top
            (x + pixel * 2, y + alto - pixel, ancho - pixel * 4, pixel),  # Bottom
            (x, y + pixel * 2, pixel, alto - pixel * 4),  # Left
            (x + ancho - pixel, y + pixel * 2, pixel, alto - pixel * 4),  # Right
        ]
        for rect in rects_oscuro:
            pygame.draw.rect(superficie, self.color_borde_oscuro, rect)
        
        # Esquinas exteriores (oscuro)
        esquinas_ext = [
            (x + pixel, y + pixel),
            (x + ancho - pixel * 2, y + pixel),
            (x + pixel, y + alto - pixel * 2),
            (x + ancho - pixel * 2, y + alto - pixel * 2)
        ]
        for ex, ey in esquinas_ext:
            pygame.draw.rect(superficie, self.color_borde_oscuro, (ex, ey, pixel, pixel))
        
        # Borde interior (claro) - Más grueso para que se note mejor
        rects_claro = [
            (x + pixel * 3, y + pixel, ancho - pixel * 6, pixel),  # Top
            (x + pixel * 3, y + alto - pixel * 2, ancho - pixel * 6, pixel),  # Bottom
            (x + pixel, y + pixel * 3, pixel, alto - pixel * 6),  # Left
            (x + ancho - pixel * 2, y + pixel * 3, pixel, alto - pixel * 6),  # Right
        ]
        for rect in rects_claro:
            pygame.draw.rect(superficie, self.color_borde_claro, rect)
        
        # Esquinas interiores (claro)
        esquinas_int = [
            (x + pixel * 2, y + pixel * 2),
            (x + ancho - pixel * 3, y + pixel * 2),
            (x + pixel * 2, y + alto - pixel * 3),
            (x + ancho - pixel * 3, y + alto - pixel * 3)
        ]
        for ex, ey in esquinas_int:
            pygame.draw.rect(superficie, self.color_borde_claro, (ex, ey, pixel, pixel))
    
    def dibujar(self, superficie):
        if not self.activo:
            return

        margen = 40
        padding = 25
        ancho = 700 - (margen * 2)
        alto = 120
        x = margen
        y = ALTO - alto - margen
        pixel = 4
        
        self._dibujar_borde_pokemon(superficie, x, y, ancho, alto, pixel)
        
        # Texto principal
        texto_render = self.fuente_texto.render(self.texto, True, self.color_texto)
        superficie.blit(texto_render, (x + padding, y + padding))
        
        if self.metadata:
            info_texto = " | ".join([f"{k}: {v}" for k, v in self.metadata.items()])
            info_texto += " | Presiona Z para cerrar"
            info_render = self.fuente_info.render(info_texto, True, self.color_info)
            superficie.blit(info_render, (x + padding, y + alto - 35))