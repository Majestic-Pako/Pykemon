import pytmx
import pygame
from pytmx.util_pygame import load_pygame

class Mapa:
    def __init__(self, ruta_mapa):
        try:
            self.tmx_data = load_pygame(ruta_mapa)
            print("Mapa cargado correctamente:", ruta_mapa)
            self.mapa_tmx = self.tmx_data
            self.ancho = self.mapa_tmx.width * self.mapa_tmx.tilewidth
            self.alto = self.mapa_tmx.height * self.mapa_tmx.tileheight
            self.colisiones = []
            collision_layer = self.tmx_data.get_layer_by_name("Colisiones")
            for obj in collision_layer:
                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                self.colisiones.append(rect)
        except Exception as e:
            print("Fallo el mapa pa ...", e)
            raise
    
    def dibujar(self, superficie, camera):
        for capa in self.mapa_tmx.visible_layers:
            if hasattr(capa, "tiles"):
                for x, y, imagen in capa.tiles():
                    if imagen:
                        px = x * self.mapa_tmx.tilewidth
                        py = y * self.mapa_tmx.tileheight
                        superficie.blit(imagen, (px - camera.x, py - camera.y))