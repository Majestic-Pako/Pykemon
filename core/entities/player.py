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
        self.dialogo_activo = False
        self.dialogo_texto = ""
        self.dialogo_npc_id = None

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
    
    def manejar_dialogo(self, superficie, npcs, teclas):
        if teclas[pygame.K_z]:
            if self.dialogo_activo:
                self.dialogo_activo = False
                pygame.time.wait(200)
            else:
                area = self.rect.inflate(TAMAÑO_CUADRADO, TAMAÑO_CUADRADO)
                for npc in npcs:
                    if area.colliderect(npc.rect):
                        self.dialogo_texto = npc.dialog_id
                        self.dialogo_npc_id = npc.npc_id
                        self.dialogo_activo = True
                        break
    
        if self.dialogo_activo:
            m, p = 40, 20
            w, h = ANCHO - (m * 2), 120
            x, y = m, ALTO - h - m
        
            cuadro = pygame.Surface((w, h))
            cuadro.fill((20, 20, 40))
            cuadro.set_alpha(230)
            superficie.blit(cuadro, (x, y))
            pygame.draw.rect(superficie, (255, 255, 255), (x, y, w, h), 3)
        
            fuente = pygame.font.Font(None, 28)
            texto = fuente.render(self.dialogo_texto, True, (255, 255, 255))
            superficie.blit(texto, (x + p, y + p))
        
            fuente_info = pygame.font.Font(None, 20)
            info = fuente_info.render(f"NPC ID: {self.dialogo_npc_id} | Presiona Z para cerrar", True, (200, 200, 100))
            superficie.blit(info, (x + p, y + h - 35))