import pygame

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


class Character:
    def __inin__ (self, objects):
        objects.append(self)


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

    def action(self, scene_surface, object):
        if self.hitbox.colliderect(object.hitbox):
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            action_message = game_font.render('взаимодействовать', False, 'Green')
            scene_surface.blit(action_message, (self.x - 50, self.y - 85))

if __name__ == '__main__':
    pass