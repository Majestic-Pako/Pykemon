import pygame

class PortalManager:
    def __init__(self):
        self.transicion_activa = False
        self.destino = None
        self.transicion_alpha = 0
        self.transicion_estado = None  
        self.transicion_velocidad = 12
        self.cambio_mapa_pendiente = False
    
    def verificar_portal(self, player_rect, portales):
        for portal in portales:
            if player_rect.colliderect(portal["rect"]):
                return {
                    "target_map": portal["target_map"],
                    "target_x": portal["target_x"],
                    "target_y": portal["target_y"]
                }
        return None
    
    def cambiar_mapa(self, target_map, target_x, target_y):
        self.transicion_activa = True
        self.transicion_alpha = 0
        self.transicion_estado = "FADE_OUT"
        self.cambio_mapa_pendiente = False
        self.destino = {
            "mapa": target_map,
            "x": target_x,
            "y": target_y
        }
    
    def actualizar_transicion(self):
        """Actualiza la animación de transición"""
        if not self.transicion_activa:
            return
        
        if self.transicion_estado == "FADE_OUT":
            self.transicion_alpha += self.transicion_velocidad
            
            if self.transicion_alpha >= 255:
                self.transicion_alpha = 255
                self.cambio_mapa_pendiente = True
                self.transicion_estado = "FADE_IN"
        
        elif self.transicion_estado == "FADE_IN":
            self.transicion_alpha -= self.transicion_velocidad
            
            if self.transicion_alpha <= 0:
                self.transicion_alpha = 0
                self.transicion_activa = False
                self.transicion_estado = None
    
    def obtener_destino(self):
        destino = self.destino
        self.destino = None
        self.cambio_mapa_pendiente = False
        return destino
    
    def debe_cambiar_mapa(self):
        return self.cambio_mapa_pendiente
    
    def dibujar_transicion(self, ventana):
        if self.transicion_activa or self.transicion_alpha > 0:
            ancho, alto = ventana.get_size()
            overlay = pygame.Surface((ancho, alto))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(self.transicion_alpha)
            ventana.blit(overlay, (0, 0))