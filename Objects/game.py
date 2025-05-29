import pygame

from Objects.characters import Hero
from Objects.scene import Scene
from Objects.interactives import Cut_interactive

from Objects.stages import stages
from Objects.acts import act


class Game:
    def __init__(self):
        #инициация игры: системные параметры
        pygame.init()
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), flags=pygame.NOFRAME)  # базовое разрешение
        # screen = pygame.display.set_mode((1920, 1040), pygame.FULLSCREEN)
        pygame.display.set_caption('Booker - The Coffee Adventure')
        icon = pygame.image.load('Booker.png')
        pygame.display.set_icon(icon)
        self.animation_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.animation_timer, 1000)
        self.clock_on = pygame.time.Clock()
        self.FPS = 60

        #переменные параметры игры
        self.running = True
        self.just_started = True
        self.pause = False
        self.timer = False

        #опции меню
        self.menu_options = (('Новая игра', (350, 280), pygame.Rect(350, 280, 200, 50)),
                             ('Продолжить', (350, 350), pygame.Rect(350, 350, 220, 50)),
                             ('Сохранить', (350, 420), pygame.Rect(350, 420, 220, 50)),
                             ('Загрузить', (350, 490), pygame.Rect(350, 490, 180, 50)),
                             ('Выйти', (350, 560), pygame.Rect(350, 560, 120, 50)),
                             )

        self.pushed_SPACE = False


    def menu_window(self, scene_surface, hero, scene):
        self.pause = True
        game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=40)

        for option in self.menu_options:
            if option[2].collidepoint(pygame.mouse.get_pos()):
                menu_option = game_font.render(option[0], False, 'Red')
                scene_surface.blit(menu_option, option[1])

                if pygame.mouse.get_pressed()[0]:
                    if option[0] == 'Новая игра':
                        scene = Scene()
                        hero = Hero()
                        scene.placing_furniture()
                        scene.placing_interactive()
                        scene.placing_chairs()
                        scene.mapping_room()
                        scene.placing_characters()
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
                        hero = Hero()
                        scene = Scene()
                        save_file = open("save.txt", encoding="UTF-8")
                        save_data = []
                        for line in save_file:
                            save_data.append(line.rstrip("\n"))
                        save_file.close()
                        hero.x = int(save_data[0])
                        hero.y = int(save_data[1])
                        scene.room = int(save_data[2])
                        scene.image = pygame.image.load(stages[scene.stage]['ФОНЫ'][scene.room][0]).convert()
                        scene.placing_furniture()
                        scene.placing_interactive()
                        scene.placing_chairs()
                        scene.mapping_room()
                        scene.placing_characters()
                        self.just_started = False

                    if option[0] == 'Выйти':
                        self.running = False

                    self.pause = False

            else:
                menu_option = game_font.render(option[0], False, 'Yellow')
                scene_surface.blit(menu_option, option[1])

        return hero, scene


    def events_tracking(self):
        self.timer = False
        for event in pygame.event.get():

            if event.type == self.animation_timer:
                self.timer = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.just_started:
                    self.pause = not self.pause

                if event.key == pygame.K_SPACE and not self.pause:
                    self.pushed_SPACE = True

            if event.type == pygame.QUIT:
                self.running = False


    def transfering_room (self, hero, scene):
        scene_before = scene.room
        if hero.hitbox.collidepoint((30, 570)) and scene.room == 3:
            scene.room = 2
            hero.x = 650
            hero.y = 80
        if hero.hitbox.collidepoint((630, 90)) and scene.room == 2:
            scene.room = 3
            hero.x = 25
            hero.y = 560
        if hero.hitbox.collidepoint((445, 620)) and scene.room == 2:
            scene.room = 1
            hero.x = 580
            hero.y = 296
        if hero.hitbox.collidepoint((595, 300)) and scene.room == 1:
            scene.room = 2
            hero.x = 425
            hero.y = 600

        if scene_before != scene.room:
            scene.image = pygame.image.load(stages[scene.stage]['ФОНЫ'][scene.room][0]).convert()
            scene.placing_furniture()
            scene.placing_interactive()
            scene.placing_chairs()
            scene.mapping_room()
            scene.placing_characters()

        return hero, scene


    def cut_scene (self, hero, scene, key):

        if scene.act_started == False:
            print(act[scene.act]['Действие'])
            for action in act[scene.act]['Действие']:
                if action[0] == 'герой идет':
                    hero.destination = Cut_interactive(action[1], action[2])
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                elif action[0] == 'реплика героя':
                    hero.replica = action[1]
            scene.act_started = True

        if scene.act_started == True:
            if act[scene.act]['Действие'][0][0] == 'герой идет' and act[scene.act]['Окончание'] == 'герой пришел':
                if hero.path_to_deal != []:
                    hero.walk()
                else:
                    scene.act = scene.act + 1
                    scene.act_started = False
            if act[scene.act]['Действие'][0][0] == 'реплика героя' and act[scene.act]['Окончание'] == 'пробел':
                if self.pushed_SPACE:
                    hero.replica = None
                    scene.act = scene.act + 1
                    scene.act_started = False


    def render (self, scene_surface, hero, scene):
        # отрисовка сцены
        scene.draw(scene_surface, self.timer, False) # False - значит, что рисуется не листва

        # отрисовка интерактивных областей
        for object in scene.interactive:
            object.draw(scene_surface, self.timer)

        # отрисовка мебели и персонажей
        rendering_objects = []

        for object in scene.characters[scene.room - 1]:
            if not object.on_chair:
                rendering_objects.append(
                    (object.y + hero.height * 1.5, object.type, scene.characters[scene.room - 1].index(object)))
        for object in scene.furniture:
            if object.table == 0:
                rendering_objects.append((object.y + object.height, object.type, scene.furniture.index(object)))
            else:
                rendering_objects.append((object.y + object.height, 'table', scene.furniture.index(object)))
        rendering_objects.append((hero.y + hero.height * 1.5, 'hero', 0))
        rendering_objects.sort(key=lambda x: x[0])

        for object in rendering_objects:
            if object[1] == 'character':
                scene.characters[scene.room - 1][object[2]].draw(scene_surface, self.timer)
            elif object[1] == 'furniture':
                scene.furniture[object[2]].draw(scene_surface, self.timer)
            elif object[1] == 'table':
                scene.draw_area(scene_surface, self.timer, object[2])
            else:
                hero.draw(scene_surface, self.timer)

        # отрисовка листьев
        scene.draw(scene_surface, self.timer, True) # True - значит, что рисуется - листва

        # интерактивное сообщение
        if scene.interactive != None:
            hero.action(scene_surface, scene.interactive)

        if hero.replica != None:
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            message = game_font.render(hero.replica, False, 'Black')
            scene_surface.blit(message, (hero.x - 50, hero.y - 85))


if __name__ == '__main__':
    pass