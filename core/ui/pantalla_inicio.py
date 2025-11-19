import pygame
import sys

class PantallaInicio:
    """Pantalla de inicio con animaciones y transiciones"""
    
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        
        # Cargar imagen de presentación
        self.imagen_original = self._cargar_imagen()
        self.imagen_escalada = self._escalar_imagen()
        
        # Estado de la pantalla
        self.activa = True
        self.iniciando_transicion = False
        
        # Animación de parpadeo del texto
        self.mostrar_texto = True
        self.tiempo_parpadeo = 0
        self.velocidad_parpadeo = 500  # ms
        
        # Animación de fade out
        self.alpha = 255
        self.velocidad_fade = 8
        
        # Fuentes
        try:
            self.fuente_texto = pygame.font.Font(None, 24)
        except:
            self.fuente_texto = pygame.font.SysFont('arial', 24)
        
        # Superficie para fade out
        self.superficie_fade = pygame.Surface((self.ancho, self.alto))
        self.superficie_fade.fill((0, 0, 0))
    
    def _cargar_imagen(self):
        """Carga la imagen de presentación con manejo de errores"""
        try:
            imagen = pygame.image.load("assets/images/presentacion.png")
            #print("[OK] Imagen de presentación cargada")
            return imagen
        except FileNotFoundError:
            #print("[ERROR] No se encontró assets/images/presentacion.png")
            placeholder = pygame.Surface((240, 160))
            placeholder.fill((50, 50, 150))
            fuente = pygame.font.Font(None, 48)
            texto = fuente.render("PYKEMON", True, (255, 255, 255))
            rect = texto.get_rect(center=(120, 80))
            placeholder.blit(texto, rect)
            return placeholder
    
    def _escalar_imagen(self):
        """Escala la imagen manteniendo aspect ratio y centrándola"""
        img_ancho, img_alto = self.imagen_original.get_size()
        
        # Calcular escalado manteniendo aspect ratio
        escala_x = self.ancho / img_ancho
        escala_y = self.alto / img_alto
        escala = min(escala_x, escala_y)
        
        # Nuevas dimensiones
        nuevo_ancho = int(img_ancho * escala)
        nuevo_alto = int(img_alto * escala)
        
        # Escalar imagen
        imagen_escalada = pygame.transform.scale(
            self.imagen_original, 
            (nuevo_ancho, nuevo_alto)
        )
        
        # Crear superficie centrada con fondo negro
        superficie_final = pygame.Surface((self.ancho, self.alto))
        superficie_final.fill((0, 0, 0))
        
        # Centrar la imagen
        pos_x = (self.ancho - nuevo_ancho) // 2
        pos_y = (self.alto - nuevo_alto) // 2
        superficie_final.blit(imagen_escalada, (pos_x, pos_y))
        
        return superficie_final
    
    def _dibujar_texto_parpadeante(self, superficie, delta_time):
        """Dibuja el texto de instrucciones con efecto de parpadeo"""
        # Actualizar parpadeo
        self.tiempo_parpadeo += delta_time
        if self.tiempo_parpadeo >= self.velocidad_parpadeo:
            self.mostrar_texto = not self.mostrar_texto
            self.tiempo_parpadeo = 0
        
        # Dibujar solo si está visible
        if self.mostrar_texto and not self.iniciando_transicion:
            texto = "Present by croco studio - copyright 2025 derechos de Game freak"
            
            # Renderizar texto con sombra
            sombra = self.fuente_texto.render(texto, True, (0, 0, 0))
            texto_render = self.fuente_texto.render(texto, True, (255, 255, 255))
            
            # Centrar en la parte inferior
            rect_texto = texto_render.get_rect(center=(self.ancho // 2, self.alto - 40))
            rect_sombra = sombra.get_rect(center=(self.ancho // 2 + 2, self.alto - 38))
            
            superficie.blit(sombra, rect_sombra)
            superficie.blit(texto_render, rect_texto)
    
    def _actualizar_fade_out(self):
        """Actualiza la animación de fade out"""
        if self.iniciando_transicion:
            self.alpha -= self.velocidad_fade
            if self.alpha <= 0:
                self.alpha = 0
                self.activa = False
    
    def _verificar_input(self, eventos):
        """Verifica si se presionó alguna tecla para iniciar"""
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_z, pygame.K_x, pygame.K_c, 
                                    pygame.K_SPACE, pygame.K_RETURN]:
                    if not self.iniciando_transicion:
                        self.iniciando_transicion = True
                        print("[INFO] Iniciando transición...")
    
    def actualizar(self, eventos, delta_time):
        """Actualiza el estado de la pantalla de inicio"""
        if not self.activa:
            return False
        
        self._verificar_input(eventos)
        self._actualizar_fade_out()
        
        return self.activa
    
    def dibujar(self, superficie, delta_time):
        """Dibuja la pantalla de inicio con todas sus animaciones"""
        if not self.activa and self.alpha <= 0:
            return
        
        # Dibujar imagen de fondo
        superficie.blit(self.imagen_escalada, (0, 0))
        
        # Dibujar texto parpadeante
        self._dibujar_texto_parpadeante(superficie, delta_time)
        
        # Aplicar fade out si está en transición
        if self.iniciando_transicion and self.alpha < 255:
            self.superficie_fade.set_alpha(255 - self.alpha)
            superficie.blit(self.superficie_fade, (0, 0))
    
    def esta_activa(self):
        """Retorna si la pantalla de inicio sigue activa"""
        return self.activa