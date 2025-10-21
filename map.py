import pytmx
import pygame
from pytmx.util_pygame import load_pygame
from core.entities.npc import NPC

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
            self.npcs = []
            npc_layer = self.tmx_data.get_layer_by_name("NPC")
            if npc_layer:
                for obj in npc_layer:
                    nombre = obj.name if hasattr(obj, 'name') else "NPC"
                    sprite_id = obj.properties.get('Sprite_id', 'default')
                    dialog_id = obj.properties.get('dialog_id', 'Sin dialogo') 
                    npc_id=obj.properties.get('npc_id', '?')
                    npc = NPC(obj.x, obj.y, nombre, sprite_id, dialog_id, npc_id)
                    self.npcs.append(npc)
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
                for npc in self.npcs:
                    npc.dibujar(superficie, camera)