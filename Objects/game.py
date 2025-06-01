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
        self.key_pushed = False
        self.keys_clear()

        # технические состояния
        self.fade_animation = None
        self.wow_fade_animation = None
        self.chapter_info = None
        self.chapter_timer = None
        self.wait = None

        # переменные для игры бариста
        self.barista_game = False
        self.barista_direction = None
        self.barista_speach = None
        self.barista_to_say = None
        self.barista_says = None
        self.barista_guest = None


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
                        save_data = str(hero.x) + '\n' + str(hero.y) + '\n' + str(scene.room) + '\n' + str(scene.act)
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
                        scene.act = int(save_data[3])
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


    def keys_clear(self):
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

        if self.key_pushed:
            self.key_pushed = False
            self.keys_clear()

        for event in pygame.event.get():

            if event.type == self.timer_1000:
                self.timer = True

            if event.type == self.timer_50:
                self.timer_005 = True

            if event.type == pygame.KEYDOWN:
                self.key_pushed = True

                if event.key == pygame.K_ESCAPE and not self.just_started:
                    self.pause = not self.pause
                # перечисление всех клавиш
                else:
                    if event.key == pygame.K_SPACE and not self.pause:
                        self.pushed_SPACE = True
                    elif event.key == pygame.K_BACKSPACE and not self.pause:
                        self.pushed_BACKSPACE = True
                    elif event.key == pygame.K_q and not self.pause:
                        self.pushed_q = True
                    elif event.key == pygame.K_w and not self.pause:
                        self.pushed_w = True
                    elif event.key == pygame.K_e and not self.pause:
                        self.pushed_e = True
                    elif event.key == pygame.K_r and not self.pause:
                        self.pushed_r = True
                    elif event.key == pygame.K_t and not self.pause:
                        self.pushed_t = True
                    elif event.key == pygame.K_y and not self.pause:
                        self.pushed_y = True
                    elif event.key == pygame.K_u and not self.pause:
                        self.pushed_u = True
                    elif event.key == pygame.K_i and not self.pause:
                        self.pushed_i = True
                    elif event.key == pygame.K_o and not self.pause:
                        self.pushed_o = True
                    elif event.key == pygame.K_p and not self.pause:
                        self.pushed_p = True
                    elif event.key == pygame.K_LEFTBRACKET and not self.pause:
                        self.pushed_LEFTBRACKET = True  # клавиша [ х
                    elif event.key == pygame.K_RIGHTBRACKET and not self.pause:
                        self.pushed_RIGHTBRACKET = True  # клавиша ] ъ
                    elif event.key == pygame.K_a and not self.pause:
                        self.pushed_a = True
                    elif event.key == pygame.K_s and not self.pause:
                        self.pushed_s = True
                    elif event.key == pygame.K_d and not self.pause:
                        self.pushed_d = True
                    elif event.key == pygame.K_f and not self.pause:
                        self.pushed_f = True
                    elif event.key == pygame.K_g and not self.pause:
                        self.pushed_g = True
                    elif event.key == pygame.K_h and not self.pause:
                        self.pushed_h = True
                    elif event.key == pygame.K_j and not self.pause:
                        self.pushed_j = True
                    elif event.key == pygame.K_k and not self.pause:
                        self.pushed_k = True
                    elif event.key == pygame.K_l and not self.pause:
                        self.pushed_l = True
                    elif event.key == pygame.K_SEMICOLON and not self.pause:
                        self.pushed_SEMICOLON = True  # клавиша ; ж
                    elif event.key == pygame.K_QUOTE and not self.pause:
                        self.pushed_QUOTE = True  # клавиша ' э
                    elif event.key == pygame.K_z and not self.pause:
                        self.pushed_z = True
                    elif event.key == pygame.K_x and not self.pause:
                        self.pushed_x = True
                    elif event.key == pygame.K_c and not self.pause:
                        self.pushed_c = True
                    elif event.key == pygame.K_v and not self.pause:
                        self.pushed_v = True
                    elif event.key == pygame.K_b and not self.pause:
                        self.pushed_b = True
                    elif event.key == pygame.K_n and not self.pause:
                        self.pushed_n = True
                    elif event.key == pygame.K_m and not self.pause:
                        self.pushed_m = True
                    elif event.key == pygame.K_COMMA and not self.pause:
                        self.pushed_COMMA = True
                    elif event.key == pygame.K_PERIOD and not self.pause:
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
            elif act[scene.act][0] == 'ГОТОВКА КОФЕ':
                self.barista_game = True
                hero.x = 400
                hero.y = 300
                hero.hitbox = pygame.Rect(hero.x, hero.y, hero.width, hero.height)
                self.barista_direction = 'вниз'
                self.barista_says = ''
                self.barista_to_say = ''
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
            elif act[scene.act][0] == 'ГОТОВКА КОФЕ':
                if key[pygame.K_r]:
                    self.barista_game = False
                    self.barista_direction = None
                    self.barista_says = None
                    self.barista_to_say = None
                    scene.act = scene.act + 1
                    scene.act_started = False


    def barista_work (self, scene_surface, hero, scene):
        if hero.path_to_deal != []:
            hero.walk()
        else:
            hero.direction = self.barista_direction
        if not self.barista_speach:
            if self.pushed_w:
                hero.destination = Cut_interactive(420, 172)
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.barista_direction = 'вверх'
            elif self.pushed_a:
                hero.destination = Cut_interactive(360, 364)
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.barista_direction = 'влево'
            elif self.pushed_d:
                hero.destination = Cut_interactive(400, 412)
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.barista_direction = 'вправо'
            elif self.pushed_s:
                hero.destination = Cut_interactive(392, 436)
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.barista_direction = 'вниз'

        if hero.x == 392 and hero.y == 436 and self.pushed_SPACE:
            self.pushed_SPACE = False
            self.barista_speach = True

        if self.barista_speach:
            self.barista_to_say = 'Здравствуйте'
            if self.barista_to_say == self.barista_says:
                self.barista_says = ''
                self.barista_speach = False
            else:
                l = ''
                if self.pushed_BACKSPACE:
                    if len(self.barista_says) < 2:
                        self.barista_says = ''
                    else:
                        self.barista_says = self.barista_says[0: len(self.barista_says) - 1]
                # перечисление всех клавиш
                else:
                    if self.pushed_SPACE:
                        l = l + ' '
                    elif self.pushed_q:
                        l = l + 'й'
                    elif self.pushed_w:
                        l = l + 'ц'
                    elif self.pushed_e:
                        l = l + 'у'
                    elif self.pushed_r:
                        l = l + 'к'
                    elif self.pushed_t:
                        l = l + 'е'
                    elif self.pushed_y:
                        l = l + 'н'
                    elif self.pushed_u:
                        l = l + 'г'
                    elif self.pushed_i:
                        l = l + 'ш'
                    elif self.pushed_o:
                        l = l + 'щ'
                    elif self.pushed_p:
                        l = l + 'з'
                    elif self.pushed_LEFTBRACKET:
                        l = l + 'х'
                    elif self.pushed_RIGHTBRACKET:
                        l = l + 'ъ'
                    elif self.pushed_a:
                        l = l + 'ф'
                    elif self.pushed_s:
                        l = l + 'ы'
                    elif self.pushed_d:
                        l = l + 'в'
                    elif self.pushed_f:
                        l = l + 'а'
                    elif self.pushed_g:
                        l = l + 'п'
                    elif self.pushed_h:
                        l = l + 'р'
                    elif self.pushed_j:
                        l = l + 'о'
                    elif self.pushed_k:
                        l = l + 'л'
                    elif self.pushed_l:
                        l = l + 'д'
                    elif self.pushed_SEMICOLON:
                        l = l + 'ж'
                    elif self.pushed_QUOTE:
                        l = l + 'э'
                    elif self.pushed_z:
                        l = l + 'я'
                    elif self.pushed_x:
                        l = l + 'ч'
                    elif self.pushed_c:
                        l = l + 'с'
                    elif self.pushed_v:
                        l = l + 'м'
                    elif self.pushed_b:
                        l = l + 'и'
                    elif self.pushed_n:
                        l = l + 'т'
                    elif self.pushed_m:
                        l = l + 'ь'
                    elif self.pushed_COMMA:
                        l = l + 'б'
                    elif self.pushed_PERIOD:
                        l = l + 'ю'
                self.barista_says = self.barista_says + l
                if len(self.barista_says) == 1:
                    self.barista_says = self.barista_says.capitalize()


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

        if self.barista_speach:
            pygame.draw.rect(scene_surface, 'Gray', (200 - 4, 150, 600, 200))
            pygame.draw.rect(scene_surface, (80, 80, 80), (200 - 4, 150, 600, 200), 2)
            game_font = pygame.font.Font('Files/Fonts/Font.ttf', size=20)
            message = game_font.render('Гость', False, 'Black')
            scene_surface.blit(message, (200, 150))
            message = game_font.render('Здравствуйте', False, 'Black')
            scene_surface.blit(message, (200, 175))
            message = game_font.render('Полина', False, 'Black')
            scene_surface.blit(message, (700, 200))
            message = game_font.render(self.barista_says, False, 'Black')
            scene_surface.blit(message, (760 - len(self.barista_says) * 10, 225))
            message = game_font.render(self.barista_to_say, False, (80, 80, 80))
            scene_surface.blit(message, (760 - len(self.barista_to_say) * 10, 250))

if __name__ == '__main__':
    pass