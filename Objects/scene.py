import pygame

from random import randint

from Objects.chairs import Chairs
from Objects.characters import Character, Plot_character
from Objects.furniture import Furniture
from Objects.interactives import Interactive

from Objects.stages import stages


class Scene:
    def __init__(self):
        self.stage = 1
        self.act = 1
        self.act_started = False
        self.image = None
        self.phase = 1
        self.shadow = pygame.Surface((48, 48), pygame.SRCALPHA)
        pygame.draw.ellipse(self.shadow, (0, 0, 0, 80), (0, 0, 48, 24))
        self.room = 1
        self.image = pygame.image.load(stages[self.stage]['ФОНЫ'][self.room][0]).convert()
        if self.room == 1:
            self.leaves = pygame.image.load(stages[self.stage]['ФОНЫ'][11][0]).convert_alpha()
        self.furniture = None
        self.interactive = None
        self.chairs = None
        self.room_map = None
        self.empty_chairs = [[],[],[]]
        self.characters = [[],[],[]]
        self.plot_characters = [[],[],[]]


    def draw(self, scene_surface, timer, leaves):

        if self.room != 1 and not leaves:
            scene_surface.blit(self.image, (0, 0))

        if self.room == 1 and not leaves:
            if timer:
                self.phase = randint (1, 3)
            scene_surface.blit(self.image, (0, 0), stages[self.stage]['ФОНЫ'][1][self.phase])
        if self.room == 1 and leaves:
            scene_surface.blit(self.leaves, (0, 0), stages[self.stage]['ФОНЫ'][11][self.phase])


    def draw_area(self, scene_surface, timer, i):
        table = self.furniture[i].table
        for object in self.chairs:
            if object.table == table:
                object.draw(scene_surface, timer)
        for object in self.characters[self.room-1]:
            if object.on_chair and object.chair.table == table:
                object.draw_legs(scene_surface, timer)
        for object in self.characters[self.room-1]:
            if object.on_chair and object.chair.table == table and (object.direction != 'вверх-вправо' and object.direction != 'вверх' and object.direction != 'вверх-влево'):
                object.draw_torso(scene_surface, timer)
        self.furniture[i].draw(scene_surface, timer)
        for object in self.characters[self.room-1]:
            if object.on_chair and object.chair.table == table and (object.direction == 'вверх-вправо' or object.direction == 'вверх' or object.direction == 'вверх-влево'):
                object.draw_torso(scene_surface, timer)
        for object in self.characters[self.room-1]:
            if object.on_chair and object.chair.table == table:
                object.draw_head(scene_surface, timer)


    def placing_furniture(self):
        objects = []
        furniture_in_room = stages[self.stage]['ТВЕРДЫЕ ОБЪЕКТЫ'][self.room]
        for parameters in furniture_in_room:
            Furniture(objects, parameters)
        self.furniture = objects


    def placing_interactive(self):
        objects = []
        interactive_in_room = stages[self.stage]['ИНТЕРАКТИВНЫЕ ОБЪЕКТЫ (npc)'][self.room]
        for parameters in interactive_in_room:
            Interactive(objects, parameters)
        self.interactive = objects


    def placing_chairs(self):
        objects = []
        chairs_in_room = stages[self.stage]['СТУЛЬЯ (npc)'][self.room]
        for parameters in chairs_in_room:
            Chairs(objects, parameters)
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


    def placing_plot_characters(self, character_data):
        self.plot_characters[self.room-1].append(Plot_character(character_data))


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