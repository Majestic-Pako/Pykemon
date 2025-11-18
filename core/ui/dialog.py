import pygame
from core.system.config import *

class DialogoBox:
    def __init__(self):
        self.activo = False
        self.texto = ""
        self.metadata = {}
        
        self.fuente_texto = pygame.font.Font(None, 24)  
        self.fuente_info = pygame.font.Font(None, 16)
        
        self.color_fondo = (248, 248, 248)  
        self.color_fondo_sombra = (200, 200, 192)  
        
        self.color_borde_externo = (0, 0, 0)  
        self.color_borde_claro = (248, 248, 248)  
        self.color_borde_medio = (104, 104, 104)  
        self.color_borde_oscuro = (56, 56, 56)  
        
        self.color_texto = (80, 80, 80)  
        self.color_info = (112, 112, 112) 
    
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
    
    def _dibujar_borde_pokemon_gba(self, superficie, x, y, ancho, alto, pixel):
        fondo = pygame.Surface((ancho - pixel * 4, alto - pixel * 4))
        fondo.fill(self.color_fondo)
        superficie.blit(fondo, (x + pixel * 2, y + pixel * 2))
        
        sombra = pygame.Surface((ancho - pixel * 6, alto - pixel * 6))
        sombra.fill(self.color_fondo_sombra)
        sombra.set_alpha(30)
        superficie.blit(sombra, (x + pixel * 4, y + pixel * 4))
        pygame.draw.rect(superficie, self.color_borde_externo, (x + pixel * 2, y, ancho - pixel * 4, pixel))
        pygame.draw.rect(superficie, self.color_borde_externo, (x + pixel * 2, y + alto - pixel, ancho - pixel * 4, pixel))
        pygame.draw.rect(superficie, self.color_borde_externo, (x, y + pixel * 2, pixel, alto - pixel * 4))
        pygame.draw.rect(superficie, self.color_borde_externo, (x + ancho - pixel, y + pixel * 2, pixel, alto - pixel * 4))
        esquinas_ext = [
            (x + pixel, y + pixel),
            (x + ancho - pixel * 2, y + pixel),
            (x + pixel, y + alto - pixel * 2),
            (x + ancho - pixel * 2, y + alto - pixel * 2)
        ]
        for ex, ey in esquinas_ext:
            pygame.draw.rect(superficie, self.color_borde_externo, (ex, ey, pixel, pixel))
        
        pygame.draw.rect(superficie, self.color_borde_claro, (x + pixel * 3, y + pixel, ancho - pixel * 6, pixel))
        pygame.draw.rect(superficie, self.color_borde_claro, (x + pixel, y + pixel * 3, pixel, alto - pixel * 6))
        
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + pixel * 3, y + alto - pixel * 2, ancho - pixel * 6, pixel))
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + ancho - pixel * 2, y + pixel * 3, pixel, alto - pixel * 6))
        
        pygame.draw.rect(superficie, self.color_borde_medio, (x + pixel * 4, y + pixel * 2, ancho - pixel * 8, pixel))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + pixel * 2, y + pixel * 4, pixel, alto - pixel * 8))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + pixel * 4, y + alto - pixel * 3, ancho - pixel * 8, pixel))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + ancho - pixel * 3, y + pixel * 4, pixel, alto - pixel * 8))
        
        esquinas_int = [
            (x + pixel * 2, y + pixel * 2),
            (x + ancho - pixel * 3, y + pixel * 2),
            (x + pixel * 2, y + alto - pixel * 3),
            (x + ancho - pixel * 3, y + alto - pixel * 3)
        ]
        for ex, ey in esquinas_int:
            pygame.draw.rect(superficie, self.color_borde_medio, (ex, ey, pixel, pixel))
    
    def dibujar(self, superficie):
        if not self.activo:
            return
        margen = 40
        padding = 20
        ancho = 700 - (margen * 2)
        alto = 100  
        x = margen
        y = ALTO - alto - margen
        pixel = 4
        
        self._dibujar_borde_pokemon_gba(superficie, x, y, ancho, alto, pixel)
        
        texto_render = self.fuente_texto.render(self.texto, False, self.color_texto)
        superficie.blit(texto_render, (x + padding, y + padding))
        
        if self.metadata:
            info_texto = " | ".join([f"{k}: {v}" for k, v in self.metadata.items()])
            info_texto += " | Presiona Z"
            info_render = self.fuente_info.render(info_texto, False, self.color_info)
            superficie.blit(info_render, (x + padding, y + alto - 28))