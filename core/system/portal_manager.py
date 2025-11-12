import pygame

class PortalManager:
    def __init__(self):
        self.transicion_activa = False
        self.destino = None
    
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
        self.destino = {
            "mapa": target_map,
            "x": target_x,
            "y": target_y
        }
    
    def obtener_destino(self):
        destino = self.destino
        self.transicion_activa = False
        self.destino = None
        return destino