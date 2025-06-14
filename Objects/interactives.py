from symbol import parameters

import pygame


class Cut_interactive:
    def __init__ (self, parameters):
        # x, y, direction
        # 0, 1, 2
        self.x = parameters[0]
        self.y = parameters[1]
        self.direction = parameters[2]


class Interactive:
    def __init__ (self, objects, parameters):
        # x, y, w, h
        # 0  1  2  3
        super().__init__()
        objects.append(self)
        self.type = 'interactive'
        self.x = parameters[0]
        self.y = parameters[1]
        self.width = parameters[2]
        self.height = parameters[3]
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = None

    def draw(self, scene_surface, timer):
        pygame.draw.rect(scene_surface, 'Green', (self.x, self.y, self.width, self.height))