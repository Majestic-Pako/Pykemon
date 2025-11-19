import pygame
import sys
import math

class PantallaInicio:
    
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        
        self.color_superior = (0, 51, 128)  
        self.color_inferior = (8, 152, 104)   
        
        self.imagen_original = self._cargar_imagen()
        self.imagen_escalada = self._escalar_imagen()
        
        self.logo_central = self._cargar_logo_central()
        self.tiempo_logo = 0
        self.alpha_logo = 0
        self.fade_in_logo = True
        
        self.activa = True
        self.iniciando_transicion = False
        
        self.mostrar_texto = True
        self.tiempo_parpadeo = 0
        self.velocidad_parpadeo = 1500  #
        
        self.alpha = 255
        self.velocidad_fade = 2  
        
        try:
            self.fuente_texto = pygame.font.SysFont('courier', 16, bold=True)
        except:
            print("[WARN] No se pudo cargar la fuente pixelart, usando fuente por defecto.")
        
        self.superficie_fade = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        self.superficie_fade.fill((0, 0, 0, 255))
    
    def _cargar_imagen(self):
        try:
            imagen = pygame.image.load("assets/images/presentacion.png")
            return imagen
        except FileNotFoundError:
            placeholder = pygame.Surface((240, 160))
            placeholder.fill((50, 50, 150))
            fuente = pygame.font.Font(None, 48)
            texto = fuente.render("PYKEMON", True, (255, 255, 255))
            rect = texto.get_rect(center=(120, 80))
            placeholder.blit(texto, rect)
            return placeholder
    
    def _cargar_logo_central(self):
        try:
            # Aca va la imagen del logo 
            logo = pygame.image.load("assets/images/logo_letras.png")
            return pygame.transform.scale(logo, (300, 100))
        except FileNotFoundError:
            placeholder = pygame.Surface((300, 80), pygame.SRCALPHA)
            placeholder.fill((0, 0, 0, 0))
            fuente = pygame.font.Font(None, 60)
            texto = fuente.render("TEXTO", True, (255, 255, 255))
            rect = texto.get_rect(center=(150, 40))
            placeholder.blit(texto, rect)
            return placeholder
    
    def _escalar_imagen(self):
        img_ancho, img_alto = self.imagen_original.get_size()
        
        escala_x = self.ancho / img_ancho
        escala_y = self.alto / img_alto
        escala = min(escala_x, escala_y)
        
        nuevo_ancho = int(img_ancho * escala)
        nuevo_alto = int(img_alto * escala)
        
        imagen_escalada = pygame.transform.scale(
            self.imagen_original, 
            (nuevo_ancho, nuevo_alto)
        )
        
        superficie_final = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        superficie_final.fill((0, 0, 0, 0)) 
        
        pos_x = (self.ancho - nuevo_ancho) // 2
        pos_y = (self.alto - nuevo_alto) // 2
        superficie_final.blit(imagen_escalada, (pos_x, pos_y))
        
        return superficie_final
    
    def _dibujar_fondos_color(self, superficie):
        altura_mitad = self.alto // 2
        
        pygame.draw.rect(superficie, self.color_superior, 
                        (0, 0, self.ancho, altura_mitad))
        
        pygame.draw.rect(superficie, self.color_inferior, 
                        (0, altura_mitad, self.ancho, altura_mitad))
    
    def _dibujar_textos_separados(self, superficie, delta_time):
        self.tiempo_parpadeo += delta_time
        
        ciclo = (self.tiempo_parpadeo % self.velocidad_parpadeo) / self.velocidad_parpadeo
        alpha_texto = int(155 + 100 * math.sin(ciclo * math.pi * 2)) 
        
        if not self.iniciando_transicion:
            texto_superior = "© 2025 Game Freak - Non commercial use"
            texto_sup_render = self.fuente_texto.render(texto_superior, True, (255, 255, 255))
            texto_sup_render.set_alpha(alpha_texto)
            rect_sup = texto_sup_render.get_rect(center=(self.ancho // 2, 25))
            superficie.blit(texto_sup_render, rect_sup)
            
            texto_inferior = "Presented by Croco Studio"
            texto_inf_render = self.fuente_texto.render(texto_inferior, True, (255, 255, 255))
            texto_inf_render.set_alpha(alpha_texto)
            rect_inf = texto_inf_render.get_rect(center=(self.ancho // 2, self.alto - 25))
            superficie.blit(texto_inf_render, rect_inf)
    
    def _actualizar_logo_central(self, delta_time):
        self.tiempo_logo += delta_time
        velocidad_fade_logo = 2.0  
        
        if self.fade_in_logo:
            self.alpha_logo += velocidad_fade_logo * delta_time / 10
            if self.alpha_logo >= 255:
                self.alpha_logo = 255
                self.fade_in_logo = False
        else:
            # Fade out
            if self.tiempo_logo > 500: 
                self.alpha_logo -= velocidad_fade_logo * delta_time / 15
                if self.alpha_logo <= 0:
                    self.alpha_logo = 0
                    self.fade_in_logo = True
                    self.tiempo_logo = 0
    
    def _dibujar_logo_central(self, superficie):
        if self.alpha_logo > 0 and not self.iniciando_transicion:
            logo_con_alpha = self.logo_central.copy()
            logo_con_alpha.set_alpha(int(self.alpha_logo))
            
            rect_logo = logo_con_alpha.get_rect(center=(self.ancho // 2, self.alto // 2))
            superficie.blit(logo_con_alpha, rect_logo)
    
    def _actualizar_fade_out(self):
        if self.iniciando_transicion:
            self.alpha -= self.velocidad_fade
            if self.alpha <= 0:
                self.alpha = 0
                self.activa = False
    
    def _verificar_input(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_z, pygame.K_x, pygame.K_c, 
                                    pygame.K_SPACE, pygame.K_RETURN]:
                    if not self.iniciando_transicion:
                        self.iniciando_transicion = True
    
    def actualizar(self, eventos, delta_time):
        if not self.activa:
            return False
        
        self._verificar_input(eventos)
        self._actualizar_fade_out()
        self._actualizar_logo_central(delta_time)
        
        return self.activa
    
    def dibujar(self, superficie, delta_time):
        if not self.activa and self.alpha <= 0:
            return
        
        self._dibujar_fondos_color(superficie)
        superficie.blit(self.imagen_escalada, (0, 0))
        self._dibujar_logo_central(superficie)  # Logo en el centro
        self._dibujar_textos_separados(superficie, delta_time)
        
        if self.iniciando_transicion and self.alpha < 255:
            self.superficie_fade.set_alpha(255 - self.alpha)
            superficie.blit(self.superficie_fade, (0, 0))
    
    def esta_activa(self):
        return self.activa