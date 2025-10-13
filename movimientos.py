import pygame
from numpy.ma.core import true_divide

class movimientos:
    def __init__(self):
        self.x=0
        self.y=0
        self.velocidad=1
        self.moviendo_arriba=False
        self.movimiento_abajo=False
        self.movimiento_izquierda=False
        self.movimiento_derecha=False
    def actualizar(self):
        if self.moviendo_arriba:
            self.y-=self.velocidad
        if self.movimiento_abajo:
            self.y+=self.velocidad
        if self.movimiento_izquierda:
            self.x-=self.velocidad
        if self.movimiento_derecha:
            self.x+=self.velocidad
    def posicion(self):
        return(self.x,self.y)

movimientos=movimientos()
jugando=True
while jugando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jugando=False
            pygame.quit()
            quit()
        if evento.type==pygame.KEYDOWN:
            if evento.key==pygame.K_w:
                movimientos.moviendo_arriba=True
            elif evento.key==pygame.K_s:
                movimientos.moviendo_abajo=True
            elif evento.key==pygame.K_d:
                movimientos.moviendo_izquierda=True
            elif evento.key==pygame.K_a:
                movimientos.moviendo_derecha=True
        elif evento.type==pygame.KEYUP:
            if evento.key==pygame.K_w:
                movimientos.moviendo_arriba=False
            elif evento.key==pygame.K_s:
                movimientos.moviendo_abajo=False
            elif evento.key==pygame.K_d:
                movimientos.moviendo_derecha=False
            elif evento.key==pygame.K_a:
                movimientos.moviendo_izquierda=False
movimientos.actualizar()
print(f"Posición: {movimientos.posicion()}")