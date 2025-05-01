import pygame

from collections import deque

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


class Sub_character:
    def __init__ (self):
        self.type = 'sub_character'
        self.x = 850
        self.y = 500
        self.width = 50
        self.height = 70
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direct = 0
        self.speed = 5
        self.head_place = True

    def draw(self, scene_surface, timer):
        pygame.draw.rect(scene_surface, 'Blue', (self.x, self.y + 20, 50, 50))
        if self.head_place == True:
            pygame.draw.rect(scene_surface, 'Yellow', (self.x, self.y - 20, 50, 50))
        else:
            pygame.draw.rect(scene_surface, 'Yellow', (self.x, self.y - 15, 50, 50))
        if timer == True:
            self.head_place = not self.head_place


class Character(Sub_character):
    def __init__ (self, objects, room_map, interactive):
        super().__init__()
        objects.append(self)
        self.path_to_deal = self.find_path_to_deal(room_map, interactive)


    def find_path_to_deal(self, room_map, interactive):
        deal_location = (interactive.y//5, interactive.x//5)
        start = (self.y//5, self.x//5)
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
                return path

            x, y = current_position

            for dx, dy, direction in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < rows and 0 <= ny < cols and room_map[nx][ny] == 1 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    new_path = path.copy()
                    new_path.append(direction)
                    queue.append(((nx, ny), new_path))


    def walk(self):
        if self.path_to_deal != []:
            if self.path_to_deal[0] == 'влево':
                self.path_to_deal.pop(0)
                self.x += -self.speed
                self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
            elif self.path_to_deal[0] == 'вниз-влево':
                self.path_to_deal.pop(0)
                self.x += -self.speed
                self.y += self.speed
                self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
            elif self.path_to_deal[0] == 'вниз':
                self.path_to_deal.pop(0)
                self.y += self.speed
                self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
            elif self.path_to_deal[0] == 'вниз-вправо':
                self.path_to_deal.pop(0)
                self.x += self.speed
                self.y += self.speed
                self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
            elif self.path_to_deal[0] == 'вправо':
                self.path_to_deal.pop(0)
                self.x += self.speed
                self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
            elif self.path_to_deal[0] == 'вверх-вправо':
                self.path_to_deal.pop(0)
                self.x += self.speed
                self.y += -self.speed
                self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
            elif self.path_to_deal[0] == 'вверх':
                self.path_to_deal.pop(0)
                self.y += -self.speed
                self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
            elif self.path_to_deal[0] == 'вверх-влево':
                self.path_to_deal.pop(0)
                self.x += -self.speed
                self.y += -self.speed
                self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

class Hero(Sub_character):

    def move(self, key, objects):
        # print (objects[0].hitbox, self.hitbox)
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

    def action(self, scene_surface, objects):
        for object in objects:
            if self.hitbox.colliderect(object.hitbox):
                game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
                action_message = game_font.render('взаимодействовать', False, 'Green')
                scene_surface.blit(action_message, (self.x - 50, self.y - 85))

if __name__ == '__main__':
    pass