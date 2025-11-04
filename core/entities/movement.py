import pygame #Importa una libreria pygame
from core.entities.npc import NPC #importa NPC desde la carpeta core.entitities.npc
from core.system.config import VELOCIDAD #importa VELOCIDAD desde la carpeta core.system.config
def manejar_movimiento(objeto, teclas, colisiones=[], npcs=[]): #Define la funcion manejar movimiento y tiene parametros
    posicion_anterior = objeto.rect.copy() #Vuelve a la posicion anterior si este objeto lo detiene
    if teclas[pygame.K_UP]: #Si presiona tal tecla para arriba
        objeto.rect.y -= VELOCIDAD #La velocidad se resta con el objeto
    if teclas[pygame.K_DOWN]: #Si presiona tal tecla para abajo
        objeto.rect.y += VELOCIDAD #La velocidad se suma con el objeto para poder ir para abajo
    if teclas[pygame.K_LEFT]: #Si presiona la tecla derecha
        objeto.rect.x -= VELOCIDAD #La velocidad se resta con el objeto para que vaya a la derecha
    if teclas[pygame.K_RIGHT]: #Si presiona izquierda
        objeto.rect.x += VELOCIDAD #La velocidad se suma para el objeto asi va a la izquierda
    
    #Esto es un bucle para la colision, si el objeto tiene una colision, se rompe ahi y vuelve a la posicicion anterior llamada como variable
    for rect in colisiones: 
        if objeto.rect.colliderect(rect):
            objeto.rect = posicion_anterior
            break
    #Esto es para el npc para que pase lo mismo pero con NPCS
    for npc in npcs:
        if objeto.rect.colliderect(npc.rect):
            objeto.rect = posicion_anterior