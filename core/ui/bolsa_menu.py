import pygame
import json
from core.system.config import *

class BolsaMenu:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.activo = False
        self.bolsa = {}
        self.items_lista = [] 
        self.item_seleccionado = 0
        self.ancho_ventana = 350
        self.margen_derecho = 20
        self.x_ventana = ancho_pantalla - self.ancho_ventana - self.margen_derecho
        self.color_fondo = (248, 248, 248)  
        self.color_fondo_sombra = (200, 200, 192)
        self.color_borde_externo = (0, 0, 0)
        self.color_borde_claro = (248, 248, 248)
        self.color_borde_medio = (104, 104, 104)
        self.color_borde_oscuro = (56, 56, 56)
        self.color_texto = (80, 80, 80)
        self.color_texto_claro = (120, 120, 120)
        self.color_cantidad = (200, 120, 40) 
        self.color_seleccion = (240, 200, 120)  
        self.color_seleccion_borde = (200, 160, 80)  
        self.color_desc_fondo = (232, 232, 224)
        self.color_desc_borde = (104, 104, 104)
        self.fuente_titulo = pygame.font.Font(None, 26)
        self.fuente_item = pygame.font.Font(None, 20)
        self.fuente_cantidad = pygame.font.Font(None, 18)
        self.fuente_desc = pygame.font.Font(None, 16)
        self.fuente_pequeña = pygame.font.Font(None, 16)
        self.pixel = 4
        self._ultima_tecla = 0
        self.KEY_DELAY = 150
        
        with open("data/objects.json", "r", encoding="utf-8") as f:
            self.objects_data = json.load(f)
    
    def abrir(self, bolsa):
        self.activo = True
        self.bolsa = bolsa
        self.item_seleccionado = 0
        self._actualizar_items_lista()
        self._ultima_tecla = pygame.time.get_ticks()

    def cerrar(self):
        self.activo = False
    
    def _actualizar_items_lista(self):
        self.items_lista = []
        for categoria in ["curacion", "captura", "debug"]:
            if categoria in self.bolsa:
                for item_key, cantidad in self.bolsa[categoria].items():
                    if cantidad > 0:
                        nombre = self.objects_data[item_key]["nombre"]
                        self.items_lista.append((item_key, nombre, cantidad))
    
    def _dibujar_borde_pokemon_gba(self, superficie, x, y, ancho, alto):
        p = self.pixel
        
        fondo = pygame.Surface((ancho - p * 4, alto - p * 4))
        fondo.fill(self.color_fondo)
        superficie.blit(fondo, (x + p * 2, y + p * 2))
        
        sombra = pygame.Surface((ancho - p * 6, alto - p * 6))
        sombra.fill(self.color_fondo_sombra)
        sombra.set_alpha(30)
        superficie.blit(sombra, (x + p * 4, y + p * 4))
        
        pygame.draw.rect(superficie, self.color_borde_externo, (x + p * 2, y, ancho - p * 4, p))
        pygame.draw.rect(superficie, self.color_borde_externo, (x + p * 2, y + alto - p, ancho - p * 4, p))
        pygame.draw.rect(superficie, self.color_borde_externo, (x, y + p * 2, p, alto - p * 4))
        pygame.draw.rect(superficie, self.color_borde_externo, (x + ancho - p, y + p * 2, p, alto - p * 4))
        
        esquinas_ext = [
            (x + p, y + p), (x + ancho - p * 2, y + p),
            (x + p, y + alto - p * 2), (x + ancho - p * 2, y + alto - p * 2)
        ]
        for ex, ey in esquinas_ext:
            pygame.draw.rect(superficie, self.color_borde_externo, (ex, ey, p, p))
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p * 3, y + p, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p, y + p * 3, p, alto - p * 6))
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + p * 3, y + alto - p * 2, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + ancho - p * 2, y + p * 3, p, alto - p * 6))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + p * 4, y + p * 2, ancho - p * 8, p))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + p * 2, y + p * 4, p, alto - p * 8))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + p * 4, y + alto - p * 3, ancho - p * 8, p))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + ancho - p * 3, y + p * 4, p, alto - p * 8))
        
        esquinas_int = [
            (x + p * 2, y + p * 2), (x + ancho - p * 3, y + p * 2),
            (x + p * 2, y + alto - p * 3), (x + ancho - p * 3, y + alto - p * 3)
        ]
        for ex, ey in esquinas_int:
            pygame.draw.rect(superficie, self.color_borde_medio, (ex, ey, p, p))
    
    def _dibujar_item_slot(self, superficie, item_key, nombre, cantidad, x, y, seleccionado=False):
        slot_alto = 42
        
        if seleccionado:
            rect_sel = pygame.Rect(x - 2, y - 2, self.ancho_ventana - 36, slot_alto)
            pygame.draw.rect(superficie, self.color_seleccion, rect_sel)
            pygame.draw.rect(superficie, self.color_seleccion_borde, rect_sel, 2)
            
            pygame.draw.circle(superficie, self.color_texto, (x + 8, y + slot_alto // 2), 3)
        
        nombre_render = self.fuente_item.render(nombre, False, self.color_texto)
        superficie.blit(nombre_render, (x + 18, y + 6))
        
        cantidad_texto = f"x{cantidad}"
        cantidad_render = self.fuente_cantidad.render(cantidad_texto, False, self.color_cantidad)
        cantidad_rect = cantidad_render.get_rect(right=x + self.ancho_ventana - 50, y=y + 20)
        superficie.blit(cantidad_render, cantidad_rect)
        
        return slot_alto
    
    def _dibujar_descripcion(self, superficie, item_key, y_pos):
        if item_key not in self.objects_data:
            return
        
        descripcion = self.objects_data[item_key]["descripcion"]
        
        desc_alto = 65
        desc_x = self.x_ventana + 18
        desc_ancho = self.ancho_ventana - 36
        
        pygame.draw.rect(superficie, self.color_desc_fondo, (desc_x, y_pos, desc_ancho, desc_alto))
        pygame.draw.rect(superficie, self.color_desc_borde, (desc_x, y_pos, desc_ancho, desc_alto), 2)
        pygame.draw.rect(superficie, self.color_borde_claro, (desc_x + 2, y_pos + 2, desc_ancho - 4, desc_alto - 4), 1)
        
        palabras = descripcion.split()
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            test_linea = linea_actual + " " + palabra if linea_actual else palabra
            test_render = self.fuente_desc.render(test_linea, False, self.color_texto)
            if test_render.get_width() < desc_ancho - 20:
                linea_actual = test_linea
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        
        if linea_actual:
            lineas.append(linea_actual)
        
        for i, linea in enumerate(lineas[:3]):
            linea_render = self.fuente_desc.render(linea, False, self.color_texto)
            superficie.blit(linea_render, (desc_x + 10, y_pos + 8 + (i * 18)))
    
    def manejar_input(self, eventos):
        if not self.activo:
            return None
        
        tiempo_actual = pygame.time.get_ticks()
        
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if tiempo_actual - self._ultima_tecla < self.KEY_DELAY:
                    continue
                
                if evento.key == pygame.K_UP:
                    if self.items_lista:
                        self.item_seleccionado = (self.item_seleccionado - 1) % len(self.items_lista)
                    self._ultima_tecla = tiempo_actual
                
                elif evento.key == pygame.K_DOWN:
                    if self.items_lista:
                        self.item_seleccionado = (self.item_seleccionado + 1) % len(self.items_lista)
                    self._ultima_tecla = tiempo_actual
                
                elif evento.key == pygame.K_z or evento.key == pygame.K_RETURN:
                    if self.items_lista:
                        item_key = self.items_lista[self.item_seleccionado][0]
                        item_data = self.objects_data[item_key]
                        
                        if item_data["tipo"] in ["curacion", "debug"]:
                            self._ultima_tecla = tiempo_actual
                            return ("USAR_OBJETO", item_key)
                    self._ultima_tecla = tiempo_actual
                
                elif evento.key == pygame.K_x:
                    self.cerrar()
                    self._ultima_tecla = tiempo_actual
                    return "VOLVER"
        
        return None
    
    def dibujar(self, superficie):
        if not self.activo:
            return
        
        slot_altura = 46
        titulo_espacio = 50
        descripcion_espacio = 75
        instrucciones_espacio = 32
        padding = 15
        
        if not self.items_lista:
            alto_ventana = 150
        else:
            items_mostrados = min(len(self.items_lista), 6)
            alto_ventana = titulo_espacio + (items_mostrados * slot_altura) + descripcion_espacio + instrucciones_espacio + padding
        
        alto_ventana = min(alto_ventana, self.alto_pantalla - 100)
        y_ventana = (self.alto_pantalla - alto_ventana) // 2
        
        self._dibujar_borde_pokemon_gba(superficie, self.x_ventana, y_ventana, 
                                        self.ancho_ventana, alto_ventana)
        
        if self.items_lista:
            titulo = self.fuente_titulo.render(
                f"BOLSA ({self.item_seleccionado + 1}/{len(self.items_lista)})", 
                False, self.color_texto
            )
        else:
            titulo = self.fuente_titulo.render("BOLSA", False, self.color_texto)
        
        titulo_rect = titulo.get_rect(centerx=self.x_ventana + self.ancho_ventana // 2, 
                                        y=y_ventana + 12)
        superficie.blit(titulo, titulo_rect)
        
        pygame.draw.line(superficie, self.color_borde_medio,
                        (self.x_ventana + 25, y_ventana + 40),
                        (self.x_ventana + self.ancho_ventana - 25, y_ventana + 40), 2)
        
        if not self.items_lista:
            texto = self.fuente_item.render("No tienes objetos", False, self.color_texto)
            texto_rect = texto.get_rect(center=(self.x_ventana + self.ancho_ventana // 2, 
                                                 y_ventana + alto_ventana // 2))
            superficie.blit(texto, texto_rect)
        else:
            contenido_y = y_ventana + titulo_espacio
            
            for i, (item_key, nombre, cantidad) in enumerate(self.items_lista):
                seleccionado = (i == self.item_seleccionado)
                self._dibujar_item_slot(superficie, item_key, nombre, cantidad,
                                        self.x_ventana + 22, contenido_y, seleccionado)
                contenido_y += slot_altura
            
            if self.items_lista:
                item_key_sel = self.items_lista[self.item_seleccionado][0]
                desc_y = y_ventana + alto_ventana - descripcion_espacio - instrucciones_espacio
                self._dibujar_descripcion(superficie, item_key_sel, desc_y)
        
        if self.items_lista and self.objects_data[self.items_lista[self.item_seleccionado][0]]["tipo"] in ["curacion", "debug"]:
            if len(self.items_lista) > 1:
                instrucciones = "Z: Usar  X: Cerrar"
            else:
                instrucciones = "Z: Usar  X: Cerrar"
        else:
            instrucciones = "X: Cerrar"
        
        inst_render = self.fuente_pequeña.render(instrucciones, False, self.color_texto_claro)
        superficie.blit(inst_render, (self.x_ventana + 22, 
                                        y_ventana + alto_ventana - 25))