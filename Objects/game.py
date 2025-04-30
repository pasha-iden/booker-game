import pygame

from Objects.characters import Hero
from Objects.scene import Scene


class Game:
    def __init__(self):
        self.running = True
        self.just_started = True
        self.pause = False
        self.menu_options = (('Новая игра', (350, 280), pygame.Rect(350, 280, 200, 50)),
                             ('Продолжить', (350, 350), pygame.Rect(350, 350, 220, 50)),
                             ('Сохранить', (350, 420), pygame.Rect(350, 420, 220, 50)),
                             ('Загрузить', (350, 490), pygame.Rect(350, 490, 180, 50)),
                             ('Выйти', (350, 560), pygame.Rect(350, 560, 120, 50)),
                             )


    def menu_window(self, scene_surface, hero, scene):
        self.pause = True
        game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=40)

        for option in self.menu_options:
            if option[2].collidepoint(pygame.mouse.get_pos()):
                menu_option = game_font.render(option[0], False, 'Red')
                scene_surface.blit(menu_option, option[1])

                if pygame.mouse.get_pressed()[0]:
                    if option[0] == 'Новая игра':
                        hero = Hero()
                        scene = Scene()
                        self.just_started = False

                    if option[0] == 'Продолжить':
                        self.just_started = False

                    if option[0] == 'Сохранить':
                        save_data = str(hero.x) + '\n' + str(hero.y) + '\n' + str(scene.room)
                        save_file = open("save.txt", 'w', encoding="UTF-8")
                        print(save_data, file=save_file)
                        save_file.close()
                        self.just_started = False

                    if option[0] == 'Загрузить':
                        save_file = open("save.txt", encoding="UTF-8")
                        save_data = []
                        for line in save_file:
                            save_data.append(line.rstrip("\n"))
                        save_file.close()
                        # print (save_data)
                        hero.x = int(save_data[0])
                        hero.y = int(save_data[1])
                        scene.room = int(save_data[2])
                        self.just_started = False

                    if option[0] == 'Выйти':
                        self.running = False

                    self.pause = False

            else:
                menu_option = game_font.render(option[0], False, 'Yellow')
                scene_surface.blit(menu_option, option[1])

        return hero, scene


    def transfering_room (self, hero, scene):
        if hero.hitbox.collidepoint((25, 750)) and scene.room == 3:
            scene.room = 2
            hero.x = 730
            hero.y = 30
        if hero.hitbox.collidepoint((760, 30)) and scene.room == 2:
            scene.room = 3
            hero.x = 25
            hero.y = 700
        if hero.hitbox.collidepoint((455, 760)) and scene.room == 2:
            scene.room = 1
            hero.x = 455
            hero.y = 130
        if hero.hitbox.collidepoint((455, 130)) and scene.room == 1:
            scene.room = 2
            hero.x = 455
            hero.y = 700

        return hero, scene



if __name__ == '__main__':
    pass