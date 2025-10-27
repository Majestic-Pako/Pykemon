import pygame
from core.system.config import *

class DialogoBox:
    def __init__(self):
        self.activo = False
        self.texto = ""
        self.metadata = {}
        self.fuente_texto = pygame.font.Font(None, 26)
        self.fuente_info = pygame.font.Font(None, 18)
    
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
    
    def dibujar(self, superficie):
        if not self.activo:
            return
        
        # Dimensiones y posición del texto pa q lo modifique Thomas :u
        margen = 40
        padding = 20 
        ancho = 700 - (margen * 2)
        alto = 120
        x = margen
        y = ALTO - alto - margen
        pixel = 4  # Tamaño de cada pixel
        
        # Cuadro de fondo
        cuadro = pygame.Surface((ancho - pixel * 2, alto - pixel * 2))
        cuadro.fill((16, 24, 40))
        cuadro.set_alpha(230)
        superficie.blit(cuadro, (x + pixel, y + pixel))
        
        # Colores estilo Pokemon Esmeralda
        color_celeste_claro = (152, 216, 248)
        color_celeste_oscuro = (88, 152, 200)
        
        # Borde exterior (celeste oscuro)
        # Líneas horizontales principales
        pygame.draw.rect(superficie, color_celeste_oscuro, (x + pixel * 2, y, ancho - pixel * 4, pixel))
        pygame.draw.rect(superficie, color_celeste_oscuro, (x + pixel * 2, y + alto - pixel, ancho - pixel * 4, pixel))
        
        # Líneas verticales principales
        pygame.draw.rect(superficie, color_celeste_oscuro, (x, y + pixel * 2, pixel, alto - pixel * 4))
        pygame.draw.rect(superficie, color_celeste_oscuro, (x + ancho - pixel, y + pixel * 2, pixel, alto - pixel * 4))
        
        # Esquinas en escalera (oscuro)
        # Superior izquierda
        pygame.draw.rect(superficie, color_celeste_oscuro, (x + pixel, y + pixel, pixel, pixel))
        # Superior derecha
        pygame.draw.rect(superficie, color_celeste_oscuro, (x + ancho - pixel * 2, y + pixel, pixel, pixel))
        # Inferior izquierda
        pygame.draw.rect(superficie, color_celeste_oscuro, (x + pixel, y + alto - pixel * 2, pixel, pixel))
        # Inferior derecha
        pygame.draw.rect(superficie, color_celeste_oscuro, (x + ancho - pixel * 2, y + alto - pixel * 2, pixel, pixel))
        
        # Borde interior brillante (celeste claro) - típico de GBA
        # Líneas horizontales internas
        pygame.draw.rect(superficie, color_celeste_claro, (x + pixel * 3, y + pixel, ancho - pixel * 6, pixel))
        pygame.draw.rect(superficie, color_celeste_claro, (x + pixel * 3, y + alto - pixel * 2, ancho - pixel * 6, pixel))
        
        # Líneas verticales internas
        pygame.draw.rect(superficie, color_celeste_claro, (x + pixel, y + pixel * 3, pixel, alto - pixel * 6))
        pygame.draw.rect(superficie, color_celeste_claro, (x + ancho - pixel * 2, y + pixel * 3, pixel, alto - pixel * 6))
        
        # Esquinas internas (claro)
        # Superior izquierda
        pygame.draw.rect(superficie, color_celeste_claro, (x + pixel * 2, y + pixel * 2, pixel, pixel))
        # Superior derecha
        pygame.draw.rect(superficie, color_celeste_claro, (x + ancho - pixel * 3, y + pixel * 2, pixel, pixel))
        # Inferior izquierda
        pygame.draw.rect(superficie, color_celeste_claro, (x + pixel * 2, y + alto - pixel * 3, pixel, pixel))
        # Inferior derecha
        pygame.draw.rect(superficie, color_celeste_claro, (x + ancho - pixel * 3, y + alto - pixel * 3, pixel, pixel))
        
        # Texto principal / si es posible cambiar la fuente
        texto_render = self.fuente_texto.render(self.texto, True, (255, 255, 255))
        superficie.blit(texto_render, (x + padding, y + padding))
        
        # Información adicional la tipica guia pa niños q no saben cerrar diálogos jeje 
        if self.metadata:
            info_texto = " | ".join([f"{k}: {v}" for k, v in self.metadata.items()])
            info_texto += " | Presiona Z para cerrar"
            info_render = self.fuente_info.render(info_texto, True, (200, 200, 100))
            superficie.blit(info_render, (x + padding, y + alto - 35))