import pygame


class Furniture:
    def __init__ (self, objects, x, y, w, h, image, ix, iy):
        objects.append(self)
        self.type = 'furniture'
        self.image = image
        self.ix = ix
        self.iy = iy
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, scene_surface, timer):
        if self.image != None:
            image = pygame.image.load(self.image).convert_alpha()
            scene_surface.blit(image, (self.ix, self.iy))

        # отрисовка хитбоксов
        # hitbox_surface = pygame.Surface((1024, 768), pygame.SRCALPHA)
        # pygame.draw.rect(hitbox_surface, (255, 0, 0, 128), (self.x, self.y, self.width, self.height))
        # scene_surface.blit(hitbox_surface, (0, 0))
