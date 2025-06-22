import pygame

from random import randint
from collections import deque

from Objects.skins import skins, coordinates
from Objects.tablethings import tables_data, place_data, tablethings

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


class Sub_character:
    def __init__ (self):
        self.type = 'sub_character'
        self.skin = 1
        self.image = pygame.image.load(skins[self.skin]).convert_alpha()
        self.x = 952
        self.y = 380
        self.width = 48
        self.height = 48
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 'вниз'
        self.speed = 4
        self.head_place = True

        self.stand = True
        self.on_walk = False
        self.on_chair = False
        self.chair = None
        self.have_a_deal = False
        self.deal_kind = 'сидит'
        self.on_interactive = False
        self.his_interactive = None
        self.staing = 0
        self.destination = self.chair
        self.path_to_deal = []

        self.thoughts = None


    def find_path_to_deal(self, room_map, destination):
        deal_location = (destination.y//self.speed, destination.x//self.speed)
        start = (self.y//self.speed, self.x//self.speed)
        rows = len(room_map)
        cols = len(room_map[0])

        directions = [
            (0, 1, 'вправо'),
            (0, -1, 'влево'),
            (1, 0, 'вниз'),
            (-1, 0, 'вверх'),
            (1, 1, 'вниз-вправо'),
            (-1, -1, 'вверх-влево'),
            (-1, 1, 'вверх-вправо'),
            (1, -1, 'вниз-влево')]

        queue = deque([(start, [])])
        visited = set([start])

        while queue:
            current_position, path = queue.popleft()

            if current_position == deal_location:
                path.append(destination.direction)
                self.path_to_deal = path

            x, y = current_position

            for dx, dy, direction in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < rows and 0 <= ny < cols and room_map[nx][ny] == 1 and room_map[nx + 11][ny] == 1 and room_map[nx][ny + 11] == 1 and room_map[nx + 11][ny + 11] == 1 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    new_path = path.copy()
                    new_path.append(direction)
                    queue.append(((nx, ny), new_path))


    def walk(self):
        if len(self.path_to_deal) > 1:
            self.direction = self.path_to_deal[0]
            self.on_walk = True
            if self.path_to_deal[0] == 'влево':
                self.x += -self.speed
            elif self.path_to_deal[0] == 'вниз-влево':
                self.x += -self.speed
                self.y += self.speed
            elif self.path_to_deal[0] == 'вниз':
                self.y += self.speed
            elif self.path_to_deal[0] == 'вниз-вправо':
                self.x += self.speed
                self.y += self.speed
            elif self.path_to_deal[0] == 'вправо':
                self.x += self.speed
            elif self.path_to_deal[0] == 'вверх-вправо':
                self.x += self.speed
                self.y += -self.speed
            elif self.path_to_deal[0] == 'вверх':
                self.y += -self.speed
            elif self.path_to_deal[0] == 'вверх-влево':
                self.x += -self.speed
                self.y += -self.speed
            self.path_to_deal.pop(0)
            self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        elif len(self.path_to_deal) == 1:
            if self.path_to_deal[0] != None:
                self.direction = self.path_to_deal[0]
            self.path_to_deal.pop(0)


    def thoughts_preparing(self):
        message = self.his_interactive.messages[randint(0, len(self.his_interactive.messages) - 1)]
        words_in_message = message.split()
        message_lines = ['']
        line = 0
        for word in words_in_message:
            if len(message_lines[line]) + len(word) + 1 > 20:
                message_lines.append('')
                line += 1
            elif len(message_lines[line]) != 0:
                message_lines[line] += ' '
            message_lines[line] = message_lines[line] + word
        self.thoughts = message_lines
        pass


    def draw(self, scene_surface, timer):
        # pygame.draw.rect(scene_surface, 'Blue', (self.x, self.y, 4, 4))
        if self.on_walk == False:
            scene_surface.blit(self.image, (self.x -8, self.y -62), coordinates[self.direction]['тело'])
        elif self.on_walk == True:
            scene_surface.blit(self.image, (self.x - 8, self.y - 62), coordinates[self.direction][self.head_place])
        scene_surface.blit(self.image, (self.x - 8, self.y - 62 + 4 * self.head_place), coordinates[self.direction]['голова'])
        self.on_walk = False
        if timer:
            self.head_place = not self.head_place


    def draw_legs(self, scene_surface, timer):
        scene_surface.blit(self.image, (self.x - 8, self.y - 62), coordinates[self.direction]['ноги'])
    def draw_torso(self, scene_surface, timer):
        scene_surface.blit(self.image, (self.x - 8, self.y - 62), coordinates[self.direction]['торс'])
    def draw_shoulders(self, scene_surface, timer):
        scene_surface.blit(self.image, (self.x - 8, self.y - 62), coordinates[self.direction]['плечи'])
    def draw_hands(self, scene_surface, timer):
        if self.deal_kind == 'сидит':
            scene_surface.blit(self.image, (self.x - 8, self.y - 62), coordinates[self.direction]['руки'])
        elif self.deal_kind == 'пьет':
            scene_surface.blit(self.image, (self.x - 8, self.y - 62), coordinates[self.direction]['пьет'])
    def draw_head(self, scene_surface, timer):
        scene_surface.blit(self.image, (self.x - 8, self.y - 62 + 4 * self.head_place), coordinates[self.direction]['голова'])
        if timer:
            self.head_place = not self.head_place


class Character(Sub_character):
    def __init__ (self, objects, chair, tablethings_atlas):
        super().__init__()
        objects.append(self)
        self.type = 'character'
        self.x = chair.landing_x
        self.y = chair.landing_y
        self.chair = chair
        self.direction = chair.direction
        self.stand = False
        self.on_chair = True
        self.destination = None

        self.tablethings_placing(tablethings_atlas)


    def decision(self, timer, room_map, interactive, can_go_away):
        go_away = False
        if timer and self.deal_kind == 'сидит':
            kind_of_decision = randint(1, 100)
            if 80 <= kind_of_decision <= 95 and len(interactive) != 0:
                self.have_a_deal = True
                self.deal_kind = 'интерактив'
                self.on_chair = False
                i = randint(0, len(interactive)-1)
                self.his_interactive = interactive[i]
                interactive.pop(i)
                self.destination = self.his_interactive
                self.x = self.chair.x
                self.y = self.chair.y
                self.find_path_to_deal(room_map, self.destination)


            elif 95 < kind_of_decision <= 100 and can_go_away:
                go_away = True
            elif 10 <= kind_of_decision <= 20:
                self.deal_kind = 'пьет'
                self.staing = 3
        if self.deal_kind == 'интерактив':
            if self.have_a_deal and self.x == self.destination.x and self.y == self.destination.y:
                self.have_a_deal = False
                self.on_interactive = True
                self.staing = 4
                self.thoughts_preparing()
            elif self.on_interactive and self.staing > 0 and timer:
                self.staing += -1
            elif self.on_interactive and self.staing == 0:
                interactive.append(self.his_interactive)
                self.his_interactive = None
                self.on_interactive = False
                self.destination = self.chair
                self.find_path_to_deal(room_map, self.destination)
                self.thoughts = None
            elif self.x == self.chair.x and self.y == self.chair.y and self.have_a_deal == False:
                self.deal_kind = 'сидит'
                self.on_chair = True
                self.direction = self.chair.direction
                self.x = self.chair.landing_x
                self.y = self.chair.landing_y
        elif self.deal_kind == 'пьет':
            if self.staing > 0 and timer:
                self.staing += -1
            elif self.staing == 0:
                self.deal_kind = 'сидит'

        return  interactive, go_away

    def draw_tablethings (self, scene_surface):

        if self.deal_kind != 'пьет':
            scene_surface.blit(self.cup_image, self.cup_coordinates)
        if self.laptop:
            scene_surface.blit(self.laptop_image, self.laptop_coordinates)
        elif self.book:
            scene_surface.blit(self.book_image, self.book_coordinates)
        elif self.plate:
            scene_surface.blit(self.plate_image, self.plate_coordinates)
        if self.glass:
            scene_surface.blit(self.glass_image, self.glass_coordinates)
        if self.water:
            scene_surface.blit(self.water_image, self.water_coordinates)


        # for el in self.all_coordinates:
            #     pygame.draw.circle(scene_surface, 'Red', (el[0] * 4 + place_data[self.chair.number][0][0], el[1] * 4 + place_data[self.chair.number][0][1]), 1)
            # for el in self.free_coordinates:
            #     # scene_surface.blit(self.cup_image, (el[0] * 4 + place_data[self.chair.number][0][0], el[1] * 4 + place_data[self.chair.number][0][1]))
            #     pygame.draw.circle(scene_surface, 'Green', (el[0] * 4 + place_data[self.chair.number][0][0], el[1] * 4 + place_data[self.chair.number][0][1]), 1)

    def tablethings_placing(self, tablethings_atlas):
        self.tablethings_images = tablethings_atlas
        self.square_coordinates = set()
        for i in range(place_data[self.chair.number][1][0]):
            for j in range(place_data[self.chair.number][1][1]):
                self.square_coordinates.add((i, j))
        self.all_coordinates = tables_data[self.chair.number]
        self.free_coordinates = tables_data[self.chair.number]

        # тарелка/книга/ноутбук - кружка - стакан - вода
        self.laptop = self.book = self.plate = self.glass = self.water = False
        plate_book_laptop = randint(1, 10)
        if plate_book_laptop in (9, 10) and self.chair.number != 301:
            self.laptop = True
            self.laptop_placing()
        elif plate_book_laptop in (7, 8) and self.chair.number != 301:
            self.book = True
            self.book_placing()
        elif (self.chair.number != 301 and plate_book_laptop in (3, 4, 5, 6)) or (self.chair.number == 301 and plate_book_laptop in (3, 4, 5, 6, 7, 8)):
            self.plate = True
            self.plate_placing()
        self.cup_placing()
        self.glass = randint(0, 2) > 0
        if self.glass:
            self.glass_placing()
            self.water = bool(randint(0, 1))
            if self.water:
                self.water_placing()
    def cup_placing (self):
        cup_index = randint(1, 8)
        self.cup_image = self.tablethings_images.subsurface(tablethings['Чашка'][cup_index][0])
        possible_coordinates = []
        for el in self.square_coordinates:
            i = 0
            while i < len(tablethings['Чашка'][cup_index][1]) and (tablethings['Чашка'][cup_index][1][i][0] + el[0], tablethings['Чашка'][cup_index][1][i][1] + el[1]) in self.free_coordinates:
                i += 1
            if i == len(tablethings['Чашка'][cup_index][1]):
                possible_coordinates.append((el[0], el[1]))
        choised_coordinate = randint(0, len(possible_coordinates) - 1)
        self.cup_coordinates = (possible_coordinates[choised_coordinate][0] * 4 - 2 + place_data[self.chair.number][0][0], possible_coordinates[choised_coordinate][1] * 4 - 2 + place_data[self.chair.number][0][1])
        self.cup_dotes = set()
        for el in tablethings['Чашка'][cup_index][1]:
            self.cup_dotes.add((el[0] + possible_coordinates[choised_coordinate][0], el[1] + possible_coordinates[choised_coordinate][1]))
        self.free_coordinates = self.free_coordinates - self.cup_dotes
    def laptop_placing (self):
        if self.chair.direction == 'вверх':
            self.laptop_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Ноутбук'][1][0]), 180)
            laptop_index = 1
        elif self.chair.direction == 'вниз':
            self.laptop_image = self.tablethings_images.subsurface(tablethings['Ноутбук'][1][0])
            laptop_index = 1
        elif self.chair.direction == 'вправо':
            self.laptop_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Ноутбук'][2][0]), 180)
            laptop_index = 2
        elif self.chair.direction == 'влево':
            self.laptop_image = self.tablethings_images.subsurface(tablethings['Ноутбук'][2][0])
            laptop_index = 2
        elif self.chair.direction == 'вниз-вправо':
            self.laptop_image = self.tablethings_images.subsurface(tablethings['Ноутбук'][3][0])
            laptop_index = 3
        elif self.chair.direction == 'вверх-влево':
            self.laptop_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Ноутбук'][3][0]), 180)
            laptop_index = 3
        elif self.chair.direction == 'вниз-влево':
            self.laptop_image = self.tablethings_images.subsurface(tablethings['Ноутбук'][4][0])
            laptop_index = 4
        elif self.chair.direction == 'вверх-вправо':
            self.laptop_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Ноутбук'][4][0]), 180)
            laptop_index = 4
        possible_coordinates = []
        for el in self.square_coordinates:
            i = 0
            while i < len(tablethings['Ноутбук'][laptop_index][1]) and (tablethings['Ноутбук'][laptop_index][1][i][0] + el[0], tablethings['Ноутбук'][laptop_index][1][i][1] + el[1]) in self.free_coordinates:
                i += 1
            if i == len(tablethings['Ноутбук'][laptop_index][1]):
                possible_coordinates.append((el[0], el[1]))
        choised_coordinate = randint(0, len(possible_coordinates) - 1)
        self.laptop_coordinates = (possible_coordinates[choised_coordinate][0] * 4 - 2 + place_data[self.chair.number][0][0], possible_coordinates[choised_coordinate][1] * 4 - 2 + place_data[self.chair.number][0][1])
        self.laptop_dotes = set()
        for el in tablethings['Ноутбук'][laptop_index][1]:
            self.laptop_dotes.add((el[0] + possible_coordinates[choised_coordinate][0], el[1] + possible_coordinates[choised_coordinate][1]))
        self.free_coordinates = self.free_coordinates - self.laptop_dotes
    def book_placing (self):
        if self.chair.direction == 'вниз':
            self.book_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Книга'][1][0]), 180)
            book_index = 1
        elif self.chair.direction == 'вверх':
            self.book_image = self.tablethings_images.subsurface(tablethings['Книга'][1][0])
            book_index = 1
        elif self.chair.direction == 'влево':
            self.book_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Книга'][2][0]), 180)
            book_index = 2
        elif self.chair.direction == 'вправо':
            self.book_image = self.tablethings_images.subsurface(tablethings['Книга'][2][0])
            book_index = 2
        elif self.chair.direction == 'вверх-влево':
            self.book_image = self.tablethings_images.subsurface(tablethings['Книга'][3][0])
            book_index = 3
        elif self.chair.direction == 'вниз-вправо':
            self.book_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Книга'][3][0]), 180)
            book_index = 3
        elif self.chair.direction == 'вверх-вправо':
            self.book_image = self.tablethings_images.subsurface(tablethings['Книга'][4][0])
            book_index = 4
        elif self.chair.direction == 'вниз-влево':
            self.book_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Книга'][4][0]), 180)
            book_index = 4
        possible_coordinates = []
        for el in self.square_coordinates:
            i = 0
            while i < len(tablethings['Книга'][book_index][1]) and (tablethings['Книга'][book_index][1][i][0] + el[0], tablethings['Книга'][book_index][1][i][1] + el[1]) in self.free_coordinates:
                i += 1
            if i == len(tablethings['Книга'][book_index][1]):
                possible_coordinates.append((el[0], el[1]))
        choised_coordinate = randint(0, len(possible_coordinates) - 1)
        self.book_coordinates = (possible_coordinates[choised_coordinate][0] * 4 - 2 + place_data[self.chair.number][0][0], possible_coordinates[choised_coordinate][1] * 4 - 2 + place_data[self.chair.number][0][1])
        self.book_dotes = set()
        for el in tablethings['Книга'][book_index][1]:
            self.book_dotes.add((el[0] + possible_coordinates[choised_coordinate][0], el[1] + possible_coordinates[choised_coordinate][1]))
        self.free_coordinates = self.free_coordinates - self.book_dotes
    def plate_placing (self):
        self.plate_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Тарелка'][0]), randint(0, 3) * 90)
        possible_coordinates = []
        for el in self.square_coordinates:
            i = 0
            while i < len(tablethings['Тарелка'][1]) and (tablethings['Тарелка'][1][i][0] + el[0], tablethings['Тарелка'][1][i][1] + el[1]) in self.free_coordinates:
                i += 1
            if i == len(tablethings['Тарелка'][1]):
                possible_coordinates.append((el[0], el[1]))
        choised_coordinate = randint(0, len(possible_coordinates) - 1)
        self.plate_coordinates = (possible_coordinates[choised_coordinate][0] * 4 - 2 + place_data[self.chair.number][0][0], possible_coordinates[choised_coordinate][1] * 4 - 2 + place_data[self.chair.number][0][1])
        self.plate_dotes = set()
        for el in tablethings['Тарелка'][1]:
            self.plate_dotes.add((el[0] + possible_coordinates[choised_coordinate][0], el[1] + possible_coordinates[choised_coordinate][1]))
        self.free_coordinates = self.free_coordinates - self.plate_dotes
    def glass_placing (self):
        self.glass_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Стакан'][0]), randint(0, 3) * 90)
        possible_coordinates = []
        for el in self.square_coordinates:
            i = 0
            while i < len(tablethings['Стакан'][1]) and (tablethings['Стакан'][1][i][0] + el[0], tablethings['Стакан'][1][i][1] + el[1]) in self.free_coordinates:
                i += 1
            if i == len(tablethings['Стакан'][1]):
                possible_coordinates.append((el[0], el[1]))
        if possible_coordinates != []:
            choised_coordinate = randint(0, len(possible_coordinates) - 1)
            self.glass_coordinates = (possible_coordinates[choised_coordinate][0] * 4 - 2 + place_data[self.chair.number][0][0], possible_coordinates[choised_coordinate][1] * 4 - 2 + place_data[self.chair.number][0][1])
            self.glass_dotes = set()
            for el in tablethings['Стакан'][1]:
                self.glass_dotes.add((el[0] + possible_coordinates[choised_coordinate][0], el[1] + possible_coordinates[choised_coordinate][1]))
            self.free_coordinates = self.free_coordinates - self.glass_dotes
        else:
            self.glass = False
    def water_placing (self):
        self.water_image = pygame.transform.rotate(self.tablethings_images.subsurface(tablethings['Вода'][0]), randint(0, 3) * 90)
        possible_coordinates = []
        for el in self.square_coordinates:
            i = 0
            while i < len(tablethings['Вода'][1]) and (tablethings['Вода'][1][i][0] + el[0], tablethings['Вода'][1][i][1] + el[1]) in self.free_coordinates:
                i += 1
            if i == len(tablethings['Вода'][1]):
                possible_coordinates.append((el[0], el[1]))
        if possible_coordinates != []:
            choised_coordinate = randint(0, len(possible_coordinates) - 1)
            self.water_coordinates = (possible_coordinates[choised_coordinate][0] * 4 - 2 + place_data[self.chair.number][0][0], possible_coordinates[choised_coordinate][1] * 4 - 2 + place_data[self.chair.number][0][1])
            self.water_dotes = set()
            for el in tablethings['Вода'][1]:
                self.water_dotes.add((el[0] + possible_coordinates[choised_coordinate][0], el[1] + possible_coordinates[choised_coordinate][1]))
            self.free_coordinates = self.free_coordinates - self.water_dotes
        else:
            self.water = False


class Plot_character(Sub_character):
    def __init__(self, parameters):
        super().__init__()
        self.type = 'plot_character'
        self.skin = parameters[0]
        self.name = parameters[1]
        if self.name[0:8] != 'очередь':
            head_surface = pygame.Surface((67, 67), pygame.SRCALPHA)
            head_surface.blit(self.image, (0, 0), (22, 577, 67, 111))
            self.head = pygame.transform.scale(head_surface, (100, 100))
        self.x = parameters[2]
        self.y = parameters[3]
        self.direction = parameters[4]
        self.on_chair = False


class Hero(Sub_character):
    def __init__ (self):
        super().__init__()
        self.type = 'hero'
        head_surface = pygame.Surface((67, 67), pygame.SRCALPHA)
        head_surface.blit(self.image, (0, 0), (22, 707, 67, 111))
        self.head = pygame.transform.scale(head_surface, (100, 100))


    def move(self, key, objects):
        now_x = self.x
        now_y = self.y
        if key[pygame.K_a] and self.x > 20:
            self.x += -self.speed
            self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if key[pygame.K_d] and self.x < SCREEN_WIDTH - 20 - self.width:
            self.x += self.speed
            self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        for object in objects:
            if self.hitbox.colliderect(object.hitbox):
                self.x = now_x
                self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if key[pygame.K_w] and self.y > 20:
            self.y += -self.speed
            self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if key[pygame.K_s] and self.y < SCREEN_HEIGHT - 20 - 50:
            self.y += self.speed
            self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        for object in objects:
            if self.hitbox.colliderect(object.hitbox):
                self.y = now_y
                self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        if key[pygame.K_a] and key[pygame.K_w]: self.direction = 'вверх-влево'; self.on_walk = True
        elif key[pygame.K_a] and key[pygame.K_s]: self.direction = 'вниз-влево'; self.on_walk = True
        elif key[pygame.K_d] and key[pygame.K_w]: self.direction = 'вверх-вправо'; self.on_walk = True
        elif key[pygame.K_d] and key[pygame.K_s]: self.direction = 'вниз-вправо'; self.on_walk = True
        elif key[pygame.K_a]: self.direction = 'влево'; self.on_walk = True
        elif key[pygame.K_d]: self.direction = 'вправо'; self.on_walk = True
        elif key[pygame.K_w]: self.direction = 'вверх'; self.on_walk = True
        elif key[pygame.K_s]: self.direction = 'вниз'; self.on_walk = True


if __name__ == '__main__':
    pass