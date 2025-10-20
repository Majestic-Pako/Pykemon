import pygame
from config import VELOCIDAD
def manejar_movimiento(objeto, teclas, colisiones=[]):
    posicion_anterior = objeto.rect.copy()
    if teclas[pygame.K_UP]:
        objeto.rect.y -= VELOCIDAD
    if teclas[pygame.K_DOWN]:
        objeto.rect.y += VELOCIDAD
    if teclas[pygame.K_LEFT]:
        objeto.rect.x -= VELOCIDAD
    if teclas[pygame.K_RIGHT]:
        objeto.rect.x += VELOCIDAD
    
    for rect in colisiones:
        if objeto.rect.colliderect(rect):
            objeto.rect = posicion_anterior
            break