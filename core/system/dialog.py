import pygame
from config import *

class DialogoBox:
    def __init__(self):
        self.activo = False
        self.texto = ""
        self.metadata = {}
        self.fuente_texto = pygame.font.Font(None, 28)
        self.fuente_info = pygame.font.Font(None, 20)
    
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
        
        # Dimensiones y posición pa q lo modifique Thomas :u
        margen = 40
        padding = 20
        ancho = ANCHO - (margen * 2)
        alto = 120
        x = margen
        y = ALTO - alto - margen
        
        # Cuadro de fondo
        cuadro = pygame.Surface((ancho, alto))
        cuadro.fill((20, 20, 40))
        cuadro.set_alpha(230)
        superficie.blit(cuadro, (x, y))
        
        # Borde
        pygame.draw.rect(superficie, (255, 255, 255), (x, y, ancho, alto), 3)
        
        # Texto principal / si es posible cambiar la fuente
        texto_render = self.fuente_texto.render(self.texto, True, (255, 255, 255))
        superficie.blit(texto_render, (x + padding, y + padding))
        
        # Información adicional la tipica guia pa niños q no saben cerrar diálogos jeje 
        if self.metadata:
            info_texto = " | ".join([f"{k}: {v}" for k, v in self.metadata.items()])
            info_texto += " | Presiona Z para cerrar"
            info_render = self.fuente_info.render(info_texto, True, (200, 200, 100))
            superficie.blit(info_render, (x + padding, y + alto - 35))