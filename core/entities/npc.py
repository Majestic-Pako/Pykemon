#Se importa las librerias
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
        ruta_sprite = f"assets/sprites/npcs/{self.sprite_id}.png"
        try:
            #print(f"[DEBUG] Intentando cargar: {ruta_sprite}")
            #print(f"[DEBUG] sprite_id recibido: '{self.sprite_id}'")
            sprite = pygame.image.load(ruta_sprite)
            sprite = pygame.transform.scale(sprite, (16 * 2, 24 * 2))
            #print(f"[OK] Sprite cargado exitosamente: {ruta_sprite} para NPC '{self.nombre}'")
            return sprite
        except FileNotFoundError as e:
            #print(f"[ERROR] FileNotFoundError: {e}")
            #print(f"[ERROR] Ruta buscada: {ruta_sprite}")
            placeholder = pygame.Surface((16 * 2, 24 * 2))
            placeholder.fill((255, 255, 0))
            return placeholder
        except Exception as e:
            #print(f"[ERROR] Excepción inesperada: {type(e).__name__}: {e}")
            placeholder = pygame.Surface((16 * 2, 24 * 2))
            placeholder.fill((255, 0, 0))  
            return placeholder
    
    def dibujar(self, superficie, camera):
        superficie.blit(self.image, camera.apply(self.rect))