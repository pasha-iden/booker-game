import pygame


class Chairs:
    def __init__ (self, objects, parameters):
        # x, y, lx, ly, image, ix, iy, table, direction, number
        # 0  1  2   3   4      5   6   7      8          9
        objects.append(self)
        self.type = 'chairs'
        self.image = pygame.image.load(parameters[4]).convert_alpha()
        self.ix = parameters[5]
        self.iy = parameters[6]
        self.x = parameters[0]
        self.y = parameters[1]
        self.landing_x = parameters[2]
        self.landing_y = parameters[3]
        self.table = parameters[7]
        self.direction = parameters[8]
        self.hitbox = pygame.Rect(self.x, self.y, self.x + 48, self.y + 48)
        self.number = parameters[9]


    def draw(self, scene_surface, timer):
        scene_surface.blit(self.image, (self.ix, self.iy))
        # pygame.draw.rect(scene_surface, 'Orange', (self.x, self.y, 48, 48))
        # pygame.draw.rect(scene_surface, 'Pink', (self.landing_x, self.landing_y, 48, 48))


if __name__ == '__main__':
    pass