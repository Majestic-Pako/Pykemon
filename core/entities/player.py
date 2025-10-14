import pygame
from config import *
from core.entities.movement import manejar_movimiento

class Player(pygame.sprite.Sprite):
    def __init__(self, ancho, alto):
        super().__init__()
        self.image = self.cargar_sprite()
        self.rect = self.image.get_rect(
            center=(ancho // 2, alto // 2)
        )
    
    def cargar_sprite(self):
        try:
            # Cambiar por la ruta correcta del sprite
            sprite = pygame.image.load("assets/sprites/player/aca_la_imagen.png")
            sprite = pygame.transform.scale(sprite, (TAMAÑO_CUADRADO, TAMAÑO_CUADRADO))
            return sprite
        except FileNotFoundError:
            # Testeo con solo el cuadrado
            placeholder = pygame.Surface((TAMAÑO_CUADRADO, TAMAÑO_CUADRADO))
            placeholder.fill(RED)
            return placeholder
    
    def update(self, teclas):
        manejar_movimiento(self, teclas)
        self.limitar_limites(ANCHO, ALTO)
    
    def limitar_limites(self, ancho, alto):
        self.rect.x = max(0, min(self.rect.x, ancho - TAMAÑO_CUADRADO))
        self.rect.y = max(0, min(self.rect.y, alto - TAMAÑO_CUADRADO))
    
    def dibujar(self, superficie):
        superficie.blit(self.image, self.rect)