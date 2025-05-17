import pygame


class Cut_interactive:
    def __init__ (self, x, y):
        self.x = x
        self.y = y


class Interactive:
    def __init__ (self, objects, x, y, w, h):
        super().__init__()
        objects.append(self)
        self.type = 'interactive'
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, scene_surface, timer):
        pygame.draw.rect(scene_surface, 'Green', (self.x, self.y, self.width, self.height))