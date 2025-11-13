#Se importa las librerias
import pytmx
import pygame
from pytmx.util_pygame import load_pygame
from core.entities.npc import NPC

#Se importa la clase mapa y se definine la inicializacion con toda su logica 
class Mapa:
    def __init__(self, ruta_mapa):
        try:
            from core.system.config import ESCALA_JUEGO
        
            self.tmx_data = load_pygame(ruta_mapa)
            print("Mapa cargado correctamente:", ruta_mapa)
            self.mapa_tmx = self.tmx_data
        
            # Dimensiones escaladas
            self.ancho = self.mapa_tmx.width * self.mapa_tmx.tilewidth * ESCALA_JUEGO
            self.alto = self.mapa_tmx.height * self.mapa_tmx.tileheight * ESCALA_JUEGO
        
        # Colisiones escaladas
            self.colisiones = []
            collision_layer = self.tmx_data.get_layer_by_name("Colisiones")
            for obj in collision_layer:
                rect = pygame.Rect(
                    obj.x * ESCALA_JUEGO, 
                    obj.y * ESCALA_JUEGO, 
                    obj.width * ESCALA_JUEGO, 
                    obj.height * ESCALA_JUEGO
                )
                self.colisiones.append(rect)
        
        # NPCs escalados
            self.npcs = []
            try:
                npc_layer = self.tmx_data.get_layer_by_name("NPC")
                if npc_layer:
                    for obj in npc_layer:
                        nombre = obj.name if hasattr(obj, 'name') else "NPC"
                        sprite_id = obj.properties.get('Sprite_id', 'default')
                        dialog_id = obj.properties.get('dialog_id', 'Sin dialogo') 
                        npc_id = obj.properties.get('npc_id', '?')
                        npc = NPC(obj.x * ESCALA_JUEGO, obj.y * ESCALA_JUEGO, nombre, sprite_id, dialog_id, npc_id)
                        self.npcs.append(npc)
                    print(f"Cargados {len(self.npcs)} NPCs")
            except ValueError:
                print("Capa 'NPC' no encontrada")
        
        # Zonas de combate escaladas
            self.zonas_combate = []
            try:
                combate_layer = self.tmx_data.get_layer_by_name("Combate")
                if combate_layer:
                    for obj in combate_layer:
                        zona = {
                            "rect": pygame.Rect(
                                obj.x * ESCALA_JUEGO, 
                                obj.y * ESCALA_JUEGO, 
                                obj.width * ESCALA_JUEGO, 
                                obj.height * ESCALA_JUEGO
                            ),
                            "encounter_rate": obj.properties.get('encounter_rate', 0.1),
                            "pokemon_ids": obj.properties.get('pokemon_ids', '').split(','),
                            "min_level": obj.properties.get('min_level', 2)
                        }
                        self.zonas_combate.append(zona)
                    print(f"Cargadas {len(self.zonas_combate)} zonas de combate")
            except ValueError:
                print("Capa 'Combate' no encontrada")
            self.portales = []
            try:
                portal_layer = self.tmx_data.get_layer_by_name("Portal")
                if portal_layer:
                    from core.system.config import ESCALA_JUEGO
                for obj in portal_layer:
                    portal = {
                        "rect": pygame.Rect(
                            obj.x * ESCALA_JUEGO, 
                            obj.y * ESCALA_JUEGO, 
                            obj.width * ESCALA_JUEGO, 
                            obj.height * ESCALA_JUEGO
                        ),
                        "target_map": obj.properties.get('target_map', ''),
                    # Multiplicar las coordenadas destino por ESCALA_JUEGO
                        "target_x": int(obj.properties.get('target_x', 0)) * ESCALA_JUEGO,
                        "target_y": int(obj.properties.get('target_y', 0)) * ESCALA_JUEGO
                    }
                    self.portales.append(portal)
                print(f"Cargados {len(self.portales)} portales")
            except ValueError:
                print("Capa 'Portal' no encontrada")
        except Exception as e:
            print("Fallo el mapa pa ...", e)
            raise
    #Se define la funcion dibujar pero pasando parametro como superficie y camera porque a a eso quiere referirse
    def dibujar(self, superficie, camera):
        from core.system.config import ESCALA_JUEGO
    
        for capa in self.mapa_tmx.visible_layers:
            if hasattr(capa, "tiles"):
                for x, y, imagen in capa.tiles():
                    if imagen:
                        px = x * self.mapa_tmx.tilewidth * ESCALA_JUEGO
                        py = y * self.mapa_tmx.tileheight * ESCALA_JUEGO
                    
                    # Escalar tile (usa NEAREST para pixel art sin blur)
                        tile_escalado = pygame.transform.scale(
                            imagen,
                            (self.mapa_tmx.tilewidth* ESCALA_JUEGO, 
                            self.mapa_tmx.tileheight* ESCALA_JUEGO)
                        )
                        superficie.blit(tile_escalado, (px - camera.x, py - camera.y))
    
        for npc in self.npcs:
            npc.dibujar(superficie, camera)