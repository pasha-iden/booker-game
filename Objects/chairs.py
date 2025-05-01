import pygame


class Chairs:
    def __init__ (self, objects, x, y, w, h):
        objects.append(self)
        self.type = 'chairs'
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.number = None

    def draw(self, scene_surface, timer):
        pygame.draw.rect(scene_surface, 'Orange', (self.x, self.y, self.width, self.height))