import pygame


class Chairs:
    def __init__ (self, objects, x, y, lx, ly):
        objects.append(self)
        self.type = 'chairs'
        self.x = x
        self.y = y
        self.landing_x = lx
        self.landing_y = ly
        self.hitbox = pygame.Rect(self.x, self.y, self.x + 48, self.y + 48)
        self.number = None

    def draw(self, scene_surface, timer):
        pygame.draw.rect(scene_surface, 'Orange', (self.x, self.y, 48, 48))
        pygame.draw.rect(scene_surface, 'Pink', (self.landing_x, self.landing_y, 48, 48))