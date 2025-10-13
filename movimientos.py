import pygame

class movimientos:
    def __init__(self):
        self.x=0
        self.y=0
        self.velocidad=velocidad
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


