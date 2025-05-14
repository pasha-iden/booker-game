import pygame

from random import randint

from Objects.chairs import Chairs
from Objects.characters import Character
from Objects.furniture import Furniture
from Objects.interactives import Interactive

from Objects.stages import stages


class Scene:
    def __init__(self):
        self.stage = 1
        self.image = None
        self.x = 0
        self.y = 0
        self.room = 1
        self.furniture = None
        self.interactive = None
        self.chairs = None
        self.room_map = None
        self.empty_chairs = [[],[],[]]
        self.characters = [[],[],[]]


    def draw(self, scene_surface):
        self.image = pygame.image.load(stages[self.stage]['ФОНЫ'][self.room]).convert()
        scene_surface.blit(self.image, stages[self.stage]['КООРДИНАТЫ'][self.room])

    def draw_area(self, scene_surface, i):
        table = self.furniture[i].table
        for object in self.chairs:
            if object.table == table:
                object.draw(scene_surface, True)
        self.furniture[i].draw(scene_surface, True)


    def placing_furniture(self):
        objects = []
        furniture_in_room = stages[self.stage]['ТВЕРДЫЕ ОБЪЕКТЫ'][self.room]
        for object in furniture_in_room:
            Furniture(objects, object[0], object[1], object[2], object[3], object[4], object[5], object[6], object[7])
        self.furniture = objects


    def placing_interactive(self):
        objects = []
        interactive_in_room = stages[self.stage]['ИНТЕРАКТИВНЫЕ ОБЪЕКТЫ (npc)'][self.room]
        for object in interactive_in_room:
            Interactive(objects, object[0], object[1], object[2], object[3])
        self.interactive = objects


    def placing_chairs(self):
        objects = []
        chairs_in_room = stages[self.stage]['СТУЛЬЯ (npc)'][self.room]
        for object in chairs_in_room:
            Chairs(objects, object[0], object[1], object[2], object[3], object[4], object[5], object[6], object[7])
        self.chairs = objects


    def placing_characters(self):
        if self.characters[self.room-1] == []:
            empty_places = randint(0, len(self.chairs)//2)
            start_qount_characters = len(self.chairs) - empty_places
            objects = []
            self.empty_chairs[self.room-1] = list(self.chairs)
            for i in range(start_qount_characters):
                current_chair = randint(0, len(self.empty_chairs[self.room-1]) - 1)
                Character(objects, self.room_map, self.empty_chairs[self.room-1][current_chair])
                self.empty_chairs[self.room-1].pop(current_chair)
            self.characters[self.room-1] = objects


    def adding_character(self, timer):
        if len(self.characters[self.room-1]) < len(self.chairs) and timer and randint(1, 100) > 90:
            objects = []
            current_chair = randint(0, len(self.empty_chairs[self.room - 1]) - 1)
            Character(objects, self.room_map, self.empty_chairs[self.room - 1][current_chair])
            self.empty_chairs[self.room-1].pop(current_chair)
            self.characters[self.room-1].append(objects[0])


    def mapping_room(self):
        room_map = []
        for y in range(768//4):
            rows = []
            for x in range(1024//4):
                place_empty = 1
                for object in self.furniture:
                    if object.hitbox.collidepoint((x * 4, y * 4)):
                        place_empty = 0
                rows.append(place_empty)

            room_map.append(rows)

        self.room_map = room_map


if __name__ == '__main__':
    pass