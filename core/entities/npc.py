import pygame
import json
import random
from core.system.config import *

class NPC(pygame.sprite.Sprite):
    dialogos_cargados = None
    
    def __init__(self, x, y, nombre, sprite_id, dialog_id='Sin dialogo', npc_id='?'):
        super().__init__()
        self.nombre = nombre
        self.sprite_id = sprite_id
        self.dialog_id = dialog_id
        self.npc_id = npc_id
        self.image = self.cargar_sprite()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.interaction_rect = self.rect.inflate(TAMAÑO_CUADRADO, TAMAÑO_CUADRADO)
        
        if NPC.dialogos_cargados is None:
            NPC.dialogos_cargados = self.cargar_dialogos()
    
    def cargar_dialogos(self):
        try:
            with open("data/dialogues.json", "r", encoding="utf-8") as f:
                dialogos = json.load(f)
                #print(f"[OK] Diálogos cargados correctamente")
                return dialogos
        except FileNotFoundError:
            #print(f"[ERROR] No se encontró data/dialogue.json")
            return {"Sin dialogo": ["..."]}
        except json.JSONDecodeError as e:
            #print(f"[ERROR] Error al parsear dialogue.json: {e}")
            return {"Sin dialogo": ["..."]}
    
    def obtener_dialogo(self):
        if NPC.dialogos_cargados is None:
            return "..."
        
        # Buscar diálogos por dialog_id
        dialogos_npc = NPC.dialogos_cargados.get(self.dialog_id)
        
        if dialogos_npc and isinstance(dialogos_npc, list) and len(dialogos_npc) > 0:
            dialogo = random.choice(dialogos_npc)
            #print(f"[DEBUG] NPC '{self.nombre}' dice: {dialogo[:50]}...")
            return dialogo
        else:
            #print(f"[WARN] No se encontraron diálogos para dialog_id: '{self.dialog_id}'")
            return "..."
    
    def cargar_sprite(self):
        try:
            ruta_sprite = f"assets/sprites/npcs/{self.sprite_id}.png"
            sprite = pygame.image.load(ruta_sprite)
            sprite = pygame.transform.scale(sprite, (16 * 2, 24 * 2))
            print(f"Sprite cargado: {ruta_sprite} para NPC '{self.nombre}'")
            return sprite
        except FileNotFoundError:
            placeholder = pygame.Surface((16 * 2, 24 * 2))
            placeholder.fill((255, 255, 0))
            return placeholder
    
    def dibujar(self, superficie, camera):
        superficie.blit(self.image, camera.apply(self.rect))