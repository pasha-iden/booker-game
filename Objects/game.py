import pygame

from random import randint

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
        self.shift_x = 0
        self.shift_y = 0
        self.scale_value = 1
        self.screen_mod = 1
        # print(pygame.display.list_modes())
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), flags=pygame.NOFRAME)  # базовое разрешение
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
        self.barista_game = False
        self.barista_direction = None
        self.barista_skill = 2
        self.barista_rules = (50, 4)
        self.barista_score = None
        self.barista_queue = None
        self.barista_list = None
        self.barista_preparing = None
        self.barista_done_animation = None
        self.barista_speach = None
        self.barista_machine = None
        self.barista_teatable = None
        self.barista_to_say = None
        self.barista_says = None
        self.barista_speach_timer = None
        self.barista_guest = None


    def menu_window(self, scene_surface, hero, scene):
        if not self.just_started and self.pushed_ESCAPE and not self.settings:
            self.pause = not self.pause
            self.pushed_ESCAPE = False
        game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=40)

        if self.settings:
            options = self.menu_settings
            if self.pushed_ESCAPE:
                self.settings = False
                self.pushed_ESCAPE = False
        else:
            options = self.menu_options

        for option in options:
            if option[2].collidepoint(pygame.mouse.get_pos()):
                menu_option = game_font.render(option[0], False, 'Red')
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
                menu_option = game_font.render(option[0], False, 'Yellow')
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
        if self.key_pushed:
            self.key_pushed = False
            self.keys_clear()

        for event in pygame.event.get():

            # таймеры
            if event.type == self.timer_1000:
                self.timer = True
            if event.type == self.timer_50:
                self.timer_005 = True
            if self.barista_list != None and self.barista_list != []:
                for i in range(len(self.barista_list)):
                    if event.type == self.barista_list[i][-2]:
                        if self.barista_list[i][-1] != None and self.barista_list[i][-1] != 'неудача':
                            self.barista_list[i][-1] += -1
            if self.barista_speach_timer != None:
                if event.type == self.barista_speach_timer[0]:
                    self.barista_speach_timer[1] += -1
            if self.barista_queue != None:
                for i in range(len(self.barista_queue)):
                    if event.type == self.barista_queue[i][2]:
                        self.barista_queue[i][3] += -1

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
                    elif event.key == pygame.K_TAB:
                        self.pushed_TAB = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.pushed_BACKSPACE = True
                    elif event.key == pygame.K_q:
                        self.pushed_q = True
                    elif event.key == pygame.K_w:
                        self.pushed_w = True
                    elif event.key == pygame.K_e:
                        self.pushed_e = True
                    elif event.key == pygame.K_r:
                        self.pushed_r = True
                    elif event.key == pygame.K_t:
                        self.pushed_t = True
                    elif event.key == pygame.K_y:
                        self.pushed_y = True
                    elif event.key == pygame.K_u:
                        self.pushed_u = True
                    elif event.key == pygame.K_i:
                        self.pushed_i = True
                    elif event.key == pygame.K_o:
                        self.pushed_o = True
                    elif event.key == pygame.K_p:
                        self.pushed_p = True
                    elif event.key == pygame.K_LEFTBRACKET:
                        self.pushed_LEFTBRACKET = True  # клавиша [ х
                    elif event.key == pygame.K_RIGHTBRACKET:
                        self.pushed_RIGHTBRACKET = True  # клавиша ] ъ
                    elif event.key == pygame.K_a:
                        self.pushed_a = True
                    elif event.key == pygame.K_s:
                        self.pushed_s = True
                    elif event.key == pygame.K_d:
                        self.pushed_d = True
                    elif event.key == pygame.K_f:
                        self.pushed_f = True
                    elif event.key == pygame.K_g:
                        self.pushed_g = True
                    elif event.key == pygame.K_h:
                        self.pushed_h = True
                    elif event.key == pygame.K_j:
                        self.pushed_j = True
                    elif event.key == pygame.K_k:
                        self.pushed_k = True
                    elif event.key == pygame.K_l:
                        self.pushed_l = True
                    elif event.key == pygame.K_SEMICOLON:
                        self.pushed_SEMICOLON = True  # клавиша ; ж
                    elif event.key == pygame.K_QUOTE:
                        self.pushed_QUOTE = True  # клавиша ' э
                    elif event.key == pygame.K_z:
                        self.pushed_z = True
                    elif event.key == pygame.K_x:
                        self.pushed_x = True
                    elif event.key == pygame.K_c:
                        self.pushed_c = True
                    elif event.key == pygame.K_v:
                        self.pushed_v = True
                    elif event.key == pygame.K_b:
                        self.pushed_b = True
                    elif event.key == pygame.K_n:
                        self.pushed_n = True
                    elif event.key == pygame.K_m:
                        self.pushed_m = True
                    elif event.key == pygame.K_COMMA or pygame.key.get_pressed().index(True) == 54:
                        self.pushed_COMMA = True
                    elif event.key == pygame.K_PERIOD or pygame.key.get_pressed().index(True) == 55:
                        self.pushed_PERIOD = True

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
                if len(message_lines[line]) + len(word) + 1 > 30 * (1 + is_replica) - is_replica * 10:
                    message_lines.append('')
                    line += 1
                    if tutorial == False:
                        lines_before_tutorial += 1
                elif len(message_lines[line]) != 0:
                    message_lines[line] += ' '
                message_lines[line] = message_lines[line] + word
        self.prepared_message = (message_lines, tutorial, lines_before_tutorial)


    def cut_scene (self, hero, scene, key):

        if scene.act_started == False:
            print(act[scene.act])
            if act[scene.act][0] == 'герой идет':
                hero.destination = Cut_interactive(act[scene.act][1], act[scene.act][2])
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
                scene.plot_characters[scene.room-1][i].destination = Cut_interactive(act[scene.act][2], act[scene.act][3])
                scene.plot_characters[scene.room-1][i].find_path_to_deal(scene.room_map, scene.plot_characters[scene.room-1][i].destination)
            elif act[scene.act][0] == 'ГОТОВКА КОФЕ':
                self.barista_game = True
                hero.x = 400
                hero.y = 300
                hero.hitbox = pygame.Rect(hero.x, hero.y, hero.width, hero.height)
                self.barista_direction = 'вниз'
                self.barista_list = []
                self.barista_preparing = []
                self.barista_done_animation = [[], [], []]
                self.barista_score = [0, 0, None]
                self.barista_queue = None
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
                    self.prepared_message = None
                    scene.act = scene.act + 1
                    scene.act_started = False
            elif act[scene.act][0] == 'мысли героя':
                if self.pushed_SPACE:
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
            elif act[scene.act][0] == 'ГОТОВКА КОФЕ':
                if self.pushed_TAB or self.barista_score[2] == True:
                    self.barista_game = False
                    self.barista_direction = None
                    self.barista_list = None
                    self.barista_preparing = None
                    self.barista_done_animation = None
                    self.barista_score = None
                    self.barista_queue = None
                    scene.act = scene.act + 1
                    scene.act_started = False


    def barista_work (self, hero, scene):

        # передвижение между точками бара
        self.s_barista_walk(hero, scene)
        # инициация под-игр
        self.s_barista_initiation(hero)
        # добавление гостя в очередь
        self.s_barista_queue_add(scene)
        print (self.barista_queue)
        # игра: диалог с гостем
        self.s_barista_speach()
        # игра: готовка ингредиентов
        self.s_barista_slots()
        # неудача, если время готовки вышло
        self.s_barista_cooking_time_lose()
        # учет готовых ингредиентов и напитков
        self.s_barista_cooking()
        # менеджмент удаления напитков из списков
        self.s_barista_dishes_management()
        # победа или поражение
        self.s_barista_result()

    def s_barista_walk (self, hero, scene):
        if hero.path_to_deal != []:
            hero.walk()
        else:
            hero.direction = self.barista_direction
        if not self.barista_speach and not self.barista_machine and not self.barista_teatable:
            if self.pushed_w:
                hero.destination = Cut_interactive(420, 172)
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.barista_direction = 'вверх'
            elif self.pushed_a:
                hero.destination = Cut_interactive(360, 364)
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.barista_teatable = True
                self.barista_direction = 'влево'
            elif self.pushed_d:
                hero.destination = Cut_interactive(400, 412)
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.barista_machine = True
                self.barista_direction = 'вправо'
            elif self.pushed_s:
                hero.destination = Cut_interactive(392, 436)
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.barista_speach = True
                self.barista_direction = 'вниз'
            self.pushed_w = False
            self.pushed_a = False
            self.pushed_s = False
            self.pushed_d = False
    def s_barista_initiation (self, hero):
        if hero.x == 392 and hero.y == 436 and self.pushed_SPACE and not self.barista_speach:
            self.pushed_SPACE = False
            self.barista_speach = True
        elif hero.x == 400 and hero.y == 412 and self.pushed_SPACE and not self.barista_machine:
            self.pushed_SPACE = False
            self.barista_machine = True
        elif hero.x == 360 and hero.y == 364 and self.pushed_SPACE and not self.barista_teatable:
            self.pushed_SPACE = False
            self.barista_teatable = True
    def s_barista_queue_add (self, scene):
        if self.barista_queue == None:
            scene.placing_plot_characters((1, 'очередь', 400, 568))
            self.barista_queue = []
            self.barista_queue.append([scene.plot_characters[scene.room-1][-1], len(self.barista_queue), pygame.USEREVENT + 10 + len(self.barista_queue), 10, None])
            pygame.time.set_timer(self.barista_queue[0][2], 1000)
    def s_barista_speach (self):
        if self.barista_speach:
            # определение, что нужно сказать
            if self.barista_to_say == None:
                to_say = ('Здравствуйте', 'Привет', 'Добрый день', 'Рады вас видеть')
                self.barista_to_say = to_say[randint(0, len(to_say) - 1)]
                self.barista_says = ''

            # взведение таймера разговора
            if self.barista_speach_timer == None:
                self.barista_speach_timer = [pygame.USEREVENT + 20, 10]
                pygame.time.set_timer(self.barista_speach_timer[0], 1000)

            # неудача, если таймер вышел
            if self.barista_speach_timer[1] == 0:
                self.barista_score[1] += 1
                self.barista_says = None
                self.barista_to_say = None
                self.barista_speach_timer = None
                self.barista_speach = False

            # завершение диалога с гостем, если фраза введена правильно
            elif self.barista_to_say == self.barista_says:
                self.barista_says = None
                self.barista_to_say = None
                self.barista_speach_timer = None
                self.barista_speach = False

                # добавление напитков в заказ
                t = randint(1, 3)
                dishes = (('Эспрессо', 'Эс'), ('Американо', 'Эс', 'Ки'), ('Капучино', 'Эс', 'Мо'), ('Латте', 'Мо', 'Эс'), ('Раф', 'Эс', 'Сл'), ('Чай', 'Ча', 'Ки'), ('Фильтр', 'Фи'))
                self.barista_queue[0][-1] = []
                for i in range(t):
                    new_dish = dishes[randint(0, len(dishes) - 1)]
                    # добавление напитка в лист заказов
                    self.barista_list.append(list(new_dish))
                    self.barista_list[-1].append(pygame.USEREVENT + 21 + self.barista_score[0])
                    pygame.time.set_timer(self.barista_list[-1][-1], 1000)
                    self.barista_list[-1].append(10)
                    # добавление напитка в список готовящихся напитков
                    self.barista_preparing.append(list(new_dish[1: len(new_dish)]))
                    # добавление номера напитка в список напитков гостя
                    self.barista_queue[0][-1].append(len(self.barista_list)-1)

            # добавление буквы в высказывание героини
            else:
                l = ''
                if self.pushed_BACKSPACE:
                    if len(self.barista_says) < 2:
                        self.barista_says = ''
                    else:
                        self.barista_says = self.barista_says[0: len(self.barista_says) - 1]
                else:  # перечисление всех клавиш
                    if self.pushed_SPACE:
                        l = ' '
                    elif self.pushed_q:
                        l = 'й'
                    elif self.pushed_w:
                        l = 'ц'
                    elif self.pushed_e:
                        l = 'у'
                    elif self.pushed_r:
                        l = 'к'
                    elif self.pushed_t:
                        l = 'е'
                    elif self.pushed_y:
                        l = 'н'
                    elif self.pushed_u:
                        l = 'г'
                    elif self.pushed_i:
                        l = 'ш'
                    elif self.pushed_o:
                        l = 'щ'
                    elif self.pushed_p:
                        l = 'з'
                    elif self.pushed_LEFTBRACKET:
                        l = 'х'
                    elif self.pushed_RIGHTBRACKET:
                        l = 'ъ'
                    elif self.pushed_a:
                        l = 'ф'
                    elif self.pushed_s:
                        l = 'ы'
                    elif self.pushed_d:
                        l = 'в'
                    elif self.pushed_f:
                        l = 'а'
                    elif self.pushed_g:
                        l = 'п'
                    elif self.pushed_h:
                        l = 'р'
                    elif self.pushed_j:
                        l = 'о'
                    elif self.pushed_k:
                        l = 'л'
                    elif self.pushed_l:
                        l = 'д'
                    elif self.pushed_SEMICOLON:
                        l = 'ж'
                    elif self.pushed_QUOTE:
                        l = 'э'
                    elif self.pushed_z:
                        l = 'я'
                    elif self.pushed_x:
                        l = 'ч'
                    elif self.pushed_c:
                        l = 'с'
                    elif self.pushed_v:
                        l = 'м'
                    elif self.pushed_b:
                        l = 'и'
                    elif self.pushed_n:
                        l = 'т'
                    elif self.pushed_m:
                        l = 'ь'
                    elif self.pushed_COMMA:
                        l = 'б'
                    elif self.pushed_PERIOD:
                        l = 'ю'
                self.barista_says = self.barista_says + l
                # заглавная первая буква
                if len(self.barista_says) == 1:
                    self.barista_says = self.barista_says.capitalize() #
    def s_barista_slots(self):
        self.barista_cooking = None

        if self.barista_machine:
            if len(self.barista_list) == len(self.barista_done_animation[1]) or self.barista_list == [] or self.pushed_SPACE:
                self.barista_machine = False
            if self.pushed_w:
                self.barista_cooking = 'Эс'
            elif self.pushed_a:
                self.barista_cooking = 'Ки'
            elif self.pushed_d:
                self.barista_cooking = 'Мо'
            elif self.pushed_s:
                self.barista_cooking = 'Сл'

        if self.barista_teatable:
            if len(self.barista_list) == len(self.barista_done_animation[1]) or self.barista_list == [] or self.pushed_SPACE:
                self.barista_teatable = False
            if self.pushed_w:
                self.barista_cooking = 'Ча'
            elif self.pushed_a:
                self.barista_cooking = 'Си'
            elif self.pushed_d:
                self.barista_cooking = 'Са'
            elif self.pushed_s:
                self.barista_cooking = 'Фи'
    def s_barista_cooking_time_lose(self):
        # неудача, если время готовки вышло
        for i in range(len(self.barista_list)):
            if self.barista_list[i][-1] == 0:
                self.barista_score[1] += 1
                self.barista_list[i][-1] = 'неудача'
                for j in range(len(self.barista_queue)):
                    if i in self.barista_queue[j][-1]:
                        self.barista_queue[j][-1].pop(self.barista_queue[j][-1].index(i))
                for j in range(len(self.barista_preparing[i])):
                    self.barista_preparing[i][j] = None
                self.barista_done_animation[0].append(60)
                self.barista_done_animation[1].append(i)
                self.barista_done_animation[2].append(False)
    def s_barista_cooking(self):
        # сверка корректности добавляемого ингредиента
        if self.barista_cooking != None:
            i = 0
            while i < len(self.barista_preparing) and i < self.barista_skill + len(self.barista_done_animation[1]) and self.barista_cooking not in self.barista_preparing[i]:
                i += 1
            # добавление ингредиента, если он корректен и не превышает скилл
            if i < len(self.barista_preparing) and i < self.barista_skill + len(self.barista_done_animation[1]):
                self.barista_preparing[i][self.barista_preparing[i].index(self.barista_cooking)] = None
                # закрытие позиции, если заказ готов
                if self.barista_preparing[i].count(None) == len(self.barista_preparing[i]) and self.barista_list[i][-1] != 'неудача':
                    self.barista_score[0] += 1
                    for j in range(len(self.barista_queue)):
                        if i in self.barista_queue[j][-1]:
                            self.barista_queue[j][-1].pop(self.barista_queue[j][-1].index(i))
                    self.barista_list[i][-1] = None
                    self.barista_done_animation[0].append(60)
                    self.barista_done_animation[1].append(i)
                    self.barista_done_animation[2].append(True)
            else:
                self.barista_score[1] += 1
    def s_barista_guest_away(self):
        pass
        # !!!!!!!!!!!!!!! (если заказов нет)
    def s_barista_dishes_management(self):
        # удаление позиции из списка заказов
        if self.barista_done_animation != [[], [], []]:

            # после анимации неудачи
            if False in self.barista_done_animation[2]:
                i = 0
                while i <= len(self.barista_done_animation[1]) - 1:
                    if self.barista_done_animation[0][i] == 255 and self.barista_done_animation[2][i] == False:
                        for j in range(len(self.barista_done_animation[1])):
                            if self.barista_done_animation[1][j] > self.barista_done_animation[1][i]:
                                self.barista_done_animation[1][j] += -1
                        self.barista_list.pop(self.barista_done_animation[1][i])
                        self.barista_preparing.pop(self.barista_done_animation[1][i])
                        # цикл перенумерации заказов в списке заказов гостей
                        for j in range(len(self.barista_queue)):
                            for p in range(len(self.barista_queue[j][-1])):
                                if self.barista_queue[j][-1][p] > i:
                                    self.barista_queue[j][-1][p] += -1
                        self.barista_done_animation[0].pop(i) # как бы таймер анимации этой позиции
                        self.barista_done_animation[1].pop(i) # индекс этой позиции
                        self.barista_done_animation[2].pop(i) # причина анимации позиции (готово или время)
                    else:
                        i += 1

            # после анимации засчитывания
            i = 0
            done = False
            while i <= len(self.barista_done_animation[1]) - 1 and done == False:
                if self.barista_done_animation[0][i] == 255:
                    for j in range(len(self.barista_done_animation[1])):
                        if self.barista_done_animation[1][j] > self.barista_done_animation[1][i]:
                            self.barista_done_animation[1][j] += -1
                    self.barista_list.pop(self.barista_done_animation[1][i])
                    self.barista_preparing.pop(self.barista_done_animation[1][i])
                    # цикл перенумерации заказов в списке заказов гостей
                    for j in range(len(self.barista_queue)):
                        for p in range(len(self.barista_queue[j][-1])):
                            if self.barista_queue[j][-1][p] > i:
                                self.barista_queue[j][-1][p] += -1
                    self.barista_done_animation[0].pop(i)
                    self.barista_done_animation[1].pop(i)
                    self.barista_done_animation[2].pop(i)
                    done = True
                i += 1
            for i in range(len(self.barista_done_animation[0])):
                self.barista_done_animation[0][i] += 5
    def s_barista_result(self):
        if self.barista_score[0] >= self.barista_rules[0]:
            self.barista_score[2] = True
        elif self.barista_score[1] >= self.barista_rules[1]:
            self.barista_score[0] = 0
            self.barista_score[1] = 0


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
        if act[scene.act][0] == 'мысли героя' and self.prepared_message != None:
            x = hero.x + 33 - (len(max(self.prepared_message[0], key=len)) * 10) // 2
            y = hero.y - 85
            if scene.room == 1 or scene.room == 3:
                if x < 5: x = 5
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
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            l = 0
            for line in self.prepared_message[0]:
                if (self.prepared_message[1] == False) or (self.prepared_message[1] == True and l < self.prepared_message[2]):
                    message = game_font.render(line, False, 'Black')
                else:
                    message = game_font.render(line, False, (125, 125, 125))
                scene_surface.blit(message, (x, y - (len(self.prepared_message[0]) -l) * 20))
                l += 1

        # отрисовка реплик
        if (act[scene.act][0] == 'реплика' or act[scene.act][0] == 'реплика героя') and self.prepared_message != None :
            x = 220
            if scene.room == 1:
                y = 480
            else:
                y = 555
            w = 600

            # окно речи и имя персонажа
            pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, w, 200))
            pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, w, 200), 2)
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            message = game_font.render(act[scene.act][1], False, 'Black')
            scene_surface.blit(message, (x + (act[scene.act][0] == 'реплика') * 120, y))

            # портрет персонажа
            if act[scene.act][0] == 'реплика':
                for character in scene.plot_characters[scene.room-1]:
                    if character.name == act[scene.act][1]:
                        scene_surface.blit(character.head, (x + 10, y + 20))
            else:
                scene_surface.blit(hero.head, (x + w - 100 - 10, y + 20))

            # реплика
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            l = 0
            for line in self.prepared_message[0]:
                if (self.prepared_message[1] == False) or (self.prepared_message[1] == True and l < self.prepared_message[2]):
                    message = game_font.render(line, False, 'Black')
                else:
                    message = game_font.render(line, False, (125, 125, 125))
                scene_surface.blit(message, (x + (act[scene.act][0] == 'реплика') * 120, y + 30 + l * 20))
                l += 1

        # рамки сцен
        if scene.room == 1:
            pygame.draw.rect(scene_surface, 'Black', (0, 0, 1024, 92))
            pygame.draw.rect(scene_surface, 'Black', (0, 682, 1024, 86))
        if scene.room == 2:
            pygame.draw.rect(scene_surface, 'Black', (0, 0, 207, 768))
            pygame.draw.rect(scene_surface, 'Black', (847, 0, 177, 768))

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
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=60)
            print_info = ((-4, -4, 'Orange'), (0, -4, 'Orange'), (4, -4, 'Orange'), (-4, 0, 'Orange'), (4, 0, 'Orange'), (-4, 4, 'Orange'), (0, 4, 'Orange'), (4, 4, 'Red'), (0, 0, 'Yellow'))
            for record in print_info:
                message = game_font.render(self.chapter_info[0], False, record[2])
                scene_surface.blit(message, (400 + record[0], 300 + record[1]))
            if self.timer:
                self.chapter_timer += 1

        if self.barista_game:

            # счет игры
            x = 240
            y = 500
            h = 50
            pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 150, h))
            pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 150, h), 2)
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            message = game_font.render('Заказов:', False, 'Black')
            scene_surface.blit(message, (x, y + 10))
            message = game_font.render(str(self.barista_score[0]) + '/' + str(self.barista_rules[0]), False, 'Black')
            scene_surface.blit(message, (x + 100 - (len(str(self.barista_score[0])) - 1) * 10, y + 10))

            x = 450
            pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 150, h))
            pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 150, h), 2)
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            message = game_font.render('Ошибок:', False, 'Black')
            scene_surface.blit(message, (x, y + 10))
            message = game_font.render(str(self.barista_score[1]) + '/' + str(self.barista_rules[1]), False, 'Black')
            scene_surface.blit(message, (x + 100 - (len(str(self.barista_score[0])) - 1) * 10, y + 10))

            # интерфейс списка заказов
            if self.barista_list != []:

                x = 500
                y = 150
                h = 50
                # строка "Выполняемые заказы"
                pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 300, h))
                pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 300, h), 2)
                game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
                message = game_font.render('Выполняемые заказы:', False, 'Black')
                scene_surface.blit(message, (x, y + 10))
                # строка "Заказы в очереди"
                if self.barista_skill + len(self.barista_done_animation[1]) < len(self.barista_list):
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y + h * (self.barista_skill + len(self.barista_done_animation[1]) + 1), 300, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y + h * (self.barista_skill + len(self.barista_done_animation[1])  + 1), 300, h), 2)
                    game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
                    message = game_font.render('В очереди:', False, 'Black')
                    scene_surface.blit(message, (x, y + 10 + h * (self.barista_skill + len(self.barista_done_animation[1]) + 1)))

                # поля позиций в заказе
                for line in range(len(self.barista_list)):
                    rlc = h * (line + 1 + (self.barista_skill + len(self.barista_done_animation[1]) < line + 1)) # relative line coordinate

                    # отображение фона полей заказов, если это не выполненный заказ
                    if self.barista_done_animation == [[], [], []] or line not in self.barista_done_animation[1]:
                        pygame.draw.rect(scene_surface, 'Gray', (x - 4, y + rlc, 300, h))

                    # отображение фона поля заказа, если заказ выполнен
                    elif self.barista_done_animation != [[], [], []] and line in self.barista_done_animation[1] and self.barista_done_animation[2][self.barista_done_animation[1].index(line)] == True:
                        ind = self.barista_done_animation[1].index(line)
                        pygame.draw.rect(scene_surface, (self.barista_done_animation[0][ind], self.barista_done_animation[0][ind], self.barista_done_animation[0][ind]), (x - 4, y + rlc, 300, h))

                    # отображение фона поля заказа, если таймер вышел
                    elif self.barista_done_animation != [[], [], []] and line in self.barista_done_animation[1] and self.barista_done_animation[2][self.barista_done_animation[1].index(line)] == False:
                        ind = self.barista_done_animation[1].index(line)
                        pygame.draw.rect(scene_surface, (255, self.barista_done_animation[0][ind], self.barista_done_animation[0][ind]), (x - 4, y + rlc, 300, h))

                    # названия заказа и его таймеры
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y + rlc, 300, h), 2)
                    game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
                    message = game_font.render(self.barista_list[line][0], False, 'Black')
                    scene_surface.blit(message, (x, y + 10 + rlc))
                    if self.barista_list[line][-1] != None and self.barista_list[line][-1] != 'неудача':
                        message = game_font.render(str(self.barista_list[line][-1]), False, 'Black')
                        scene_surface.blit(message, (x + 270 - self.barista_list[line][-1]//10 * 11, y + 10 + rlc))

                    # перечисление ингредиентов
                    for i in range(1, len(self.barista_list[line]) -2):
                        # отображение засчитанного ингредиента темной иконкой
                        if self.barista_preparing[line][i-1] == None:
                            pygame.draw.rect(scene_surface, (100, 100, 100), (x + 100 - 4 + h * (i-1), y + rlc, h, h))
                        # отображение остальных иконок
                        pygame.draw.rect(scene_surface, (80, 80, 80), (x + 100 - 4 + h * (i-1), y + rlc, h, h), 2)
                        game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
                        message = game_font.render(self.barista_list[line][i], False, 'Black')
                        scene_surface.blit(message, (x + 100 + 5 + h * (i-1), y + 10 + rlc))

            # окно диалога с гостем
            if self.barista_speach:
                x = 220 # 200
                y = 150
                w = 400 # 600
                h = 150
                pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, w, h))
                pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, w, h), 2)
                game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
                message = game_font.render('Гость', False, 'Black')
                scene_surface.blit(message, (x, y))
                message = game_font.render('Здравствуйте', False, 'Black')
                scene_surface.blit(message, (x, y + 25))
                message = game_font.render(str(self.barista_speach_timer[1]), False, 'Black')
                scene_surface.blit(message, (x + 370 - self.barista_speach_timer[1] //10 * 11, y + 25))
                message = game_font.render('Полина', False, 'Black')
                scene_surface.blit(message, (x + w - 80 , y + 50))
                message = game_font.render(self.barista_says, False, 'Black')
                scene_surface.blit(message, (x + w - 20 - len(self.barista_says) * 10, y + 75))
                message = game_font.render(self.barista_to_say, False, (80, 80, 80))
                scene_surface.blit(message, (x + w - 20 - len(self.barista_to_say) * 10, y + 100))

            # интерфейс опций кофе-машины
            if self.barista_machine:
                x = 500
                y = 377
                w = 43
                print_info = ((x, y, 'Эс'), (x, y + w * 2, 'Сл'), (x - w, y + w, 'Ки'), (x + w, y + w, 'Мо'))
                for record in print_info:
                    pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                    game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
                    message = game_font.render(record[2], False, 'Black')
                    scene_surface.blit(message, (record[0] + 5, record[1] + 5))

            # интерфейс опций чайного столика
            if self.barista_teatable:
                x = 280
                y = 327
                w = 43
                print_info = ((x, y, 'Ча'), (x, y + w * 2, 'Фи'), (x - w, y + w, 'Си'), (x + w, y + w, 'Са'))
                for record in print_info:
                    pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                    game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
                    message = game_font.render(record[2], False, 'Black')
                    scene_surface.blit(message, (record[0] + 5, record[1] + 5))


    def frames_render (self, final_surface, scene):
        if self.screen_mod == 2:
            if not self.pause:
                if scene.room == 1:
                    pygame.draw.rect(final_surface, (80, 80, 80), (0, 84, 1024, 606), 4)
                    pygame.draw.rect(final_surface, 'Gray', (0 + 4, 84 + 4, 1024 - 8, 606 - 8), 4)

                if scene.room == 2:
                    pygame.draw.rect(final_surface, (80, 80, 80), (206, 0, 644, 768), 4)
                    pygame.draw.rect(final_surface, 'Gray', (206 + 4, 0 + 4, 644 - 8, 768 - 8), 4)

                if scene.room == 3:
                    pygame.draw.rect(final_surface, (80, 80, 80), (0, 0, 1024, 768), 4)
                    pygame.draw.rect(final_surface, 'Gray', (0 + 4, 0 + 4, 1024 - 8, 768 - 8), 4)


if __name__ == '__main__':
    pass