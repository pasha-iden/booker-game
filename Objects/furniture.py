import pygame


class Furniture:
    def __init__ (self, objects, parameters):
        # x, y, w, h, image, ix, iy, table
        # 0  1  2  3  4      5   6   7
        objects.append(self)
        self.type = 'furniture'
        self.picture = parameters[4]
        if self.picture != None:
            self.image = pygame.image.load(self.picture).convert_alpha()
        self.ix = parameters[5]
        self.iy = parameters[6]
        self.x = parameters[0]
        self.y = parameters[1]
        self.width = parameters[2]
        self.height = parameters[3]
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.table = parameters[7]

    def draw(self, scene_surface, timer):
        if self.picture != None:
            scene_surface.blit(self.image, (self.ix, self.iy))

        # отрисовка хитбоксов
        # hitbox_surface = pygame.Surface((1024, 768), pygame.SRCALPHA)
        # pygame.draw.rect(hitbox_surface, (255, 0, 0, 128), (self.x, self.y, self.width, self.height))
        # scene_surface.blit(hitbox_surface, (0, 0))
