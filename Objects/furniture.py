import pygame

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class Furniture:
    def __init__ (self, objects, x, y, w, h):
        objects.append(self)
        self.type = 'furniture'
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, scene_surface, timer):
        pygame.draw.rect(scene_surface, 'Red', (self.x, self.y - 20, self.width, self.height + 15))