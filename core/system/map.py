import pytmx
import pygame
from pytmx.util_pygame import load_pygame
from core.entities.npc import NPC

class Mapa:
    def __init__(self, ruta_mapa):
        try:
            from core.system.config import ESCALA_JUEGO
        
            self.tmx_data = load_pygame(ruta_mapa)
            print("[OK] Mapa cargado correctamente:", ruta_mapa)
            self.mapa_tmx = self.tmx_data
        
            self.ancho = self.mapa_tmx.width * self.mapa_tmx.tilewidth * ESCALA_JUEGO
            self.alto = self.mapa_tmx.height * self.mapa_tmx.tileheight * ESCALA_JUEGO
        
            self.colisiones = []
            collision_layer = self.tmx_data.get_layer_by_name("Colisiones")
            if collision_layer:
                for obj in collision_layer:
                    rect = pygame.Rect(
                        obj.x * ESCALA_JUEGO, 
                        obj.y * ESCALA_JUEGO, 
                        obj.width * ESCALA_JUEGO, 
                        obj.height * ESCALA_JUEGO
                    )
                    self.colisiones.append(rect)
                #print(f"[OK] Cargadas {len(self.colisiones)} colisiones")
        
            self.npcs = []
            try:
                npc_layer = self.tmx_data.get_layer_by_name("NPC")
                if npc_layer:
                    objetos = list(npc_layer)
                    
                    for obj in objetos:
                        nombre = obj.name if hasattr(obj, 'name') else "NPC"
                        sprite_id = obj.properties.get('sprite_id', 'default')
                        dialog_id = obj.properties.get('dialog_id', 'Sin dialogo') 
                        npc_id = obj.properties.get('npc_id', '?')
                        
                        try:
                            npc = NPC(
                                obj.x * ESCALA_JUEGO, 
                                obj.y * ESCALA_JUEGO, 
                                nombre, 
                                sprite_id, 
                                dialog_id, 
                                npc_id
                            )
                            self.npcs.append(npc)
                        except Exception as e:
                            #print(f"[WARN] No se pudo cargar NPC '{nombre}': {e}")
                            continue
                    
                    if self.npcs:
                        print(f"[OK] Cargados {len(self.npcs)} NPCs")
            except ValueError:
                print("[WARN] Capa 'NPC' no encontrada")
            '''
            except Exception as e:
                print(f"[WARN] Error cargando NPCs: {e}")
            '''
            self.zonas_combate = []
            try:
                combate_layer = self.tmx_data.get_layer_by_name("Combate")
                if combate_layer:
                    for obj in combate_layer:
                        pokemon_ids_raw = obj.properties.get('pokemon_ids', '')
                        zona = {
                            "rect": pygame.Rect(
                                obj.x * ESCALA_JUEGO, 
                                obj.y * ESCALA_JUEGO, 
                                obj.width * ESCALA_JUEGO, 
                                obj.height * ESCALA_JUEGO
                            ),
                            "encounter_rate": obj.properties.get('encounter_rate', 0.1),
                            "pokemon_ids": pokemon_ids_raw,
                            "min_level": obj.properties.get('min_level', 2)
                        }
                        self.zonas_combate.append(zona)
                    #print(f"[OK] Cargadas {len(self.zonas_combate)} zonas de combate")
            except ValueError:
                print("[WARN] Capa 'Combate' no encontrada")
            '''
            except Exception as e:
                print(f"[WARN] Error cargando zonas de combate: {e}")
            '''
            self.portales = []
            try:
                portal_layer = self.tmx_data.get_layer_by_name("Portal")
                if portal_layer:
                    for obj in portal_layer:
                        portal = {
                            "rect": pygame.Rect(
                                obj.x * ESCALA_JUEGO, 
                                obj.y * ESCALA_JUEGO, 
                                obj.width * ESCALA_JUEGO, 
                                obj.height * ESCALA_JUEGO
                            ),
                            "target_map": obj.properties.get('target_map', ''),
                            "target_x": int(obj.properties.get('target_x', 0)) * ESCALA_JUEGO,
                            "target_y": int(obj.properties.get('target_y', 0)) * ESCALA_JUEGO
                        }
                        self.portales.append(portal)
                    #print(f"[OK] Cargados {len(self.portales)} portales")
            
            except ValueError:
                print("[WARN] Capa 'Portal' no encontrada")
            '''
            except Exception as e:
                print(f"[WARN] Error cargando portales: {e}")
            '''
        except Exception as e:
            print(f"[ERROR] Error cargando mapa: {e}")
            raise
    
    def dibujar(self, superficie, camera):
        from core.system.config import ESCALA_JUEGO
    
        for capa in self.mapa_tmx.visible_layers:
            if hasattr(capa, "tiles"):
                for x, y, imagen in capa.tiles():
                    if imagen:
                        px = x * self.mapa_tmx.tilewidth * ESCALA_JUEGO
                        py = y * self.mapa_tmx.tileheight * ESCALA_JUEGO
                        tile_escalado = pygame.transform.scale(
                            imagen,
                            (self.mapa_tmx.tilewidth * ESCALA_JUEGO, 
                             self.mapa_tmx.tileheight * ESCALA_JUEGO)
                        )
                        superficie.blit(tile_escalado, (px - camera.x, py - camera.y))
        for npc in self.npcs:
            npc.dibujar(superficie, camera)