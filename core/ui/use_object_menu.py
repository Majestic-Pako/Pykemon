import pygame
from core.system.config import *

class UsarObjetoMenu:
    def __init__(self, ancho_pantalla, alto_pantalla):
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        
        self.activo = False
        self.equipo_pokemon = []
        self.pokemon_seleccionado = 0
        self.item_nombre = ""
        
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
        self.color_seleccion = (120, 160, 200)  
        self.color_seleccion_borde = (80, 120, 160)  
        self.color_info = (112, 112, 112)
        
        self.fuente_titulo = pygame.font.Font(None, 24)
        self.fuente_nombre = pygame.font.Font(None, 20)
        self.fuente_info = pygame.font.Font(None, 18)
        
        self.pixel = 4
        
        self._ultima_tecla = 0
        self.KEY_DELAY = 150
    
    def abrir(self, equipo_pokemon, item_nombre):
        self.activo = True
        self.equipo_pokemon = equipo_pokemon
        self.item_nombre = item_nombre
        self.pokemon_seleccionado = 0
        self._ultima_tecla = pygame.time.get_ticks()
    
    def cerrar(self):
        self.activo = False
    
    def _dibujar_borde_pokemon_gba(self, superficie, x, y, ancho, alto):
        p = self.pixel
        
        # Fondo principal
        fondo = pygame.Surface((ancho - p * 4, alto - p * 4))
        fondo.fill(self.color_fondo)
        superficie.blit(fondo, (x + p * 2, y + p * 2))
        
        # Sombra interna
        sombra = pygame.Surface((ancho - p * 6, alto - p * 6))
        sombra.fill(self.color_fondo_sombra)
        sombra.set_alpha(30)
        superficie.blit(sombra, (x + p * 4, y + p * 4))
        
        # === BORDE EXTERNO (Negro) ===
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
        
        # === HIGHLIGHT (Blanco) ===
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p * 3, y + p, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_claro, (x + p, y + p * 3, p, alto - p * 6))
        
        # === SOMBRA (Gris oscuro) ===
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + p * 3, y + alto - p * 2, ancho - p * 6, p))
        pygame.draw.rect(superficie, self.color_borde_oscuro, (x + ancho - p * 2, y + p * 3, p, alto - p * 6))
        
        # === BORDE MEDIO ===
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
    
    def manejar_input(self, eventos):
        if not self.activo:
            return None
        
        tiempo_actual = pygame.time.get_ticks()
        
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if tiempo_actual - self._ultima_tecla < self.KEY_DELAY:
                    continue
                
                if evento.key == pygame.K_UP:
                    self.pokemon_seleccionado = (self.pokemon_seleccionado - 1) % len(self.equipo_pokemon)
                    self._ultima_tecla = tiempo_actual
                
                elif evento.key == pygame.K_DOWN:
                    self.pokemon_seleccionado = (self.pokemon_seleccionado + 1) % len(self.equipo_pokemon)
                    self._ultima_tecla = tiempo_actual
                
                elif evento.key == pygame.K_z or evento.key == pygame.K_RETURN:
                    self._ultima_tecla = tiempo_actual
                    return ("CONFIRMAR", self.pokemon_seleccionado)
                
                elif evento.key == pygame.K_x:
                    self.cerrar()
                    self._ultima_tecla = tiempo_actual
                    return "CANCELAR"
        
        return None
    
    def dibujar(self, superficie):
        if not self.activo:
            return
        
        slot_altura = 48
        titulo_espacio = 65
        instrucciones_espacio = 32
        padding = 15
        
        alto_ventana = titulo_espacio + (len(self.equipo_pokemon) * slot_altura) + instrucciones_espacio + padding
        alto_ventana = min(alto_ventana, self.alto_pantalla - 100)
        
        y_ventana = (self.alto_pantalla - alto_ventana) // 2
        
        self._dibujar_borde_pokemon_gba(superficie, self.x_ventana, y_ventana, 
                                        self.ancho_ventana, alto_ventana)
        
        titulo = self.fuente_titulo.render(f"Usar {self.item_nombre}", False, self.color_texto)
        titulo_rect = titulo.get_rect(centerx=self.x_ventana + self.ancho_ventana // 2, 
                                        y=y_ventana + 12)
        superficie.blit(titulo, titulo_rect)
        
        subtitulo = self.fuente_info.render("Selecciona un Pokemon", False, self.color_texto_claro)
        subtitulo_rect = subtitulo.get_rect(centerx=self.x_ventana + self.ancho_ventana // 2, 
                                            y=y_ventana + 35)
        superficie.blit(subtitulo, subtitulo_rect)
        
        pygame.draw.line(superficie, self.color_borde_medio,
                        (self.x_ventana + 25, y_ventana + 55),
                        (self.x_ventana + self.ancho_ventana - 25, y_ventana + 55), 2)
        
        contenido_y = y_ventana + titulo_espacio
        
        for i, pokemon in enumerate(self.equipo_pokemon):
            seleccionado = (i == self.pokemon_seleccionado)
            
            if seleccionado:
                rect_sel = pygame.Rect(self.x_ventana + 18, contenido_y - 3, 
                                        self.ancho_ventana - 36, 42)
                pygame.draw.rect(superficie, self.color_seleccion, rect_sel)
                pygame.draw.rect(superficie, self.color_seleccion_borde, rect_sel, 2)
                
                # Indicador de flecha
                flecha = self.fuente_nombre.render(">", False, self.color_texto)
                superficie.blit(flecha, (self.x_ventana + 24, contenido_y + 2))
            
            nombre_texto = f"{pokemon.nombre}  Nv.{pokemon.nivel}"
            nombre_render = self.fuente_nombre.render(nombre_texto, False, self.color_texto)
            superficie.blit(nombre_render, (self.x_ventana + 42, contenido_y + 4))
            
            ps_texto = f"PS: {pokemon.ps_actual}/{pokemon.stats_actuales['ps']}"
            ps_render = self.fuente_info.render(ps_texto, False, self.color_texto_claro)
            superficie.blit(ps_render, (self.x_ventana + 42, contenido_y + 24))
            
            contenido_y += slot_altura
        
        if len(self.equipo_pokemon) > 1:
            instrucciones = "Z: Confirmar  X: Cancelar"
        else:
            instrucciones = "Z: Confirmar  X: Cancelar"
        
        inst_render = self.fuente_info.render(instrucciones, False, self.color_info)
        superficie.blit(inst_render, (self.x_ventana + 22, 
                                        y_ventana + alto_ventana - 25))