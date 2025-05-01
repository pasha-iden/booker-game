import pygame

from Objects.characters import Character
from Objects.furniture import Furniture
from Objects.interactives import Interactive


class Scene:
    def __init__(self):
        self.image = None
        self.x = 0
        self.y = 0
        self.room = 1
        self.furniture = None
        self.interactive = None
        self.room_map = None
        self.characters = None


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
                                  (550, 0, 100, 100))

        for object in furnitere_in_room:
            Furniture(objects, object[0], object[1], object[2], object[3])

        self.furniture = objects


    def placing_interactive(self):
        objects = []

        if self.room == 1:
            interactive_in_room = ((600, 600, 50, 50),)

        if self.room == 2:
            interactive_in_room = ((500, 500, 50, 50),)

        if self.room == 3:
            interactive_in_room = ((400, 400, 50, 50),)

        for object in interactive_in_room:
            Interactive(objects, object[0], object[1], object[2], object[3])

        self.interactive = objects


    def placing_characters(self):
        objects = []
        Character(objects, self.room_map, self.interactive[0])
        self.characters = objects


    def mapping_room(self):
        room_map = []
        for y in range(768//5):
            rows = []
            for x in range(1024//5):
                place_empty = 1
                for object in self.furniture:
                    if object.hitbox.collidepoint((x * 5, y * 5)):
                        place_empty = 0
                rows.append(place_empty)

            room_map.append(rows)

        self.room_map = room_map


if __name__ == '__main__':
    pass