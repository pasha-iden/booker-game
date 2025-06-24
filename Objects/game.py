import pygame

from random import randint
from rubish.time_detector import time_counter

from Objects.characters import Hero
from Objects.scene import Scene
from Objects.interactives import Cut_interactive

from Objects.stages import stages
from Objects.acts import act

from Objects.barista import Barista


class Game:
    def __init__(self):
        # инициация игры: системные параметры
        pygame.init()
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.shift_x = 0
        self.shift_y = 0
        self.scale_value = 1
        self.screen_mod = 1
        # print(pygame.display.list_modes())
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))  # базовое разрешение
        pygame.display.set_caption('Booker - The Coffee Adventure')
        icon = pygame.image.load('Booker.png')
        pygame.display.set_icon(icon)

        # шрифты
        self.game_font = pygame.font.Font('Files/Fonts/Roboto_Condensed-Medium.ttf', size=20)
        self.menu_font = pygame.font.Font('Files/Fonts/Roboto_Condensed-Medium.ttf', size=40)
        self.chapter_font = pygame.font.Font('Files/Fonts/Roboto_Condensed-Medium.ttf', size=60)

        # таймеры
        self.timer_1000 = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_1000, 1000)
        self.timer_50 = pygame.USEREVENT + 2
        pygame.time.set_timer(self.timer_50, 50)
        self.clock_on = pygame.time.Clock()
        self.FPS = 60

        # переменные параметры игры
        self.running = True
        self.just_started = True
        self.pause = True
        self.settings = False
        self.timer = False
        self.timer_005 = False

        # опции меню
        self.menu_options = (('Новая игра', (350, 280), pygame.Rect(350, 280, 200, 50)),
                             ('Продолжить', (350, 350), pygame.Rect(350, 350, 220, 50)),
                             ('Сохранить', (350, 420), pygame.Rect(350, 420, 220, 50)),
                             ('Загрузить', (350, 490), pygame.Rect(350, 490, 180, 50)),
                             ('Настройки', (350, 560), pygame.Rect(350, 560, 180, 50)),
                             ('Выйти', (350, 630), pygame.Rect(350, 630, 120, 50)),
                             )
        self.menu_settings = (('Полноэкранный режим', (350, 280), pygame.Rect(350, 280, 400, 50)),
                              ('Оконный режим (без рамок)', (350, 350), pygame.Rect(350, 350, 470, 50)),
                              ('Оконный режим (с рамками)', (350, 420), pygame.Rect(350, 420, 470, 50)),
                              )

        # нажатые клавиши
        self.key_pushed = False
        self.mouse_left = False
        self.keys_clear()

        # технические состояния
        self.fade_animation = None
        self.wow_fade_animation = None
        self.chapter_info = None
        self.chapter_timer = None
        self.wait = None

        # мысли и реплики
        self.prepared_message = None

        # переменные для игры бариста
        self.barista = None
        self.barista_letter = None
        self.counted_cook_time = None
        self.counted_order_time = None

        # пост-эффекты
        # шумы
        self.dots_surface = pygame.Surface((1024, 768))
        self.doting_stage = 0
        # слои цветовых фильтров и их окрашивание
        self.red_mask = pygame.Surface((1024, 768), pygame.SRCALPHA)
        self.green_mask = pygame.Surface((1024, 768), pygame.SRCALPHA)
        self.blue_mask = pygame.Surface((1024, 768), pygame.SRCALPHA)
        self.red_mask.fill((255, 0, 0, 255))
        self.green_mask.fill((0, 255, 0, 255))
        self.blue_mask.fill((0, 0, 255, 255))
        # полосы
        self.lines_surface = pygame.Surface((1024, 768), pygame.SRCALPHA)
        for y in range(0, 768, 3):
            pygame.draw.line(self.lines_surface, (0, 0, 0, 40), (0, y), (1024, y), 1)



    def menu_window(self, scene_surface, hero, scene):
        if not self.just_started and self.pushed_ESCAPE and not self.settings:
            self.pause = not self.pause
            self.pushed_ESCAPE = False

        if self.settings:
            options = self.menu_settings
            if self.pushed_ESCAPE:
                self.settings = False
                self.pushed_ESCAPE = False
        else:
            options = self.menu_options

        for option in options:
            if option[2].collidepoint(pygame.mouse.get_pos()):
                menu_option = self.menu_font.render(option[0], False, 'Red')
                scene_surface.blit(menu_option, option[1])

                # if pygame.mouse.get_pressed()[0]:
                if self.mouse_left:
                    screen_mod_before = self.screen_mod
                    if option[0] == 'Новая игра':
                        scene = Scene()
                        hero = Hero()
                        scene.placing_furniture()
                        scene.placing_interactive()
                        scene.placing_chairs()
                        scene.mapping_room()
                        scene.placing_characters()
                        self.prepared_message = None
                        self.just_started = False
                        self.pause = False

                    elif option[0] == 'Продолжить' and not self.just_started:
                        self.just_started = False
                        self.pause = False

                    elif option[0] == 'Сохранить' and not self.just_started:
                        save_data = str(hero.x) + '\n' + str(hero.y) + '\n' + str(scene.room) + '\n' + str(scene.act)
                        save_file = open("save.txt", 'w', encoding="UTF-8")
                        print(save_data, file=save_file)
                        save_file.close()
                        self.just_started = False
                        self.pause = False

                    elif option[0] == 'Загрузить':
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
                        scene.act = int(save_data[3])
                        scene.image = pygame.image.load(stages[scene.stage]['ФОНЫ'][scene.room][0]).convert()

                        scene.placing_furniture()
                        scene.placing_interactive()
                        scene.placing_chairs()
                        scene.mapping_room()
                        scene.placing_characters()
                        self.prepared_message = None
                        self.just_started = False
                        self.pause = False

                    elif option[0] == 'Настройки':
                        self.settings = True
                    elif option[0] == 'Полноэкранный режим':
                        self.screen = pygame.display.set_mode((1920, 1200), pygame.FULLSCREEN) # или 1080
                        self.screen_mod = 2
                        self.settings = False
                    elif option[0] == 'Оконный режим (без рамок)':
                        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), flags=pygame.NOFRAME)
                        self.screen_mod = 1
                        self.settings = False
                    elif option[0] == 'Оконный режим (с рамками)':
                        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                        self.screen_mod = 1
                        self.settings = False

                    elif option[0] == 'Выйти':
                        self.running = False

                    if screen_mod_before != self.screen_mod:
                        if self.screen_mod == 1:
                            self.shift_x = 0
                            self.shift_y = 0
                            self.scale_value = 1
                            self.menu_options = (('Новая игра', (350, 280), pygame.Rect(350, 280, 200, 50)),
                                                 ('Продолжить', (350, 350), pygame.Rect(350, 350, 220, 50)),
                                                 ('Сохранить', (350, 420), pygame.Rect(350, 420, 220, 50)),
                                                 ('Загрузить', (350, 490), pygame.Rect(350, 490, 180, 50)),
                                                 ('Настройки', (350, 560), pygame.Rect(350, 560, 180, 50)),
                                                 ('Выйти', (350, 630), pygame.Rect(350, 630, 120, 50)),
                                                 )

                            self.menu_settings = (('Полноэкранный режим', (350, 280), pygame.Rect(350, 280, 400, 50)),
                                                  ('Оконный режим (без рамок)', (350, 350), pygame.Rect(350, 350, 470, 50)),
                                                  ('Оконный режим (с рамками)', (350, 420), pygame.Rect(350, 420, 470, 50)),
                                                  )
                        if self.screen_mod == 2:
                            self.shift_x = 260
                            self.shift_y = 100
                            self.scale_value = 1
                            self.menu_options = (('Новая игра', (350, 280), pygame.Rect(350 + self.shift_x, 280 + self.shift_y, 200, 50)),
                                                 ('Продолжить', (350, 350), pygame.Rect(350 + self.shift_x, 350 + self.shift_y, 220, 50)),
                                                 ('Сохранить', (350, 420), pygame.Rect(350 + self.shift_x, 420 + self.shift_y, 220, 50)),
                                                 ('Загрузить', (350, 490), pygame.Rect(350 + self.shift_x, 490 + self.shift_y, 180, 50)),
                                                 ('Настройки', (350, 560), pygame.Rect(350 + self.shift_x, 560 + self.shift_y, 180, 50)),
                                                 ('Выйти', (350, 630), pygame.Rect(350 + self.shift_x, 630 + self.shift_y, 120, 50)),
                                                 )
                            self.menu_settings = (('Полноэкранный режим', (350, 280), pygame.Rect(350 + self.shift_x, 280 + self.shift_y, 400, 50)),
                                                  ('Оконный режим (без рамок)', (350, 350), pygame.Rect(350 + self.shift_x, 350 + self.shift_y, 470, 50)),
                                                  ('Оконный режим (с рамками)', (350, 420), pygame.Rect(350 + self.shift_x, 420 + self.shift_y, 470, 50)),
                                                  )


            else:
                menu_option = self.menu_font.render(option[0], False, 'Yellow')
                scene_surface.blit(menu_option, option[1])

        return hero, scene


    def keys_clear(self):
        self.pushed_ESCAPE = False
        self.pushed_TAB = False
        self.pushed_SPACE = False
        self.pushed_BACKSPACE = False
        self.pushed_q = False
        self.pushed_w = False
        self.pushed_e = False
        self.pushed_r = False
        self.pushed_t = False
        self.pushed_y = False
        self.pushed_u = False
        self.pushed_i = False
        self.pushed_o = False
        self.pushed_p = False
        self.pushed_LEFTBRACKET = False  # клавиша [ х
        self.pushed_RIGHTBRACKET = False  # клавиша ] ъ
        self.pushed_a = False
        self.pushed_s = False
        self.pushed_d = False
        self.pushed_f = False
        self.pushed_g = False
        self.pushed_h = False
        self.pushed_j = False
        self.pushed_k = False
        self.pushed_l = False
        self.pushed_SEMICOLON = False  # клавиша ; ж
        self.pushed_QUOTE = False  # клавиша ' э
        self.pushed_z = False
        self.pushed_x = False
        self.pushed_c = False
        self.pushed_v = False
        self.pushed_b = False
        self.pushed_n = False
        self.pushed_m = False
        self.pushed_COMMA = False
        self.pushed_PERIOD = False


    def events_tracking(self):
        self.timer = False
        self.timer_005 = False

        self.mouse_left = False

        self.barista_letter = None
        if self.key_pushed:
            self.key_pushed = False
            self.keys_clear()

        for event in pygame.event.get():

            # таймеры
            if event.type == self.timer_1000:
                self.timer = True
            if event.type == self.timer_50:
                self.timer_005 = True
            if self.barista != None and not self.pause:
                if self.barista.list != None and self.barista.list != []:
                    for i in range(len(self.barista.list)):
                        if event.type == self.barista.list[i][-2]:
                            if self.barista.list[i][-1] != None and self.barista.list[i][-1] != 'неудача':
                                self.barista.list[i][-1] += -1
                if self.barista.start_timer != None:
                    if event.type == self.barista.start_timer[0]:
                        self.barista.start_timer[1] += -1
                if self.barista.speach_timer != None:
                    if event.type == self.barista.speach_timer[0]:
                        self.barista.speach_timer[1] += -1
                if self.barista.queue != None and self.barista.queue != [] and not self.barista.speach:
                    if event.type == self.barista.queue[0][1]:
                        self.barista.queue[0][2] += -1

            # левая клавиша мыши
            if event.type == pygame.MOUSEBUTTONDOWN:  # Нажата кнопка мыши
                if event.button == 1:
                    self.mouse_left = True

            # нажатые клавиши
            if event.type == pygame.KEYDOWN:
                self.key_pushed = True

                if event.key == pygame.K_ESCAPE:
                    self.pushed_ESCAPE = True
                # перечисление всех клавиш
                else:
                    if event.key == pygame.K_SPACE:
                        self.pushed_SPACE = True
                        self.barista_letter = ' '
                    elif event.key == pygame.K_TAB:
                        self.pushed_TAB = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.pushed_BACKSPACE = True
                        self.barista_letter = 'backspace'
                    elif event.key == pygame.K_q:
                        self.pushed_q = True
                        self.barista_letter = 'й'
                    elif event.key == pygame.K_w:
                        self.pushed_w = True
                        self.barista_letter = 'ц'
                    elif event.key == pygame.K_e:
                        self.pushed_e = True
                        self.barista_letter = 'у'
                    elif event.key == pygame.K_r:
                        self.pushed_r = True
                        self.barista_letter = 'к'
                    elif event.key == pygame.K_t:
                        self.pushed_t = True
                        self.barista_letter = 'е'
                    elif event.key == pygame.K_y:
                        self.pushed_y = True
                        self.barista_letter = 'н'
                    elif event.key == pygame.K_u:
                        self.pushed_u = True
                        self.barista_letter = 'г'
                    elif event.key == pygame.K_i:
                        self.pushed_i = True
                        self.barista_letter = 'ш'
                    elif event.key == pygame.K_o:
                        self.pushed_o = True
                        self.barista_letter = 'щ'
                    elif event.key == pygame.K_p:
                        self.pushed_p = True
                        self.barista_letter = 'з'
                    elif event.key == pygame.K_LEFTBRACKET:
                        self.pushed_LEFTBRACKET = True  # клавиша [ х
                        self.barista_letter = 'х'
                    elif event.key == pygame.K_RIGHTBRACKET:
                        self.pushed_RIGHTBRACKET = True  # клавиша ] ъ
                        self.barista_letter = 'ъ'
                    elif event.key == pygame.K_a:
                        self.pushed_a = True
                        self.barista_letter = 'ф'
                    elif event.key == pygame.K_s:
                        self.pushed_s = True
                        self.barista_letter = 'ы'
                    elif event.key == pygame.K_d:
                        self.pushed_d = True
                        self.barista_letter = 'в'
                    elif event.key == pygame.K_f:
                        self.pushed_f = True
                        self.barista_letter = 'а'
                    elif event.key == pygame.K_g:
                        self.pushed_g = True
                        self.barista_letter = 'п'
                    elif event.key == pygame.K_h:
                        self.pushed_h = True
                        self.barista_letter = 'р'
                    elif event.key == pygame.K_j:
                        self.pushed_j = True
                        self.barista_letter = 'о'
                    elif event.key == pygame.K_k:
                        self.pushed_k = True
                        self.barista_letter = 'л'
                    elif event.key == pygame.K_l:
                        self.pushed_l = True
                        self.barista_letter = 'д'
                    elif event.key == pygame.K_SEMICOLON:
                        self.pushed_SEMICOLON = True  # клавиша ; ж
                        self.barista_letter = 'ж'
                    elif event.key == pygame.K_QUOTE:
                        self.pushed_QUOTE = True  # клавиша ' э
                        self.barista_letter = 'э'
                    elif event.key == pygame.K_z:
                        self.pushed_z = True
                        self.barista_letter = 'я'
                    elif event.key == pygame.K_x:
                        self.pushed_x = True
                        self.barista_letter = 'ч'
                    elif event.key == pygame.K_c:
                        self.pushed_c = True
                        self.barista_letter = 'с'
                    elif event.key == pygame.K_v:
                        self.pushed_v = True
                        self.barista_letter = 'м'
                    elif event.key == pygame.K_b:
                        self.pushed_b = True
                        self.barista_letter = 'и'
                    elif event.key == pygame.K_n:
                        self.pushed_n = True
                        self.barista_letter = 'т'
                    elif event.key == pygame.K_m:
                        self.pushed_m = True
                        self.barista_letter = 'ь'
                    elif event.key == pygame.K_COMMA or pygame.key.get_pressed().index(True) == 54:
                        self.pushed_COMMA = True
                        self.barista_letter = 'б'
                    elif event.key == pygame.K_PERIOD or pygame.key.get_pressed().index(True) == 55:
                        self.pushed_PERIOD = True
                        self.barista_letter = 'ю'

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
            for character in scene.characters[scene.room-1]:
                i = 0
                deleted = False
                while i < len(scene.interactive) and not deleted:
                    if character.his_interactive != None and character.his_interactive.number == scene.interactive[i].number:
                        scene.interactive.pop(i)
                        deleted = True
                    else:
                        i += 1


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
                if len(message_lines[line]) + len(word) + 1 > 30 * (1 + is_replica) - is_replica * 10:
                    message_lines.append('')
                    line += 1
                    if tutorial == False:
                        lines_before_tutorial += 1
                elif len(message_lines[line]) != 0:
                    message_lines[line] += ' '
                message_lines[line] = message_lines[line] + word
        self.prepared_message = (message_lines, tutorial, lines_before_tutorial)


    def cut_scene (self, hero, scene):

        if scene.act_started == False:
            # print(act[scene.act])
            if act[scene.act][0] == 'герой идет':
                hero.destination = Cut_interactive(act[scene.act][1])
                hero.find_path_to_deal(scene.room_map, hero.destination)
            elif act[scene.act][0] == 'реплика' or act[scene.act][0] == 'реплика героя':
                self.message_preparing(act[scene.act][2], True)
            elif act[scene.act][0] == 'мысли героя':
                self.message_preparing(act[scene.act][1], False)
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
                scene.plot_characters[scene.room-1][i].destination = Cut_interactive(act[scene.act][2])
                scene.plot_characters[scene.room-1][i].find_path_to_deal(scene.room_map, scene.plot_characters[scene.room-1][i].destination)
            elif act[scene.act][0] == 'ОБУЧЕНИЕ БАРИСТА':
                self.barista = Barista(False)
            elif act[scene.act][0] == 'ГОТОВКА КОФЕ':
                self.barista = Barista(True, self.counted_order_time, self.counted_cook_time)
                hero.x = 400
                hero.y = 300
                hero.direction = 'вниз'
                hero.hitbox = pygame.Rect(hero.x, hero.y, hero.width, hero.height)
            if act[scene.act][0][0:8] != 'обучение':
                scene.act_started = True



        if scene.act_started == True:
            if act[scene.act][0] == 'герой идет':
                if hero.path_to_deal != []:
                    hero.walk()
                else:
                    scene.act = scene.act + 1
                    scene.act_started = False
            elif act[scene.act][0] == 'реплика' or act[scene.act][0] == 'реплика героя' :
                if self.pushed_SPACE:
                    # self.pushed_SPACE = False
                    self.barista_letter = None
                    self.prepared_message = None
                    scene.act = scene.act + 1
                    scene.act_started = False
            elif act[scene.act][0] == 'мысли героя':
                if self.pushed_SPACE:
                    # self.pushed_SPACE = False
                    self.prepared_message = None
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
            elif act[scene.act][0] == 'ОБУЧЕНИЕ БАРИСТА':
                scene.act = scene.act + 1
                scene.act_started = False
            elif act[scene.act][0] == 'ЗАВЕРШЕНИЕ ОБУЧЕНИЯ БАРИСТА':
                # self.tutorial_barista_game = False
                self.barista = None
                scene.act = scene.act + 1
                scene.act_started = False
            elif act[scene.act][0] == 'ГОТОВКА КОФЕ':
                if self.pushed_TAB or self.barista.score[2] == True:
                    self.barista = None
                    scene.act = scene.act + 1
                    scene.act_started = False


    def mini_games_logica(self, hero, scene):

        if self.barista != None:
            self.barista.logica(hero, scene, self.barista_letter, self.timer)
            if self.barista.message_preparing:
                self.message_preparing(act[scene.act][2], True)
            elif self.barista.message_preparing == False:
                self.prepared_message = None
                self.barista.message_preparing = None
            if self.barista.return_times:
                self.counted_order_time = self.barista.counted_order_time
                self.counted_cook_time = self.barista.counted_cook_time
                self.barista.counted_order_time = None
                self.barista.counted_cook_time = None
                self.barista.return_times = None


    # рендер всей сцены
    # @time_counter()
    def render (self, scene_surface, hero, scene):
        # отрисовка сцены
        scene.draw(scene_surface, self.timer, False) # False - значит, что рисуется не листва

        # интерактивные области npc
        # for object in scene.interactive:
        #     object.draw(scene_surface, self.timer)

        # интерактивные области героя
        # for object in scene.girl_interactive:
        #     object.draw(scene_surface, self.timer)

        # ранжирование объектов по порядку их отрисовки
        rendering_objects = []
        for object in scene.characters[scene.room - 1]:
            if not object.on_chair:
                rendering_objects.append((object.y + object.height * 1.5, object.type, scene.characters[scene.room - 1].index(object)))
                scene_surface.blit(scene.shadow, (object.x, object.y + 35)) # тени персонажей
        for object in scene.plot_characters[scene.room - 1]:
            if not object.on_chair:
                rendering_objects.append((object.y + object.height * 1.5, object.type, scene.plot_characters[scene.room - 1].index(object)))
                scene_surface.blit(scene.shadow, (object.x, object.y + 35)) # тени сюжетных персонажей
        for object in scene.furniture:
            if object.table == 0:
                rendering_objects.append((object.y + object.height, object.type, scene.furniture.index(object)))
            else:
                rendering_objects.append((object.y + object.height, 'table', scene.furniture.index(object)))
        rendering_objects.append((hero.y + hero.height * 1.5, 'hero', 0))
        scene_surface.blit(scene.shadow, (hero.x, hero.y + 35)) # тень героя
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

        # интерактивное сообщение и подсказка
        if scene.girl_interactive != None:
            collided = False
            for object in scene.girl_interactive:
                if hero.hitbox.colliderect(object.hitbox):
                    collided = True
                    hero.his_interactive = object
                    # подсказка
                    if hero.thoughts == None:
                        # включение интерактивного сообщение
                        if self.pushed_SPACE:
                            self.pushed_SPACE = False
                            hero.thoughts_preparing()
                        # отображение подсказки
                        else:
                            x = hero.x + 15
                            y = hero.y - 75
                            if scene.room == 2 or scene.room == 3:
                                if y < 15: y = 15
                            else:
                                if y < 97: y = 97
                            pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 25, 25))
                            pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 25, 25), 2)
                            message = self.game_font.render('?', False, 'Black')
                            scene_surface.blit(message, (x + 4, y))
                    # сообщение
                    if  hero.thoughts != None:
                        # отключение сообщения
                        if self.pushed_SPACE:
                            self.pushed_SPACE = False
                            hero.thoughts = None
                        # отображение сообщения
                        else:
                            x = hero.x + 33 - (len(max(hero.thoughts, key=len)) * 10) // 2
                            y = hero.y - 85
                            if scene.room == 1 or scene.room == 3:
                                if x < 5: x = 15
                                if (x + len(max(hero.thoughts, key=len)) * 10) > 1020: x = 1020 - len(max(hero.thoughts, key=len)) * 10
                            else:
                                if x < 207: x = 212
                                if (x + len(max(hero.thoughts, key=len)) * 10) > 842: x = 842 - len(max(hero.thoughts, key=len)) * 10
                            if scene.room == 2 or scene.room == 3:
                                if y - len(hero.thoughts) * 21 < 5: y = len(hero.thoughts) * 21 + 5
                            else:
                                if y - len(hero.thoughts) * 21 < 97: y = len(hero.thoughts) * 21 + 97
                            pygame.draw.rect(scene_surface, 'Gray', (x - 4, y - len(hero.thoughts) * 21, len(max(hero.thoughts, key=len)) * 10, len(hero.thoughts) * 22 + 6))
                            pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y - len(hero.thoughts) * 21, len(max(hero.thoughts, key=len)) * 10, len(hero.thoughts) * 22 + 6), 2)
                            l = 0
                            for line in hero.thoughts:
                                message = self.game_font.render(line, False, 'Black')
                                scene_surface.blit(message, (x, y - (len(hero.thoughts) - l) * 20))
                                l += 1
            if not collided:
                hero.his_interactive = None
                hero.thoughts = None

        # мысли NPC
        for character in scene.characters[scene.room-1]:
            if character.thoughts != None:
                x = character.x + 33 - (len(max(character.thoughts, key=len)) * 10) // 2
                y = character.y - 85
                if scene.room == 1 or scene.room == 3:
                    if x < 5: x = 15
                    if (x + len(max(character.thoughts, key=len)) * 10) > 1020: x = 1020 - len(max(character.thoughts, key=len)) * 10
                else:
                    if x < 207: x = 212
                    if (x + len(max(character.thoughts, key=len)) * 10) > 842: x = 842 - len(max(character.thoughts, key=len)) * 10
                if scene.room == 2 or scene.room == 3:
                    if y - len(character.thoughts) * 21 < 5: y = len(character.thoughts) * 21 + 5
                else:
                    if y - len(character.thoughts) * 21 < 97: y = len(character.thoughts) * 21 + 97
                pygame.draw.rect(scene_surface, 'Gray', (x - 4, y - len(character.thoughts) * 21, len(max(character.thoughts, key=len)) * 10, len(character.thoughts) * 22 + 6))
                pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y - len(character.thoughts) * 21, len(max(character.thoughts, key=len)) * 10, len(character.thoughts) * 22 + 6), 2)
                l = 0
                for line in character.thoughts:
                    message = self.game_font.render(line, False, 'Black')
                    scene_surface.blit(message, (x, y - (len(character.thoughts) - l) * 20))
                    l += 1

        # отрисовка мыслей
        if self.prepared_message != None and act[scene.act][0] == 'мысли героя':
            x = hero.x + 33 - (len(max(self.prepared_message[0], key=len)) * 10) // 2
            y = hero.y - 85
            if scene.room == 1 or scene.room == 3:
                if x < 5: x = 15
                if (x + len(max(self.prepared_message[0], key=len)) * 10) > 1020: x = 1020 - len(max(self.prepared_message[0], key=len)) * 10
            else:
                if x < 207: x = 212
                if (x + len(max(self.prepared_message[0], key=len)) * 10) > 842: x = 842 - len(max(self.prepared_message[0], key=len)) * 10
            if scene.room == 2 or scene.room == 3:
                if y - len(self.prepared_message[0]) * 21 < 5: y = len(self.prepared_message[0]) * 21 + 5
            else:
                if y - len(self.prepared_message[0]) * 21 < 97: y = len(self.prepared_message[0]) * 21 + 97
            pygame.draw.rect(scene_surface, 'Gray', (x - 4, y - len(self.prepared_message[0]) * 21, len(max(self.prepared_message[0], key=len)) * 10, len(self.prepared_message[0]) * 22 + 6))
            pygame.draw.rect(scene_surface, (80, 80 ,80), (x - 4, y - len(self.prepared_message[0]) * 21, len(max(self.prepared_message[0], key=len)) * 10, len(self.prepared_message[0]) * 22 + 6), 2)
            l = 0
            for line in self.prepared_message[0]:
                if (self.prepared_message[1] == False) or (self.prepared_message[1] == True and l < self.prepared_message[2]):
                    message = self.game_font.render(line, False, 'Black')
                else:
                    message = self.game_font.render(line, False, (125, 125, 125))
                scene_surface.blit(message, (x, y - (len(self.prepared_message[0]) -l) * 20))
                l += 1

        # отрисовка реплик
        if self.prepared_message != None and act[scene.act][0] != 'мысли героя':
            x = 220
            if scene.room == 1:
                y = 480
            else:
                y = 555
            w = 600

            # окно речи и имя персонажа
            pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, w, 200))
            pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, w, 200), 2)
            message = self.game_font.render(act[scene.act][1], False, 'Black')
            scene_surface.blit(message, (x + (act[scene.act][0] == 'реплика' or act[scene.act][0][0:8] == 'обучение') * 120, y))

            # портрет персонажа
            if act[scene.act][0] == 'реплика' or act[scene.act][0][0:8] == 'обучение':
                for character in scene.plot_characters[scene.room-1]:
                    if character.name == act[scene.act][1]:
                        scene_surface.blit(character.head, (x + 10, y + 20))
            else:
                scene_surface.blit(hero.head, (x + w - 100 - 10, y + 20))

            # реплика
            l = 0
            for line in self.prepared_message[0]:
                if (self.prepared_message[1] == False) or (self.prepared_message[1] == True and l < self.prepared_message[2]):
                    message = self.game_font.render(line, False, 'Black')
                else:
                    message = self.game_font.render(line, False, (125, 125, 125))
                scene_surface.blit(message, (x + (act[scene.act][0] == 'реплика' or act[scene.act][0][0:8] == 'обучение') * 120, y + 30 + l * 20))
                l += 1

        # рамки
        if not self.pause:
            if scene.room == 1:
                pygame.draw.rect(scene_surface, 'Black', (0, 0, 1024, 92))
                pygame.draw.rect(scene_surface, 'Black', (0, 682, 1024, 86))
                pygame.draw.rect(scene_surface, (80, 80, 80), (0, 84, 1024, 606), 4)
                pygame.draw.rect(scene_surface, 'Gray', (0 + 4, 84 + 4, 1024 - 8, 606 - 8), 4)

            if scene.room == 2:
                pygame.draw.rect(scene_surface, 'Black', (0, 0, 207, 768))
                pygame.draw.rect(scene_surface, 'Black', (847, 0, 177, 768))
                pygame.draw.rect(scene_surface, (80, 80, 80), (206, 0, 644, 768), 4)
                pygame.draw.rect(scene_surface, 'Gray', (206 + 4, 0 + 4, 644 - 8, 768 - 8), 4)

            if scene.room == 3:
                pygame.draw.rect(scene_surface, (80, 80, 80), (0, 0, 1024, 768), 4)
                pygame.draw.rect(scene_surface, 'Gray', (0 + 4, 0 + 4, 1024 - 8, 768 - 8), 4)

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
    def cut_effects_render (self, scene_surface, hero, scene):

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

            print_info = ((-4, -4, 'Orange'), (0, -4, 'Orange'), (4, -4, 'Orange'), (-4, 0, 'Orange'), (4, 0, 'Orange'), (-4, 4, 'Orange'), (0, 4, 'Orange'), (4, 4, 'Red'), (0, 0, 'Yellow'))
            for record in print_info:
                message = self.chapter_font.render(self.chapter_info[0], False, record[2])
                scene_surface.blit(message, (400 + record[0], 300 + record[1]))
            if self.timer:
                self.chapter_timer += 1


    # рендер мини - игр
    def mini_game_render (self, scene_surface, hero, scene):

        if self.barista != None:
            self.barista.render(scene_surface, hero, scene)


    @time_counter()
    def after_effects (self, scene_surface):

        # размытие
        blurring_surface = pygame.Surface((1024, 768))
        blurring_surface.blit(scene_surface, (-2, 0))
        blurring_surface.blit(scene_surface, (2, 0))
        blurring_surface.blit(scene_surface, (0, 2))
        blurring_surface.blit(scene_surface, (0, -2))
        blurring_surface.set_alpha(50)
        scene_surface.blit(blurring_surface, (0, 0))

        # пикcельное мерцание (шумы)
        if self.doting_stage == 0:
            self.dots = pygame.Surface((1024, 768), pygame.SRCALPHA)
            a = 300
        elif self.doting_stage in (1, 2, 3):
            a = 450
        for dot in range(a):
            x = randint(0, 1023)
            y = randint(0, 767)
            current_color = scene_surface.get_at((x, y))
            new_color = (
                max(0, min(255, current_color.r + randint(-20, 20))),
                max(0, min(255, current_color.g + randint(-20, 20))),
                max(0, min(255, current_color.b + randint(-20, 20))))
            pygame.draw.circle(self.dots, (new_color[0], new_color[1], new_color[2]), (x, y), 1)
        if self.doting_stage < 3:
            self.doting_stage += 1
        else:
            self.dots_surface = self.dots
            self.doting_stage = 0
        scene_surface.blit(self.dots_surface, (0, 0))

        # глитч смещения части экрана
        if randint(0, 50) == 0:
            area_to_shift = pygame.Rect(0, randint(0, 748), 1024, randint(4, 14))
            shifted_surface = scene_surface.subsurface(area_to_shift).copy()
            shifted_position = area_to_shift.move(4, 0)
            scene_surface.fill((0, 0, 0), area_to_shift)
            scene_surface.blit(shifted_surface, shifted_position)

        # хроматические аберрации
        # копии изображения для трех каналов
        red_shifted = scene_surface.copy()
        green_shifted = scene_surface.copy()
        blue_shifted = scene_surface.copy()
        # наложение цветовых фильтров на изображение
        red_shifted.blit(self.red_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        green_shifted.blit(self.green_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        blue_shifted.blit(self.blue_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        # обратное складывание в одно изображение
        result_surface = pygame.Surface((1024, 768))
        result_surface.blit(red_shifted, (-1, 0), special_flags=pygame.BLEND_RGB_ADD)
        result_surface.blit(green_shifted, (1, 0), special_flags=pygame.BLEND_RGB_ADD)
        result_surface.blit(blue_shifted, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        # перенос на основную поверхность
        scene_surface.blit(result_surface, (0, 0))

        # полосы
        scene_surface.blit(self.lines_surface, (0, 0))


if __name__ == '__main__':
    pass