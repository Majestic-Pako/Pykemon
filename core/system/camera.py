import pygame

class Camera:
    def __init__(self, map_width, map_height, screen_width, screen_height):
        self.map_w = map_width
        self.map_h = map_height
        self.screen_w = screen_width
        self.screen_h = screen_height
        self.x = 0
        self.y = 0

    def update(self, target_rect):
        self.x = int(target_rect.centerx - self.screen_w // 2)
        self.y = int(target_rect.centery - self.screen_h // 2)
        self.x = max(0, min(self.x, self.map_w - self.screen_w))
        self.y = max(0, min(self.y, self.map_h - self.screen_h))

    def apply(self, rect):
        return rect.move(-self.x, -self.y)

    def apply_pos(self, x, y):
        return x - self.x, y - self.y