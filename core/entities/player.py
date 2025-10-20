import pygame
from config import *
from core.entities.movement import manejar_movimiento
from camera import Camera

class Player(pygame.sprite.Sprite):
    def __init__(self, ancho, alto, ancho_mapa, alto_mapa):
        super().__init__()
        self.image = self.cargar_sprite()
        self.rect = self.image.get_rect(
            center=(ancho // 2, alto // 2)
        )
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa

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
        self.limitar_limites()
    
    def limitar_limites(self):
        self.rect.x = max(0, min(self.rect.x, self.ancho_mapa - TAMAÑO_CUADRADO))
        self.rect.y = max(0, min(self.rect.y, self.alto_mapa - TAMAÑO_CUADRADO))
    
    def dibujar(self, superficie, camera):
        superficie.blit(self.image, camera.apply(self.rect))