import pygame
from core.system.config import *

class MenuManager:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla

        # Estado
        self.activo = False
        self.opcion_seleccionada = 0
        self.opciones = ["POKEMON", "BOLSA", "SALIR"]

        # Layout 
        self.ancho_menu = 200
        self.alto_menu = 250
        self.x_menu = ancho_pantalla - self.ancho_menu - 30
        self.y_menu = 50
        self.y_inicio = self.y_menu + 70
        self.espacio_opcion = 45

        self.color_fondo = (248, 248, 248)  
        self.color_fondo_sombra = (200, 200, 192)
        
        self.color_borde_externo = (0, 0, 0)
        self.color_borde_claro = (248, 248, 248)
        self.color_borde_medio = (104, 104, 104)
        self.color_borde_oscuro = (56, 56, 56)
        
        # Texto y selección
        self.color_texto = (80, 80, 80)  
        self.color_seleccion = (200, 120, 120)  
        self.color_seleccion_borde = (160, 80, 80)  
        self.color_info = (112, 112, 112)
        
        self.pixel = 4

        self.fuente_titulo = pygame.font.Font(None, 28)
        self.fuente_opcion = pygame.font.Font(None, 22)
        self.fuente_small = pygame.font.Font(None, 16)

        self._ultima_tecla = 0
        self.KEY_DELAY = 150

    def toggle(self):
        self.activo = not self.activo
        if self.activo:
            self.opcion_seleccionada = 0

    def manejar_input(self, eventos):
        if not self.activo:
            return None

        tiempo_actual = pygame.time.get_ticks()
        for evento in eventos:
            if evento.type != pygame.KEYDOWN:
                continue

            if tiempo_actual - self._ultima_tecla < self.KEY_DELAY:
                continue

            if evento.key == pygame.K_UP:
                self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                self._ultima_tecla = tiempo_actual
            elif evento.key == pygame.K_DOWN:
                self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                self._ultima_tecla = tiempo_actual
            elif evento.key in (pygame.K_z, pygame.K_RETURN):
                self._ultima_tecla = tiempo_actual
                return self.opciones[self.opcion_seleccionada]
            elif evento.key == pygame.K_x:
                self.activo = False
                self._ultima_tecla = tiempo_actual
                return None

        return None

    def _dibujar_borde_pokemon_gba(self, superficie, x, y, ancho, alto):
        p = self.pixel
        
        fondo = pygame.Surface((ancho - p * 4, alto - p * 4))
        fondo.fill(self.color_fondo)
        superficie.blit(fondo, (x + p * 2, y + p * 2))
        
        sombra = pygame.Surface((ancho - p * 6, alto - p * 6))
        sombra.fill(self.color_fondo_sombra)
        sombra.set_alpha(30)
        superficie.blit(sombra, (x + p * 4, y + p * 4))
        
        # === BORDE EXTERNO (Negro) ===
        pygame.draw.rect(superficie, self.color_borde_externo, (x + p * 2, y, ancho - p * 4, p))
        pygame.draw.rect(superficie, self.color_borde_externo, (x + p * 2, y + alto - p, ancho - p * 4, p))
        pygame.draw.rect(superficie, self.color_borde_externo, (x, y + p * 2, p, alto - p * 4))
        pygame.draw.rect(superficie, self.color_borde_externo, (x + ancho - p, y + p * 2, p, alto - p * 4))
        
        # Esquinas externas
        esquinas_ext = [
            (x + p, y + p), (x + ancho - p * 2, y + p),
            (x + p, y + alto - p * 2), (x + ancho - p * 2, y + alto - p * 2)
        ]
        for ex, ey in esquinas_ext:
            pygame.draw.rect(superficie, self.color_borde_externo, (ex, ey, p, p))
        
        # === HIGHLIGHT (Blanco) ===
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p * 3, y + p, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p, y + p * 3, p, alto - p * 6))
        
        # === SOMBRA (Gris oscuro) ===
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + p * 3, y + alto - p * 2, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + ancho - p * 2, y + p * 3, p, alto - p * 6))
        
        # === BORDE MEDIO (Gris medio) ===
        pygame.draw.rect(superficie, self.color_borde_medio, (x + p * 4, y + p * 2, ancho - p * 8, p))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + p * 2, y + p * 4, p, alto - p * 8))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + p * 4, y + alto - p * 3, ancho - p * 8, p))
        pygame.draw.rect(superficie, self.color_borde_medio, (x + ancho - p * 3, y + p * 4, p, alto - p * 8))
        
        # Esquinas internas
        esquinas_int = [
            (x + p * 2, y + p * 2), (x + ancho - p * 3, y + p * 2),
            (x + p * 2, y + alto - p * 3), (x + ancho - p * 3, y + alto - p * 3)
        ]
        for ex, ey in esquinas_int:
            pygame.draw.rect(superficie, self.color_borde_medio, (ex, ey, p, p))

    def dibujar(self, superficie):
        if not self.activo:
            return

        self._dibujar_borde_pokemon_gba(superficie, self.x_menu, self.y_menu, self.ancho_menu, self.alto_menu)

        titulo = self.fuente_titulo.render("MENU", False, self.color_texto)
        titulo_rect = titulo.get_rect(midtop=(self.x_menu + self.ancho_menu // 2, self.y_menu + 12))
        superficie.blit(titulo, titulo_rect)

        pygame.draw.line(
            superficie,
            self.color_borde_medio,
            (self.x_menu + 20, self.y_menu + 45),
            (self.x_menu + self.ancho_menu - 20, self.y_menu + 45),
            2
        )

        for i, opcion in enumerate(self.opciones):
            y_pos = self.y_inicio + i * self.espacio_opcion

            if i == self.opcion_seleccionada:
                rect_sel = pygame.Rect(self.x_menu + 12, y_pos - 4, self.ancho_menu - 24, 28)
                pygame.draw.rect(superficie, self.color_seleccion, rect_sel)
                pygame.draw.rect(superficie, self.color_seleccion_borde, rect_sel, 2)
                
                indicador = self.fuente_opcion.render(">", False, self.color_texto)
                superficie.blit(indicador, (self.x_menu + 18, y_pos - 2))

            texto = self.fuente_opcion.render(opcion, False, self.color_texto)
            superficie.blit(texto, (self.x_menu + 38, y_pos))

        instrucciones = self.fuente_small.render("Z: OK  X: Cerrar", False, self.color_info)
        superficie.blit(instrucciones, (self.x_menu + 18, self.y_menu + self.alto_menu - 25))