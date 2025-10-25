import pygame
from core.system.config import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, nombre, sprite_id,dialog_id='Sin dialogo',npc_id='?'):
        super().__init__()
        self.nombre = nombre
        self.sprite_id = sprite_id
        self.dialog_id = dialog_id
        self.npc_id = npc_id
        self.image = self.cargar_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.interaction_rect = self.rect.inflate(TAMAÑO_CUADRADO, TAMAÑO_CUADRADO)
    
    def cargar_sprite(self):
        try:
            # Cambiar por la ruta correcta del sprite para diferentes tipos de NPCs
            ruta_sprite = f"assets/sprites/npcs/{self.sprite_id}.png"
            sprite = pygame.image.load(ruta_sprite)
            sprite = pygame.transform.scale(sprite, (TAMAÑO_CUADRADO, TAMAÑO_CUADRADO))
            print(f"Sprite cargado: {ruta_sprite} para NPC '{self.nombre}'")
            return sprite
        except FileNotFoundError:
            # Placeholder amarillo por ahora
            placeholder = pygame.Surface((TAMAÑO_CUADRADO, TAMAÑO_CUADRADO))
            placeholder.fill((255, 255, 0))
            return placeholder
    
    def dibujar(self, superficie, camera):
        superficie.blit(self.image, camera.apply(self.rect))