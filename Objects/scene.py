import pygame

class Scene:
    def __init__(self):
        self.image = None
        self.x = 0
        self.y = 0
        self.room = 1
        self.room_before = None

    def draw(self, scene_surface):
        if self.room == 1:
            self.image = pygame.image.load('files/images/room_outside.jpg').convert()
            scene_surface.blit(self.image, (0, 90))
        if self.room == 2:
            self.image = pygame.image.load('files/images/room_kitchen.jpg').convert()
            scene_surface.blit(self.image, (170, 0))
        if self.room == 3:
            self.image = pygame.image.load('files/images/room_large.jpg').convert()
            scene_surface.blit(self.image, (0, 0))

if __name__ == '__main__':
    pass