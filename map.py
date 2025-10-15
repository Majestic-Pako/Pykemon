## Solo es de testeo de mapas, borrar despues
import pytmx
import pygame
from pytmx.util_pygame import load_pygame

class Mapa:
    def __init__(self, ruta_mapa):
        self.mapa_tmx = load_pygame(ruta_mapa)
        self.ancho = self.mapa_tmx.width * self.mapa_tmx.tilewidth
        self.alto = self.mapa_tmx.height * self.mapa_tmx.tileheight
    
    def dibujar(self, superficie):
        for capa in self.mapa_tmx.visible_layers:
            if isinstance(capa, pytmx.TiledTileLayer):
                for x, y, imagen in capa.tiles():
                    if imagen:
                        superficie.blit(imagen, (x * self.mapa_tmx.tilewidth, y * self.mapa_tmx.tileheight))