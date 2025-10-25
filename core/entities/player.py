import pygame
from core.system.config import *
from core.entities.movement import manejar_movimiento
from core.system.camera import Camera
from core.system.dialog import DialogoBox

class Player(pygame.sprite.Sprite):
    def __init__(self, ancho, alto, ancho_mapa, alto_mapa):
        super().__init__()
        self.image = self.cargar_sprite()
        self.rect = self.image.get_rect(
            center=(ancho // 2, alto // 2)
        )
        self.ancho_mapa = ancho_mapa
        self.alto_mapa = alto_mapa
        self.dialogo_activo = False
        self.dialogo_texto = ""
        self.dialogo_npc_id = None
        self.dialogo_box = DialogoBox()
        self._z_held = False

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
        self.dialogo_box.dibujar(superficie)
    
    def manejar_dialogo(self, teclas, npcs):
        z_now = teclas[pygame.K_z]
        if z_now and not self._z_held:
            if self.dialogo_box.activo:
                self.dialogo_box.cerrar()
                pygame.time.wait(200)
            else:
                area_interaccion = self.rect.inflate(TAMAÑO_CUADRADO, TAMAÑO_CUADRADO)
                for npc in npcs:
                    if area_interaccion.colliderect(npc.rect):
                        metadata = {"NPC ID": getattr(npc, "npc_id", None)}
                        self.dialogo_box.mostrar(getattr(npc, "dialog_id", "Sin dialogo"), metadata)
                        pygame.time.wait(150)
                        break
        self._z_held = z_now