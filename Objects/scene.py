import pygame

from random import randint

from Objects.chairs import Chairs
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
        self.chairs = None
        self.room_map = None
        self.characters = [[],[],[]]


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
            interactive_in_room = ((400, 180, 50, 50),)

        for object in interactive_in_room:
            Interactive(objects, object[0], object[1], object[2], object[3])

        self.interactive = objects


    def placing_chairs(self):
        objects = []

        if self.room == 1:
            chairs_in_room = ((300, 600, 50, 50),
                              (200, 650, 50, 50))

        if self.room == 2:
            chairs_in_room = ((400, 500, 50, 50),
                              (150, 250, 50, 50))

        if self.room == 3:
            chairs_in_room = ((500, 400, 50, 50),
                              (620, 620, 50, 50))

        for object in chairs_in_room:
            Chairs(objects, object[0], object[1], object[2], object[3])

        self.chairs = objects


    def placing_characters(self):
        if self.characters[self.room-1] == []:
            empty_places = randint(0, len(self.chairs)//2)
            start_qount_characters = len(self.chairs) - empty_places
            objects = []
            empty_chairs = list(self.chairs)
            for i in range(start_qount_characters):
                current_chair = randint(0, len(empty_chairs) - 1)
                Character(objects, self.room_map, empty_chairs[current_chair], self.interactive[0])
                empty_chairs.pop(current_chair)
            self.characters[self.room-1] = objects


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