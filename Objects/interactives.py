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
        # x, y, number, direcion, messages
        # 0  1  2       3         4
        # super().__init__()
        objects.append(self)
        self.type = 'interactive'
        self.number = parameters[2]
        self.x = parameters[0]
        self.y = parameters[1]
        # self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = parameters[3]
        self.messages = parameters[4]

    def draw(self, scene_surface, timer):
        pygame.draw.rect(scene_surface, 'Green', (self.x, self.y, 40, 40))


class Hero_interactive:
    def __init__(self, objects, parameters):
        # x, y, w, h, number, direcion, messages
        # 0  1  2  3  4       5         6
        # super().__init__()
        objects.append(self)
        self.type = 'interactive'
        self.number = parameters[4]
        self.x = parameters[0]
        self.y = parameters[1]
        self.width = parameters[2]
        self.height = parameters[3]
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = parameters[5]
        self.messages = parameters[6]

    def draw(self, scene_surface, timer):
        pygame.draw.rect(scene_surface, 'Red', (self.x, self.y, self.width, self.height))