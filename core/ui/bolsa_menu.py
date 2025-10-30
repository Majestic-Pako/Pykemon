import pygame
import json
from core.system.config import *

class BolsaMenu:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        
        # Estado
        self.activo = False
        self.bolsa = {}
        self.items_lista = [] 
        self.item_seleccionado = 0
        
        # Dimensiones de la ventana (lateral derecho)
        self.ancho_ventana = 350
        self.margen_derecho = 20
        self.x_ventana = ancho_pantalla - self.ancho_ventana - self.margen_derecho
        
        # Colores estilo Pokémon
        self.color_fondo = (16, 24, 40)
        self.color_borde_oscuro = (88, 152, 200)
        self.color_borde_claro = (152, 216, 248)
        self.color_texto = (255, 255, 255)
        self.color_cantidad = (200, 200, 100)
        self.color_seleccion = (80, 120, 200, 100)
        
        # Fuentes
        self.fuente_titulo = pygame.font.Font(None, 28)
        self.fuente_item = pygame.font.Font(None, 22)
        self.fuente_cantidad = pygame.font.Font(None, 20)
        self.fuente_desc = pygame.font.Font(None, 18)
        self.fuente_pequeña = pygame.font.Font(None, 18)
        
        # Tamaño del pixel para bordes
        self.pixel = 4
        
        # Control de input
        self._ultima_tecla = 0
        self.KEY_DELAY = 150
        
        # Cargar datos de objetos
        with open("data/objects.json", "r", encoding="utf-8") as f:
            self.objects_data = json.load(f)
    
    def abrir(self, bolsa):
        """Abre el menú con la bolsa del jugador"""
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
    
    def _dibujar_borde_pokemon(self, superficie, x, y, ancho, alto):
        p = self.pixel
        
        # Fondo
        fondo = pygame.Surface((ancho - p * 4, alto - p * 4))
        fondo.fill(self.color_fondo)
        fondo.set_alpha(245)
        superficie.blit(fondo, (x + p * 2, y + p * 2))
        
        # Borde exterior (oscuro)
        rects_oscuro = [
            (x + p * 2, y, ancho - p * 4, p),
            (x + p * 2, y + alto - p, ancho - p * 4, p),
            (x, y + p * 2, p, alto - p * 4),
            (x + ancho - p, y + p * 2, p, alto - p * 4),
        ]
        for rect in rects_oscuro:
            pygame.draw.rect(superficie, self.color_borde_oscuro, rect)
        
        # Esquinas exteriores
        esquinas_ext = [
            (x + p, y + p), (x + ancho - p * 2, y + p),
            (x + p, y + alto - p * 2), (x + ancho - p * 2, y + alto - p * 2)
        ]
        for ex, ey in esquinas_ext:
            pygame.draw.rect(superficie, self.color_borde_oscuro, (ex, ey, p, p))
        
        # Borde interior (claro)
        rects_claro = [
            (x + p * 3, y + p, ancho - p * 6, p),
            (x + p * 3, y + alto - p * 2, ancho - p * 6, p),
            (x + p, y + p * 3, p, alto - p * 6),
            (x + ancho - p * 2, y + p * 3, p, alto - p * 6),
        ]
        for rect in rects_claro:
            pygame.draw.rect(superficie, self.color_borde_claro, rect)
        
        # Esquinas interiores
        esquinas_int = [
            (x + p * 2, y + p * 2), (x + ancho - p * 3, y + p * 2),
            (x + p * 2, y + alto - p * 3), (x + ancho - p * 3, y + alto - p * 3)
        ]
        for ex, ey in esquinas_int:
            pygame.draw.rect(superficie, self.color_borde_claro, (ex, ey, p, p))
    
    def _dibujar_item_slot(self, superficie, item_key, nombre, cantidad, x, y, seleccionado=False):
        """Dibuja un slot de objeto"""
        slot_alto = 45
        
        # Fondo si está seleccionado
        if seleccionado:
            fondo_sel = pygame.Surface((self.ancho_ventana - 40, slot_alto - 5))
            fondo_sel.set_alpha(100)
            fondo_sel.fill(self.color_seleccion)
            superficie.blit(fondo_sel, (x, y))
        
        # Nombre del objeto
        nombre_render = self.fuente_item.render(nombre, True, self.color_texto)
        superficie.blit(nombre_render, (x + 15, y + 8))
        
        # Cantidad (alineada a la derecha)
        cantidad_texto = f"x{cantidad}"
        cantidad_render = self.fuente_cantidad.render(cantidad_texto, True, self.color_cantidad)
        cantidad_rect = cantidad_render.get_rect(right=x + self.ancho_ventana - 60, y=y + 10)
        superficie.blit(cantidad_render, cantidad_rect)
        
        return slot_alto
    
    def _dibujar_descripcion(self, superficie, item_key, y_pos):
        if item_key not in self.objects_data:
            return
        
        descripcion = self.objects_data[item_key]["descripcion"]
        
        # Fondo para la descripción
        desc_alto = 70
        desc_rect = pygame.Rect(self.x_ventana + 15, y_pos, self.ancho_ventana - 30, desc_alto)
        pygame.draw.rect(superficie, (30, 35, 50), desc_rect, border_radius=5)
        pygame.draw.rect(superficie, self.color_borde_oscuro, desc_rect, 2, border_radius=5)
        
        # Texto de descripción (dividir en líneas si es muy largo)
        palabras = descripcion.split()
        lineas = []
        linea_actual = ""
        
        for palabra in palabras:
            test_linea = linea_actual + " " + palabra if linea_actual else palabra
            test_render = self.fuente_desc.render(test_linea, True, self.color_texto)
            if test_render.get_width() < self.ancho_ventana - 60:
                linea_actual = test_linea
            else:
                lineas.append(linea_actual)
                linea_actual = palabra
        
        if linea_actual:
            lineas.append(linea_actual)
        
        # Dibujar líneas (máximo 3)
        for i, linea in enumerate(lineas[:3]):
            linea_render = self.fuente_desc.render(linea, True, self.color_texto)
            superficie.blit(linea_render, (self.x_ventana + 25, y_pos + 10 + (i * 20)))
    
    def manejar_input(self, eventos):
        """Maneja la navegación y cierre del menú"""
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
                    # Usar objeto
                    if self.items_lista:
                        item_key = self.items_lista[self.item_seleccionado][0]
                        item_data = self.objects_data[item_key]
                        
                        # Solo permitir usar objetos de curación y debug
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
        """Dibuja el menú de bolsa"""
        if not self.activo:
            return
        
        # Calcular altura dinámica según cantidad de objetos
        slot_altura = 50
        titulo_espacio = 50
        descripcion_espacio = 80
        instrucciones_espacio = 35
        padding = 15
        
        if not self.items_lista:
            alto_ventana = 150
        else:
            items_mostrados = min(len(self.items_lista), 6)  # Máximo 6 items visibles
            alto_ventana = titulo_espacio + (items_mostrados * slot_altura) + descripcion_espacio + instrucciones_espacio + padding
        
        # Limitar altura máxima
        alto_ventana = min(alto_ventana, self.alto_pantalla - 100)
        
        # Centrar verticalmente
        y_ventana = (self.alto_pantalla - alto_ventana) // 2
        
        # Dibujar ventana
        self._dibujar_borde_pokemon(superficie, self.x_ventana, y_ventana, 
                                        self.ancho_ventana, alto_ventana)
        
        # Título con indicador
        if self.items_lista:
            titulo = self.fuente_titulo.render(
                f"BOLSA ({self.item_seleccionado + 1}/{len(self.items_lista)})", 
                True, self.color_texto
            )
        else:
            titulo = self.fuente_titulo.render("BOLSA", True, self.color_texto)
        
        titulo_rect = titulo.get_rect(centerx=self.x_ventana + self.ancho_ventana // 2, 
                                        y=y_ventana + 15)
        superficie.blit(titulo, titulo_rect)
        
        # Línea separadora
        pygame.draw.line(superficie, self.color_borde_claro,
                        (self.x_ventana + 30, y_ventana + 45),
                        (self.x_ventana + self.ancho_ventana - 30, y_ventana + 45), 1)
        
        # Verificar si hay objetos
        if not self.items_lista:
            texto = self.fuente_item.render("No tienes objetos", True, self.color_texto)
            texto_rect = texto.get_rect(center=(self.x_ventana + self.ancho_ventana // 2, 
                                                 y_ventana + alto_ventana // 2))
            superficie.blit(texto, texto_rect)
        else:
            # Dibujar objetos
            contenido_y = y_ventana + titulo_espacio
            
            for i, (item_key, nombre, cantidad) in enumerate(self.items_lista):
                seleccionado = (i == self.item_seleccionado)
                self._dibujar_item_slot(superficie, item_key, nombre, cantidad,
                                        self.x_ventana + 20, contenido_y, seleccionado)
                contenido_y += slot_altura
            
            # Descripción del objeto seleccionado
            if self.items_lista:
                item_key_sel = self.items_lista[self.item_seleccionado][0]
                desc_y = y_ventana + alto_ventana - descripcion_espacio - instrucciones_espacio
                self._dibujar_descripcion(superficie, item_key_sel, desc_y)
        
        # Instrucciones
        if len(self.items_lista) > 1:
            instrucciones = "↑↓: Navegar Z: Usar  X: Cerrar"
        else:
            instrucciones = "X: Cerrar"
        
        inst_render = self.fuente_pequeña.render(instrucciones, True, (200, 200, 100))
        superficie.blit(inst_render, (self.x_ventana + 30, 
                                        y_ventana + alto_ventana - 30))