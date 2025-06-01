import pygame

from Objects.characters import Hero
from Objects.scene import Scene
from Objects.interactives import Cut_interactive

from Objects.stages import stages
from Objects.acts import act


class Game:
    def __init__(self):
        # инициация игры: системные параметры
        pygame.init()
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        # screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), flags=pygame.NOFRAME)  # базовое разрешение
        # screen = pygame.display.set_mode((1920, 1040), pygame.FULLSCREEN)
        pygame.display.set_caption('Booker - The Coffee Adventure')
        icon = pygame.image.load('Booker.png')
        pygame.display.set_icon(icon)
        self.timer_1000 = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_1000, 1000)
        self.timer_50 = pygame.USEREVENT + 2
        pygame.time.set_timer(self.timer_50, 50)
        self.clock_on = pygame.time.Clock()
        self.FPS = 60

        # переменные параметры игры
        self.running = True
        self.just_started = True
        self.pause = False
        self.timer = False
        self.timer_005 = False

        # опции меню
        self.menu_options = (('Новая игра', (350, 280), pygame.Rect(350, 280, 200, 50)),
                             ('Продолжить', (350, 350), pygame.Rect(350, 350, 220, 50)),
                             ('Сохранить', (350, 420), pygame.Rect(350, 420, 220, 50)),
                             ('Загрузить', (350, 490), pygame.Rect(350, 490, 180, 50)),
                             ('Выйти', (350, 560), pygame.Rect(350, 560, 120, 50)),
                             )

        # нажатые клавиши
        self.pushed_SPACE = False

        # технические состояния
        self.fade_animation = None
        self.wow_fade_animation = None
        self.chapter_info = None
        self.chapter_timer = None
        self.wait = None


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
        self.timer_005 = False
        for event in pygame.event.get():

            if event.type == self.timer_1000:
                self.timer = True

            if event.type == self.timer_50:
                self.timer_005 = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.just_started:
                    self.pause = not self.pause

                if event.key == pygame.K_SPACE and not self.pause:
                    self.pushed_SPACE = True

            if event.type == pygame.QUIT:
                self.running = False


    def transfering_room_initiation (self, hero, scene):
        if (hero.hitbox.collidepoint((30, 570)) and scene.room == 3) or (hero.hitbox.collidepoint((630, 90)) and scene.room == 2) or (hero.hitbox.collidepoint((445, 620)) and scene.room == 2) or (hero.hitbox.collidepoint((595, 300)) and scene.room == 1):
            self.fade_animation = -12


    def transfering_room (self, hero, scene):
        scene_before = scene.room
        if hero.hitbox.collidepoint((30, 570)) and scene.room == 3:
            scene.room = 2
            hero.x = 652
            hero.y = 80
        if hero.hitbox.collidepoint((630, 90)) and scene.room == 2:
            scene.room = 3
            hero.x = 28
            hero.y = 556
        if hero.hitbox.collidepoint((445, 620)) and scene.room == 2:
            scene.room = 1
            hero.x = 580
            hero.y = 296
        if hero.hitbox.collidepoint((595, 300)) and scene.room == 1:
            scene.room = 2
            hero.x = 424
            hero.y = 600

        if scene_before != scene.room:
            scene.image = pygame.image.load(stages[scene.stage]['ФОНЫ'][scene.room][0]).convert()
            scene.placing_furniture()
            scene.placing_interactive()
            scene.placing_chairs()
            scene.mapping_room()
            scene.placing_characters()


    def message_preparing (self, message, is_replica):
        words_in_message = message.split()
        message_lines = ['']
        line = 0
        tutorial = False
        lines_before_tutorial = 0
        for word in words_in_message:
            if word == '*':
                if message_lines != ['']:
                    message_lines.append('')
                    message_lines.append('')
                    line += 2
                    if tutorial == False:
                        lines_before_tutorial += 2
                tutorial = True

            else:
                if len(message_lines[line]) + len(word) + 1 > 30 * (1 + is_replica):
                    message_lines.append('')
                    line += 1
                    if tutorial == False:
                        lines_before_tutorial += 1
                elif len(message_lines[line]) != 0:
                    message_lines[line] += ' '
                message_lines[line] = message_lines[line] + word
        return message_lines, tutorial, lines_before_tutorial


    def cut_scene (self, hero, scene, key):

        if scene.act_started == False:
            print(act[scene.act])
            if act[scene.act][0] == 'герой идет':
                hero.destination = Cut_interactive(act[scene.act][1], act[scene.act][2])
                hero.find_path_to_deal(scene.room_map, hero.destination)
            elif act[scene.act][0] == 'реплика':
                scene.replica = act[scene.act][2]
            elif act[scene.act][0] == 'мысли героя':
                hero.thoughts = act[scene.act][1]
            elif act[scene.act][0] == 'погружение':
                self.wow_fade_animation = 0
            elif act[scene.act][0] == 'акт':
                self.chapter_info = act[scene.act][1]
                self.chapter_timer = 0
            elif act[scene.act][0] == 'ожидание':
                self.wait = 0
            elif act[scene.act][0] == 'появление персонажа':
                scene.placing_plot_characters(act[scene.act][1])
            elif act[scene.act][0] == 'затемнение и обратно':
                self.fade_animation = -12
            elif act[scene.act][0] == 'персонаж идет':
                i = 0
                while scene.plot_characters[scene.room-1][i].name != act[scene.act][1]:
                    i += 1
                scene.plot_characters[scene.room-1][i].destination = Cut_interactive(act[scene.act][2], act[scene.act][3])
                scene.plot_characters[scene.room-1][i].find_path_to_deal(scene.room_map, scene.plot_characters[scene.room-1][i].destination)
            scene.act_started = True

        if scene.act_started == True:
            if act[scene.act][0] == 'герой идет':
                if hero.path_to_deal != []:
                    hero.walk()
                else:
                    scene.act = scene.act + 1
                    scene.act_started = False
            elif act[scene.act][0] == 'реплика':
                if self.pushed_SPACE:
                    scene.replica = None
                    scene.act = scene.act + 1
                    scene.act_started = False
            elif act[scene.act][0] == 'мысли героя':
                if self.pushed_SPACE:
                    hero.thoughts = None
                    scene.act = scene.act + 1
                    scene.act_started = False
            elif act[scene.act][0] == 'погружение':
                if self.wow_fade_animation == 110:
                    self.wow_fade_animation = None
                    hero.x = act[scene.act][1]
                    hero.y = act[scene.act][2]
                    hero.hitbox = pygame.Rect(hero.x, hero.y, hero.width, hero.height)
                    self.transfering_room(hero, scene)
                    scene.act = scene.act + 1
                    scene.act_started = False
            elif act[scene.act][0] == 'акт':
                if self.chapter_timer == 4:
                    self.chapter_info = None
                    self.chapter_timer = None
                    scene.act = scene.act + 1
                    scene.act_started = False
            elif act[scene.act][0] == 'ожидание':
                if self.wait < act[scene.act][1]:
                    if self.timer:
                        self.wait += 1
                else:
                    self.wait = None
                    scene.act = scene.act + 1
                    scene.act_started = False
            elif act[scene.act][0] == 'появление персонажа':
                scene.act = scene.act + 1
                scene.act_started = False
            elif act[scene.act][0] == 'затемнение и обратно':
                if self.fade_animation == None:
                    scene.act = scene.act + 1
                    scene.act_started = False
            elif act[scene.act][0] == 'персонаж идет':
                walk_characters = False
                for plot_character in scene.plot_characters[scene.room-1]:
                    if plot_character.path_to_deal != []:
                        plot_character.walk()
                        walk_characters = True
                if walk_characters == False:
                    scene.act = scene.act + 1
                    scene.act_started = False

    # рендер всей сцены
    def render (self, scene_surface, hero, scene):
        # отрисовка сцены
        scene.draw(scene_surface, self.timer, False) # False - значит, что рисуется не листва

        # отрисовка интерактивных областей
        for object in scene.interactive:
            object.draw(scene_surface, self.timer)

        # ранжирование объектов по порядку их отрисовки
        rendering_objects = []
        for object in scene.characters[scene.room - 1]:
            if not object.on_chair:
                rendering_objects.append((object.y + hero.height * 1.5, object.type, scene.characters[scene.room - 1].index(object)))
        for object in scene.plot_characters[scene.room - 1]:
            if not object.on_chair:
                rendering_objects.append((object.y + hero.height * 1.5, object.type, scene.plot_characters[scene.room - 1].index(object)))
        for object in scene.furniture:
            if object.table == 0:
                rendering_objects.append((object.y + object.height, object.type, scene.furniture.index(object)))
            else:
                rendering_objects.append((object.y + object.height, 'table', scene.furniture.index(object)))
        rendering_objects.append((hero.y + hero.height * 1.5, 'hero', 0))
        rendering_objects.sort(key=lambda x: x[0])

        # отрисовка объектов
        for object in rendering_objects:
            if object[1] == 'character':
                scene.characters[scene.room - 1][object[2]].draw(scene_surface, self.timer)
            elif object[1] == 'plot_character':
                scene.plot_characters[scene.room - 1][object[2]].draw(scene_surface, self.timer)
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

        # отрисовка мыслей
        if hero.thoughts != None:
            message_lines, tutorial, lines_before_tutorial = self.message_preparing(hero.thoughts, False)
            pygame.draw.rect(scene_surface, 'Gray', (hero.x - 100 - 4, hero.y - 85 - len(message_lines) * 22, len(max(message_lines, key=len)) * 11, len(message_lines) * 22 + 6))
            pygame.draw.rect(scene_surface, (80, 80 ,80), (hero.x - 100 - 4, hero.y - 85 - len(message_lines) * 22, len(max(message_lines, key=len)) * 11, len(message_lines) * 22 + 6), 2)
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            l = 0
            for line in message_lines:
                if (tutorial == False) or (tutorial == True and l < lines_before_tutorial):
                    message = game_font.render(line, False, 'Black')
                else:
                    message = game_font.render(line, False, (125, 125, 125))
                scene_surface.blit(message, (hero.x - 100, hero.y - 85 - (len(message_lines) -l) * 20))
                l += 1

        # отрисовка реплик
        if scene.replica != None:

            # окно речи и имя персонажа
            message_lines, tutorial, lines_before_tutorial = self.message_preparing(scene.replica, True)
            pygame.draw.rect(scene_surface, 'Gray', (200 - 4, 600, 600, 200))
            pygame.draw.rect(scene_surface, (80, 80, 80), (200 - 4, 600, 600, 200), 2)
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            message = game_font.render(act[scene.act][1], False, 'Black')
            scene_surface.blit(message, (200, 600))

            # реплика
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            l = 0
            for line in message_lines:
                if (tutorial == False) or (tutorial == True and l < lines_before_tutorial):
                    message = game_font.render(line, False, 'Black')
                else:
                    message = game_font.render(line, False, (125, 125, 125))
                scene_surface.blit(message, (200, 630 + l * 20))
                l += 1

        # затемнение при переходе между комнатами
        if self.fade_animation != None:
            fade_surface = pygame.Surface((1024, 768), pygame.SRCALPHA)
            if abs(self.fade_animation) <= 2:
                fade = 255
            else:
                fade = 255 - 24 * (abs(self.fade_animation)  - 2)
            pygame.draw.rect(fade_surface, (0, 0, 0, fade), (0, 0, 1024, 768))
            scene_surface.blit(fade_surface, (0, 0))
            if self.timer_005:
                self.fade_animation += 1


    # рендер cюжетных спецэффектов
    def cut_effects_render(self, scene_surface, hero, scene):

        # wow-переход
        if self.wow_fade_animation != None:
            fade_surface = pygame.Surface((1024, 768), pygame.SRCALPHA)
            if self.wow_fade_animation < 52:
                fade = 0 + 5 * self.wow_fade_animation
            else:
                fade = 255
            pygame.draw.rect(fade_surface, (0, 0, 0, fade), (0, 0, 1024, 768))
            scene_surface.blit(fade_surface, (0, 0))
            if self.timer_005:
                self.wow_fade_animation += 1

        # название главы
        if self.chapter_info != None:
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=60)
            print_info = ((-4, -4, 'Orange'), (0, -4, 'Orange'), (4, -4, 'Orange'), (-4, 0, 'Orange'), (4, 0, 'Orange'), (-4, 4, 'Orange'), (0, 4, 'Orange'), (4, 4, 'Red'), (0, 0, 'Yellow'))
            for record in print_info:
                message = game_font.render(self.chapter_info[0], False, record[2])
                scene_surface.blit(message, (400 + record[0], 300 + record[1]))
            if self.timer:
                self.chapter_timer += 1

if __name__ == '__main__':
    pass