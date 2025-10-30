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

        # Estilo
        self.color_fondo = (16, 24, 40)
        self.color_borde_oscuro = (88, 152, 200)
        self.color_borde_claro = (152, 216, 248)
        self.color_texto = (255, 255, 255)
        self.color_seleccion = (80, 120, 200)
        self.pixel = 2

        # Fuentes 
        self.fuente_titulo = pygame.font.Font(None, 32)
        self.fuente_opcion = pygame.font.Font(None, 24)
        self.fuente_small = pygame.font.Font(None, 16)

        # Debounce de input
        self._ultima_tecla = 0
        self.KEY_DELAY = 150

    def toggle(self):
        #Abrir/cerrar menú y resetear selección al abrir.
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

    def _dibujar_borde_pokemon(self, superficie, x, y, ancho, alto):
        #Dibuja borde estilo 
        p = self.pixel
        # Fondo semi-transparente
        fondo = pygame.Surface((ancho - p * 2, alto - p * 2), pygame.SRCALPHA)
        fondo.fill((*self.color_fondo, 230))
        superficie.blit(fondo, (x + p, y + p))

        # Borde exterior (oscuro)
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + p * 2, y, ancho - p * 4, p))
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + p * 2, y + alto - p, ancho - p * 4, p))
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x, y + p * 2, p, alto - p * 4))
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + ancho - p, y + p * 2, p, alto - p * 4))

        # Esquinas exteriores
        esquinas_ext = [
            (x + p, y + p),
            (x + ancho - p * 2, y + p),
            (x + p, y + alto - p * 2),
            (x + ancho - p * 2, y + alto - p * 2)
        ]
        for ex, ey in esquinas_ext:
            pygame.draw.rect(superficie, self.color_borde_oscuro, (ex, ey, p, p))

        # Borde interior (claro)
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p * 3, y + p, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p * 3, y + alto - p * 2, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p, y + p * 3, p, alto - p * 6))
        pygame.draw.rect(superficie, self.color_borde_claro, (x + ancho - p * 2, y + p * 3, p, alto - p * 6))

        esquinas_int = [
            (x + p * 2, y + p * 2),
            (x + ancho - p * 3, y + p * 2),
            (x + p * 2, y + alto - p * 3),
            (x + ancho - p * 3, y + alto - p * 3)
        ]
        for ex, ey in esquinas_int:
            pygame.draw.rect(superficie, self.color_borde_claro, (ex, ey, p, p))

    def dibujar(self, superficie):
        if not self.activo:
            return

        # Fondo y borde
        self._dibujar_borde_pokemon(superficie, self.x_menu, self.y_menu, self.ancho_menu, self.alto_menu)

        # Título
        titulo = self.fuente_titulo.render("MENU", True, self.color_texto)
        titulo_rect = titulo.get_rect(midtop=(self.x_menu + self.ancho_menu // 2, self.y_menu + 12))
        superficie.blit(titulo, titulo_rect)

        # Separador
        pygame.draw.line(
            superficie,
            self.color_borde_claro,
            (self.x_menu + 20, self.y_menu + 50),
            (self.x_menu + self.ancho_menu - 20, self.y_menu + 50),
            1
        )

        # Opciones
        for i, opcion in enumerate(self.opciones):
            y_pos = self.y_inicio + i * self.espacio_opcion

            # Fondo seleccionado
            if i == self.opcion_seleccionada:
                rect_sel = pygame.Rect(self.x_menu + 15, y_pos - 3, self.ancho_menu - 30, 30)
                pygame.draw.rect(superficie, self.color_seleccion, rect_sel, border_radius=3)
                indicador = self.fuente_opcion.render(">", True, self.color_texto)
                superficie.blit(indicador, (self.x_menu + 20, y_pos))

            texto = self.fuente_opcion.render(opcion, True, self.color_texto)
            superficie.blit(texto, (self.x_menu + 40, y_pos))

        # Instrucciones
        instrucciones = self.fuente_small.render("Z: OK  X: Cerrar", True, (200, 200, 100))
        superficie.blit(instrucciones, (self.x_menu + 20, self.y_menu + self.alto_menu - 25))

