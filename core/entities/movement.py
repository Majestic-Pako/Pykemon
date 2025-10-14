import pygame
from config import VELOCIDAD
def manejar_movimiento(objeto, teclas):
    if teclas[pygame.K_UP]:
        objeto.rect.y -= VELOCIDAD
    if teclas[pygame.K_DOWN]:
        objeto.rect.y += VELOCIDAD
    if teclas[pygame.K_LEFT]:
        objeto.rect.x -= VELOCIDAD
    if teclas[pygame.K_RIGHT]:
        objeto.rect.x += VELOCIDAD