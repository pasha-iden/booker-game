import pygame


class Chairs:
    def __init__ (self, objects, x, y, lx, ly, image, ix, iy, table, direction):
        objects.append(self)
        self.type = 'chairs'
        self.image = image
        self.ix = ix
        self.iy = iy
        self.x = x
        self.y = y
        self.landing_x = lx
        self.landing_y = ly
        self.table = table
        self.direction = direction
        self.hitbox = pygame.Rect(self.x, self.y, self.x + 48, self.y + 48)
        self.number = None

    def draw(self, scene_surface, timer):
        image = pygame.image.load(self.image).convert_alpha()
        scene_surface.blit(image, (self.ix, self.iy))
        # pygame.draw.rect(scene_surface, 'Orange', (self.x, self.y, 48, 48))
        # pygame.draw.rect(scene_surface, 'Pink', (self.landing_x, self.landing_y, 48, 48))