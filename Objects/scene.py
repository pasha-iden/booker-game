import pygame

from Objects.furniture import Furniture


class Scene:
    def __init__(self):
        self.image = None
        self.x = 0
        self.y = 0
        self.room = 1
        self.furniture = None


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


    def placing_furniture(self):
        objects = []

        if self.room == 1:
            furnitere_in_room = ((0, 350, 200, 100),)

        if self.room == 2:
            furnitere_in_room = ((0, 350, 200, 100),
                                  (400, 250, 150, 130))

        if self.room == 3:
            furnitere_in_room = ((0, 350, 200, 100),
                                  (400, 250, 150, 130),
                                  (0, 0, 250, 200),
                                  (400, 0, 100, 150),
                                  (550, 0, 100, 100),
                                  (780, 230, 100, 100),
                                  (720, 420, 150, 130))

        for object in furnitere_in_room:
            Furniture(objects, object[0], object[1], object[2], object[3])

        self.furniture = tuple(objects)
        return False


if __name__ == '__main__':
    pass