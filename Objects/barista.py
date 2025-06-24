import pygame

from random import randint

from Objects.interactives import Cut_interactive

from Objects.acts import act


class Barista:
    def __init__(self, game, order_time = None, cook_time = None):
        self.game = game
        self.letter = None
        self.start_timer = [pygame.USEREVENT + 3, 3]
        pygame.time.set_timer(self.start_timer[0], 1000)
        self.skill = 1
        self.rules = (20, 4)
        self.cook_time = cook_time
        self.order_time = order_time
        self.guests = 0
        self.score = [0, 0, None]
        self.queue = []
        self.queue_wait = []
        self.queue_away = []
        self.list = []
        self.preparing = []
        self.done_animation = [[], [], []]
        self.speach = False
        self.machine = False
        self.teatable = False
        self.to_say = None
        self.says = None
        self.speach_timer = None

        # переменные для обучения игре бариста
        self.counted_cook_time = None
        self.counted_order_time = None
        self.message_preparing = None
        self.return_times = None
        
        # технические переменные
        self.game_font = pygame.font.Font('Files/Fonts/Roboto_Condensed-Medium.ttf', size=20)
        self.count_font = pygame.font.Font('Files/Fonts/Roboto_Condensed-Medium.ttf', size=40)

    def logica(self, hero, scene, letter, timer):

        self.letter = letter
        if self.game:
            if self.start_timer != None and self.start_timer[1] == -1:
                self.start_timer = None
            if self.score[0] >= self.rules[0] or self.score[1] >= self.rules[1]:
                self.score[2] = False
            if self.start_timer == None and self.score[2] != False:

                # передвижение между точками бара
                self.walk(hero, scene)
                # инициация под-игр
                self.initiation(hero)
                # добавление гостя в очередь
                self.queue_add(scene, timer)
                # игра: диалог с гостем
                self.talk(scene, timer)
                # игра: готовка ингредиентов
                self.slots()
                # неудача, если время готовки вышло
                self.cooking_time_lose()
                # учет готовых ингредиентов и напитков
                self.cooking()
                # менеджмент удаления напитков из списков
                self.dishes_management()
                # передвижение ожидающих гостей
                self.wait_guests_walk(scene)
                # уход гостей
                self.away_guests_walk(scene)

            # победа или поражение
            else:
                self.result(hero, scene)
        else:
            self.tutorial(hero, scene)


    # Методы логики
    # region
    def walk(self, hero, scene):
        if hero.path_to_deal != []:
            hero.walk()
        if not self.speach and not self.machine and not self.teatable:
            # if self.letter == 'ц':
            #     hero.destination = Cut_interactive((420, 172, вверх))
            #     hero.find_path_to_deal(scene.room_map, hero.destination)
            if self.letter == 'ф':
                hero.destination = Cut_interactive((360, 364, 'влево'))
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.teatable = True
            elif self.letter == 'в':
                hero.destination = Cut_interactive((400, 412, 'вправо'))
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.machine = True
            elif self.letter == 'ы':
                hero.destination = Cut_interactive((392, 436, 'вниз'))
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.speach = True
            self.letter = None


    def initiation(self, hero):
        if hero.x == 392 and hero.y == 436 and self.letter == ' ' and not self.speach:
            self.letter = None
            self.speach = True
        elif hero.x == 400 and hero.y == 412 and self.letter == ' ' and not self.machine:
            self.letter = None
            self.machine = True
        elif hero.x == 360 and hero.y == 364 and self.letter == ' ' and not self.teatable:
            self.letter = None
            self.teatable = True


    # таймер на прием заказа у человека в очереди задается здесь
    def queue_add(self, scene, timer):
        if (self.queue == [] or (timer and randint(1, 2) == 1)) and len(self.queue) < 4:
            self.guests += 1
            places = ((392, 568, 'вверх'), (444, 580, 'вверх-влево'), (500, 560, 'вниз-влево'), (540, 600, 'влево'))
            scene.placing_plot_characters((1, 'очередь ' + str(self.guests), places[len(self.queue)][0], places[len(self.queue)][1], places[len(self.queue)][2] ))
            self.queue.append([scene.plot_characters[scene.room - 1][-1].name, pygame.USEREVENT + 5 + self.guests - self.guests // 5 * 5, self.cook_time + 1, [None]])
            pygame.time.set_timer(self.queue[-1][1], 1000)


    # таймеры на заказ и разговор задаются здесь
    def talk(self, scene, timer):
        if self.speach:
            current_guest = 0
            while current_guest < len(self.queue) and self.queue[current_guest][-1] != [None]:
                current_guest += 1
            if current_guest < len(self.queue):
                # определение, что нужно сказать
                if self.to_say == None:
                    to_say = ('Здравствуйте', 'Привет', 'Добрый день', 'Рады вас видеть')
                    self.to_say = to_say[randint(0, len(to_say) - 1)]
                    self.says = ''

                # взведение таймера разговора
                if self.speach_timer == None:
                    self.speach_timer = [pygame.USEREVENT + 3, self.order_time]
                    pygame.time.set_timer(self.speach_timer[0], 1000)

                # неудача, если таймер вышел
                if self.speach_timer[1] == 0:
                    self.score[1] += 1
                    self.says = None
                    self.to_say = None
                    self.speach_timer = None
                    self.speach = False
                    self.queue_away.append(self.queue[current_guest])
                    self.queue.pop(current_guest)

                # завершение диалога с гостем, если фраза введена правильно
                elif self.to_say == self.says:
                    self.says = None
                    self.to_say = None
                    self.speach_timer = None
                    self.speach = False

                    # добавление напитков в заказ
                    t = randint(1, 3)
                    dishes = (('Эспрессо', 'Эс'), ('Американо', 'Эс', 'Ки'), ('Капучино', 'Эс', 'Мо'), ('Латте', 'Мо', 'Эс'), ('Раф', 'Эс', 'Сл'), ('Чай', 'Ча', 'Ки'), ('Какао', 'Ка', 'Мо'), ('Фильтр', 'Фи'))
                    for i in range(t):
                        new_dish = dishes[randint(0, len(dishes) - 1)]
                        # добавление напитка в лист заказов
                        self.list.append(list(new_dish))
                        self.list[-1].append(pygame.USEREVENT + 11 + self.score[0] - self.score[0] // 15 * 15)
                        pygame.time.set_timer(self.list[-1][-1], 1000)
                        self.list[-1].append(self.cook_time)
                        # добавление напитка в список готовящихся напитков
                        self.preparing.append(list(new_dish[1: len(new_dish)]))
                        # добавление номера напитка в список напитков гостя
                        if self.queue[current_guest][-1] == [None]:
                            self.queue[current_guest][-1] = []
                        self.queue[current_guest][-1].append(len(self.list) - 1)
                    self.queue_wait.append(self.queue[current_guest])
                    self.queue.pop(current_guest)
                    if self.queue == []:
                        self.queue_add(scene, timer)

                # добавление буквы в высказывание героини
                else:
                    self.lettering()
            else:
                self.speach = False


    def lettering(self):
        if self.letter != None:
            if self.letter == 'backspace':
                if len(self.says) < 2:
                    self.says = ''
                else:
                    self.says = self.says[0: len(self.says) - 1]
            else:
                self.says = self.says + self.letter
                # заглавная первая буква
                if len(self.says) == 1:
                    self.says = self.says.capitalize()
                if self.says == ' ':
                    self.says = ''


    def slots(self):
        self.ingredient = None

        if self.machine:
            if len(self.list) == len(self.done_animation[1]) or self.list == [] or self.letter == ' ':
                self.machine = False
            if self.letter == 'ц':
                self.ingredient = 'Эс'
            elif self.letter == 'ф':
                self.ingredient = 'Ки'
            elif self.letter == 'в':
                self.ingredient = 'Мо'
            elif self.letter == 'ы':
                self.ingredient = 'Сл'

        if self.teatable:
            if len(self.list) == len(self.done_animation[1]) or self.list == [] or self.letter == ' ':
                self.teatable = False
            if self.letter == 'ц':
                self.ingredient = 'Ча'
            elif self.letter == 'ф':
                self.ingredient = 'Ка'
            elif self.letter == 'в':
                self.ingredient = 'Си'
            elif self.letter == 'ы':
                self.ingredient = 'Фи'


    def cooking_time_lose(self):
        # неудача, если время готовки вышло
        for i in range(len(self.list)):
            if self.list[i][-1] == 0:
                self.score[1] += 1
                self.list[i][-1] = 'неудача'
                for j in range(len(self.queue_wait)):
                    if i in self.queue_wait[j][-1]:
                        self.queue_wait[j][-1].pop(self.queue_wait[j][-1].index(i))
                for j in range(len(self.preparing[i])):
                    self.preparing[i][j] = None
                self.done_animation[0].append(60)
                self.done_animation[1].append(i)
                self.done_animation[2].append(False)


    def cooking(self):
        # сверка корректности добавляемого ингредиента
        if self.ingredient != None:
            i = 0
            while i < len(self.preparing) and i < self.skill + len(self.done_animation[1]) and self.ingredient not in self.preparing[i]:
                i += 1
            # добавление ингредиента, если он корректен и не превышает скилл
            if i < len(self.preparing) and i < self.skill + len(self.done_animation[1]):
                self.preparing[i][self.preparing[i].index(self.ingredient)] = None
                # закрытие позиции, если заказ готов
                if self.preparing[i].count(None) == len(self.preparing[i]) and self.list[i][-1] != 'неудача':
                    self.score[0] += 1
                    for j in range(len(self.queue_wait)):
                        if i in self.queue_wait[j][-1]:
                            self.queue_wait[j][-1].pop(self.queue_wait[j][-1].index(i))
                    self.list[i][-1] = None
                    self.done_animation[0].append(60)
                    self.done_animation[1].append(i)
                    self.done_animation[2].append(True)
            else:
                self.score[1] += 1


    def wait_guests_walk(self, scene):
        # передвижение людей в очереди на кассу
        places = ((392, 568, 'вверх'), (444, 580, 'вверх-влево'), (500, 560, 'вниз-влево'), (540, 600, 'влево'))
        for i in range(len(self.queue)):
            for j in range(len(scene.plot_characters[scene.room - 1])):
                if scene.plot_characters[scene.room - 1][j].name == self.queue[i][0]:
                    if scene.plot_characters[scene.room - 1][j].x != places[i][0] and scene.plot_characters[scene.room - 1][j].y != places[i][1] and scene.plot_characters[scene.room - 1][j].path_to_deal == []:
                        scene.plot_characters[scene.room - 1][j].destination = Cut_interactive(places[i])
                        scene.plot_characters[scene.room - 1][j].find_path_to_deal(scene.room_map, scene.plot_characters[scene.room - 1][j].destination)
                    elif scene.plot_characters[scene.room - 1][j].path_to_deal != []:
                        scene.plot_characters[scene.room - 1][j].walk()

        # передвижение людей в очереди за заказом
        places = ((576, 540, 'вниз'), (560, 512, 'вниз-вправо'), (588, 488, 'вниз-влево'), (568, 472, 'влево'))
        for i in range(len(self.queue_wait)):
            for j in range(len(scene.plot_characters[scene.room - 1])):
                if scene.plot_characters[scene.room - 1][j].name == self.queue_wait[i][0]:
                    if scene.plot_characters[scene.room - 1][j].x != places[i][0] and scene.plot_characters[scene.room - 1][j].y != places[i][1] and scene.plot_characters[scene.room - 1][j].path_to_deal == []:
                        scene.plot_characters[scene.room - 1][j].destination = Cut_interactive(places[i])
                        scene.plot_characters[scene.room - 1][j].find_path_to_deal(scene.room_map, scene.plot_characters[scene.room - 1][j].destination)
                    elif scene.plot_characters[scene.room - 1][j].path_to_deal != []:
                        scene.plot_characters[scene.room - 1][j].walk()


    def away_guests_walk(self, scene):

        # если гость не дождался приема заказа
        if self.queue[0][2] == 0:
            self.queue_away.append(self.queue[0])
            self.queue.pop(0)
            self.score[1] += 1

        i = 0
        # определение гостей, которые уже ничего не ждут (с выполненным или просроченным заказом)
        while i < len(self.queue_wait):
            while i < len(self.queue_wait) and self.queue_wait[i][-1] != []:
                i += 1
            # если он есть
            if i < len(self.queue_wait):
                # передача индекса сюжетного персонажа из очереди на_заказ/ожидающих в очередь уходящих
                self.queue_away.append(self.queue_wait[i])
                self.queue_wait.pop(i)
        # если очередь уходящих гостей не пустая
        if self.queue_away != []:
            places = (444, 628, 'вниз')
            for i in range(len(self.queue_away)):
                for j in range(len(scene.plot_characters[scene.room - 1])):
                    if scene.plot_characters[scene.room - 1][j].name == self.queue_away[i][0]:
                        if scene.plot_characters[scene.room - 1][j].x != places[0] and scene.plot_characters[scene.room - 1][j].y != places[1] and scene.plot_characters[scene.room - 1][j].path_to_deal == []:
                            scene.plot_characters[scene.room - 1][j].destination = Cut_interactive(places)
                            scene.plot_characters[scene.room - 1][j].find_path_to_deal(scene.room_map, scene.plot_characters[scene.room - 1][j].destination)
                        elif scene.plot_characters[scene.room - 1][j].x != places[0] and scene.plot_characters[scene.room - 1][j].y != places[1] and scene.plot_characters[scene.room - 1][j].path_to_deal != []:
                            scene.plot_characters[scene.room - 1][j].walk()

            # перебор всех уходящих гостей
            k = 0
            while k < len(self.queue_away):
                deleted = False
                # удаление гостя из списка персонажей сцены по индексу, хранящемуся в очереди уходящих гостей
                i = 0
                while i < len(scene.plot_characters[scene.room - 1]) and not deleted:
                    if scene.plot_characters[scene.room - 1][i].x == places[0] and scene.plot_characters[scene.room - 1][i].y == places[1]:
                        scene.plot_characters[scene.room - 1].pop(i)
                        self.queue_away.pop(k)
                        deleted = True
                    i += 1
                if not deleted:
                    k += 1


    def dishes_management(self):
        # удаление позиции из списка заказов
        if self.done_animation != [[], [], []]:

            # после анимации неудачи
            if False in self.done_animation[2]:
                i = 0
                while i <= len(self.done_animation[1]) - 1:
                    if self.done_animation[0][i] == 255 and self.done_animation[2][i] == False:
                        for j in range(len(self.done_animation[1])):
                            if self.done_animation[1][j] > self.done_animation[1][i]:
                                self.done_animation[1][j] += -1
                        self.list.pop(self.done_animation[1][i])
                        self.preparing.pop(self.done_animation[1][i])
                        # цикл перенумерации заказов в списке заказов гостей
                        for j in range(len(self.queue_wait)):
                            for p in range(len(self.queue_wait[j][-1])):
                                if self.queue_wait[j][-1] != [None] and self.queue_wait[j][-1][p] > i:
                                    self.queue_wait[j][-1][p] += -1
                        self.done_animation[0].pop(i)  # как бы таймер анимации этой позиции
                        self.done_animation[1].pop(i)  # индекс этой позиции
                        self.done_animation[2].pop(i)  # причина анимации позиции (готово или время)
                    else:
                        i += 1

            # после анимации засчитывания
            i = 0
            done = False
            while i <= len(self.done_animation[1]) - 1 and done == False:
                if self.done_animation[0][i] == 255:
                    for j in range(len(self.done_animation[1])):
                        if self.done_animation[1][j] > self.done_animation[1][i]:
                            self.done_animation[1][j] += -1
                    self.list.pop(self.done_animation[1][i])
                    self.preparing.pop(self.done_animation[1][i])
                    # цикл перенумерации заказов в списке заказов гостей
                    for j in range(len(self.queue_wait)):
                        for p in range(len(self.queue_wait[j][-1])):
                            if self.queue_wait[j][-1] != [None] and self.queue_wait[j][-1][p] > i:
                                self.queue_wait[j][-1][p] += -1
                    self.done_animation[0].pop(i)
                    self.done_animation[1].pop(i)
                    self.done_animation[2].pop(i)
                    done = True
                i += 1
            for i in range(len(self.done_animation[0])):
                self.done_animation[0][i] += 5


    def result(self, hero, scene):
        i = 0
        while i < len(scene.plot_characters[scene.room - 1]):
            if scene.plot_characters[scene.room - 1][i].name[0:7] == 'очередь':
                scene.plot_characters[scene.room - 1].pop(i)
            else:
                i += 1

        if self.letter =='у':
            self.start_timer = [pygame.USEREVENT + 3, 3]
            pygame.time.set_timer(self.start_timer[0], 1000)
            hero.x = 400
            hero.y = 300
            hero.direction = 'вниз'
            hero.hitbox = pygame.Rect(hero.x, hero.y, hero.width, hero.height)
            self.list = []
            self.preparing = []
            self.done_animation = [[], [], []]
            self.score = [0, 0, None]
            self.queue = []
            self.queue_wait = []
            self.queue_away = []
            self.guests = 0
        elif self.letter =='й' and self.score[0] >= self.rules[0]:
            self.score[2] = True


    def tutorial(self, hero, scene):

        # self.message_preparing = None
        if scene.act_started == False:
            if act[scene.act][0][0:8] == 'обучение' and int(act[scene.act][0][9:11]) not in (29, 31):
                self.message_preparing = True

            if act[scene.act][0] == 'обучение 12':
                self.to_say = 'Здравствуйте'
                self.says = ''

            elif act[scene.act][0] == 'обучение 16':
                self.machine = False
                self.list = [['Американо', 'Эс', 'Ки']]
                self.preparing = [['Эс', 'Ки']]

            elif act[scene.act][0] == 'обучение 20':
                self.list = [['Эспрессо', 'Эс'], ['Чай', 'Ча', 'Ки']]
                self.preparing = [['Эс'], ['Ча', 'Ки']]

            elif act[scene.act][0] == 'обучение 29':
                self.rules = [3]
                self.score = [0]
                self.speach = False
                self.machine = False
                self.teatable = False
                self.list = []
                self.preparing = []
                self.done_animation = [[], [], []]
                self.tutorial_to_say = ['Добрый день']
                self.tutorial_list = [['Латте', 'Мо', 'Эс'], ['Чай', 'Ча', 'Ки'], ['Фильтр', 'Фи']]
                self.tutorial_preparing = [['Мо', 'Эс'], ['Ча', 'Ки'], ['Фи']]

            elif act[scene.act][0] == 'обучение 31':
                self.rules = [10, 3]
                self.score = [0, 0]
                self.speach = False
                self.machine = False
                self.teatable = False
                self.list = []
                self.preparing = []
                self.done_animation = [[], [], []]
                self.tutorial_to_say = ['Здравствуйте', 'Рады вас видеть', 'Привет', 'Добрый день', 'Рады вас видеть']
                self.tutorial_list = [['Американо', 'Эс', 'Ки'],
                                              ['Какао', 'Ка', 'Мо'],
                                              ['Чай', 'Ча', 'Ки'],  # 1
                                              ['Фильтр', 'Фи'],  # 2
                                              ['Капучино', 'Эс', 'Мо'],
                                              ['Раф', 'Эс', 'Сл'],  # 3
                                              ['Латте', 'Мо', 'Эс'],  # 4
                                              ['Чай', 'Ча', 'Ки'],
                                              ['Эс', 'Эс'],
                                              ['Какао', 'Ка', 'Мо']]  # 5
                self.tutorial_preparing = [['Эс', 'Ки'], ['Ка', 'Мо'], ['Ча', 'Ки'], ['Фи'], ['Эс', 'Мо'], ['Эс', 'Сл'], ['Мо', 'Эс'], ['Ча', 'Ки'], ['Эс'], ['Ка', 'Мо']]
                self.counted_order_time = 0
                self.counted_cook_time = 0

            elif act[scene.act][0] == 'обучение 34':
                self.list = [['Эспрессо', 'Эс'], ['Чай', 'Ча', 'Ки']]
                self.preparing = [['Эс'], ['Ча', 'Ки']]

            if act[scene.act][0][0:8] == 'обучение':
                scene.act_started = True

        if scene.act_started == True:
            if act[scene.act][0] == 'обучение 01':
                if self.letter == 'в':
                    hero.destination = Cut_interactive((400, 412, 'вправо'))
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 02':
                if self.letter == 'ф':
                    hero.destination = Cut_interactive((360, 364, 'влево'))
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 03':
                if self.letter == 'ы':
                    hero.destination = Cut_interactive((392, 436, 'вниз'))
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 04':
                if self.letter == 'в':
                    hero.destination = Cut_interactive((400, 412, 'вправо'))
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 05':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 06':
                if self.letter == 'ц':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 07':
                if self.letter == 'в':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 08':
                if self.letter == 'ф':
                    hero.destination = Cut_interactive((360, 364, 'влево'))
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 09':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 10':
                if self.letter == 'ы':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 11':
                if self.letter == 'ы':
                    hero.destination = Cut_interactive((392, 436, 'вниз'))
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 12':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 13':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 14':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 15':
                if self.says == self.to_say:
                    self.to_say = None
                    self.says = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 16':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 17':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 18':
                if self.preparing == [['Эс', None]] or self.preparing == [[None, 'Ки']]:
                    self.machine = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 19':
                if self.preparing == [[None, None]]:
                    self.preparing = None
                    self.list = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 20':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 21':
                if self.preparing[0] == [None]:
                    self.list.pop(0)
                    self.preparing.pop(0)
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 22':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 23':
                if self.preparing[0] == ['Ча', None]:
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 24':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 25':
                if self.letter == 'ф':
                    hero.destination = Cut_interactive((360, 364, 'влево'))
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 26':
                if self.preparing[0] == [None, None]:
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 27':
                if self.letter == ' ':
                    self.list = None
                    self.preparing = None
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 28':
                if self.letter == ' ':
                    self.message_preparing = False
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 29':
                if self.score[0] == self.rules[0]:
                    self.machine = None
                    self.teatable = None
                    self.speach = None
                    self.score = None
                    self.rules = None
                    self.list = None
                    self.preparing = None
                    self.done_animation = None
                    self.tutorial_preparing = None
                    self.tutorial_list = None
                    self.tutorial_to_say = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 30':
                if self.letter == ' ':
                    self.message_preparing = False
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 31':
                if self.score[1] == self.rules[1]:
                    scene.act = scene.act + 1
                    scene.act_started = False
                if self.score[0] == self.rules[0]:
                    self.score = None
                    self.rules = None
                    self.machine = None
                    self.teatable = None
                    self.speach = None
                    self.list = None
                    self.preparing = None
                    self.done_animation = None
                    self.tutorial_preparing = None
                    self.tutorial_list = None
                    self.tutorial_to_say = None
                    self.counted_cook_time = (max(8, int(self.counted_cook_time * 1.2 // 120 + 1)))
                    self.counted_order_time = (max(8, int(self.counted_order_time * 1.2 // 120 + 1)))
                    self.return_times = True
                    scene.act = scene.act + 2
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 32':
                if self.letter == ' ':
                    self.message_preparing = False
                    self.letter = None
                    scene.act = scene.act - 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 33':
                if self.letter == ' ':
                    self.letter = None
                    scene.act = scene.act + 1
                    scene.act_started = False

            elif act[scene.act][0] == 'обучение 34':
                if self.letter == ' ':
                    self.letter = None
                    self.message_preparing = False
                    self.list = None
                    self.preparing = None
                    scene.act = scene.act + 1
                    scene.act_started = False


        # передвижение персонажа в обучении
        if act[scene.act][0] == 'реплика' or act[scene.act][0][0:8] == 'обучение' and int(act[scene.act][0][9:11]) < 29:
            if hero.path_to_deal != []:
                hero.walk()

        # ввод текста при первом обучении вводу текста
        if act[scene.act][0] == 'обучение 15':
            self.lettering()

        # первое приготовление напитка
        # приготовление эспрессо при первом приготовлении напитка
        elif act[scene.act][0] == 'обучение 18':
            if self.letter == 'в' and not self.machine:
                hero.destination = Cut_interactive((400, 412, 'вправо'))
                hero.find_path_to_deal(scene.room_map, hero.destination)
                self.machine = True
            if self.machine:
                if self.letter == 'ц':
                    self.preparing = [[None, 'Ки']]
                elif self.letter == 'ф':
                    self.preparing = [['Эс', None]]
        # продолжение первого приготовления
        elif act[scene.act][0] == 'обучение 19':
            if self.letter == 'ц':
                self.preparing[0][0] = None
            elif self.letter == 'ф':
                self.preparing[0][1] = None

        # приготовление эспрессо перед чаем
        elif act[scene.act][0] == 'обучение 21':
            if self.letter == 'ц':
                self.preparing[0] = [None]
        # приготовление кипятка для чая
        elif act[scene.act][0] == 'обучение 23':
            if self.letter == 'ф':
                self.preparing[0][1] = None
        # приготовление чая
        elif act[scene.act][0] == 'обучение 26':
            if self.letter == 'ц':
                self.preparing[0][0] = None

        # первый и второй полный цикл
        elif (act[scene.act][0] == 'обучение 29' or act[scene.act][0] == 'обучение 31') and scene.act_started == True:

            # передвижение персонажа
            if hero.path_to_deal != []:
                hero.walk()
            if not self.speach and not self.machine and not self.teatable:
                if self.letter == 'ф':
                    hero.destination = Cut_interactive((360, 364, 'влево'))
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                    self.teatable = True
                elif self.letter == 'в':
                    hero.destination = Cut_interactive((400, 412, 'вправо'))
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                    self.machine = True
                elif self.letter == 'ы':
                    hero.destination = Cut_interactive((392, 436, 'вниз'))
                    hero.find_path_to_deal(scene.room_map, hero.destination)
                    if self.tutorial_to_say != [] and (self.list == [] or len(self.list) == len(self.done_animation[1])):
                        self.speach = True
                self.letter = None

            # инициация областей
            if hero.x == 392 and hero.y == 436 and self.letter == ' ' and not self.speach:
                self.letter = None
                if self.tutorial_to_say != [] and (self.list == [] or len(self.list) == len(self.done_animation)):
                    self.speach = True
            elif hero.x == 400 and hero.y == 412 and self.letter == ' ' and not self.machine:
                self.letter = None
                self.machine = True
            elif hero.x == 360 and hero.y == 364 and self.letter == ' ' and not self.teatable:
                self.letter = None
                self.teatable = True

            # разговор с гостем
            if self.speach:

                # определение, что нужно сказать
                if self.to_say == None:
                    self.to_say = str(self.tutorial_to_say[0])
                    self.tutorial_to_say.pop(0)
                    self.says = ''

                # завершение диалога с гостем, если фраза введена правильно
                elif self.to_say == self.says:
                    self.says = None
                    self.to_say = None
                    self.speach = False

                    # добавление напитков в заказ
                    if act[scene.act][0] == 'обучение 29':
                        self.list = list(self.tutorial_list)
                        self.preparing = list(self.tutorial_preparing)
                        self.tutorial_list = None
                        self.tutorial_preparing = None
                    if act[scene.act][0] == 'обучение 31':
                        if len(self.tutorial_list) == 10 or len(self.tutorial_list) == 3:
                            # 1
                            self.list.append(list(self.tutorial_list[0]))
                            self.tutorial_list.pop(0)
                            self.preparing.append(list(self.tutorial_preparing[0]))
                            self.tutorial_preparing.pop(0)
                            # 2
                            self.list.append(list(self.tutorial_list[0]))
                            self.tutorial_list.pop(0)
                            self.preparing.append(list(self.tutorial_preparing[0]))
                            self.tutorial_preparing.pop(0)
                            # 3
                            self.list.append(list(self.tutorial_list[0]))
                            self.tutorial_list.pop(0)
                            self.preparing.append(list(self.tutorial_preparing[0]))
                            self.tutorial_preparing.pop(0)
                        elif len(self.tutorial_list) == 7 or len(self.tutorial_list) == 4:
                            self.list.append(list(self.tutorial_list[0]))
                            self.tutorial_list.pop(0)
                            self.preparing.append(list(self.tutorial_preparing[0]))
                            self.tutorial_preparing.pop(0)
                        elif len(self.tutorial_list) == 6:
                            # 1
                            self.list.append(list(self.tutorial_list[0]))
                            self.tutorial_list.pop(0)
                            self.preparing.append(list(self.tutorial_preparing[0]))
                            self.tutorial_preparing.pop(0)
                            # 2
                            self.list.append(list(self.tutorial_list[0]))
                            self.tutorial_list.pop(0)
                            self.preparing.append(list(self.tutorial_preparing[0]))
                            self.tutorial_preparing.pop(0)

                # добавление буквы в высказывание героини
                else:
                    self.lettering()

            # механика слотов
            self.ingredient = None

            if self.machine:
                if len(self.list) == len(self.done_animation[1]) or self.list == [] or self.letter == ' ':
                    self.machine = False
                if self.letter == 'ц':
                    self.ingredient = 'Эс'
                elif self.letter == 'ф':
                    self.ingredient = 'Ки'
                elif self.letter == 'в':
                    self.ingredient = 'Мо'
                elif self.letter == 'ы':
                    self.ingredient = 'Сл'

            if self.teatable:
                if len(self.list) == len(self.done_animation[1]) or self.list == [] or self.letter == ' ':
                    self.teatable = False
                if self.letter == 'ц':
                    self.ingredient = 'Ча'
                elif self.letter == 'ф':
                    self.ingredient = 'Ка'
                elif self.letter == 'в':
                    self.ingredient = 'Си'
                elif self.letter == 'ы':
                    self.ingredient = 'Фи'

            # сверка корректности добавляемого ингредиента
            if self.ingredient != None:
                i = 0
                while i < len(self.preparing) and i < self.skill + len(self.done_animation[1]) and self.ingredient not in self.preparing[i]:
                    i += 1
                # добавление ингредиента, если он корректен и не превышает скилл
                if i < len(self.preparing) and i < self.skill + len(self.done_animation[1]):
                    self.preparing[i][self.preparing[i].index(self.ingredient)] = None
                    # закрытие позиции, если заказ готов
                    if self.preparing[i].count(None) == len(self.preparing[i]):
                        self.score[0] += 1
                        self.done_animation[0].append(60)
                        self.done_animation[1].append(i)
                        self.done_animation[2].append(True)
                else:
                    if act[scene.act][0] == 'обучение 31':
                        self.score[1] += 1

            # удаление позиции из списка заказов
            if self.done_animation != [[], [], []]:

                # после анимации засчитывания
                i = 0
                done = False
                while i <= len(self.done_animation[1]) - 1 and done == False:
                    if self.done_animation[0][i] == 255:
                        for j in range(len(self.done_animation[1])):
                            if self.done_animation[1][j] > self.done_animation[1][i]:
                                self.done_animation[1][j] += -1
                        self.list.pop(self.done_animation[1][i])
                        self.preparing.pop(self.done_animation[1][i])
                        self.done_animation[0].pop(i)
                        self.done_animation[1].pop(i)
                        self.done_animation[2].pop(i)
                        done = True
                    i += 1
                for i in range(len(self.done_animation[0])):
                    self.done_animation[0][i] += 5

            # счет секундомеров
            if act[scene.act][0] == 'обучение 31':
                if (len(self.tutorial_list) == 7 or len(self.tutorial_list) == 0) and self.list != []:
                    self.counted_cook_time += 1
                if self.to_say == 'Рады вас видеть':
                    self.counted_order_time += 1
    # endregion


    def render(self, scene_surface, hero, scene):

        if self.game:

            # отсчет перед началом
            if self.start_timer != None:
                message = self.count_font.render(str(self.start_timer[1]), False, 'Red')
                scene_surface.blit(message, (410, 350))

            # результат игры
            elif self.score[2] == False:
                x = 280  # 200
                y = 220
                w = 380  # 600
                h = 150
                pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, w, h))
                pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, w, h), 2)
                if self.score[0] >= self.rules[0]:
                    message = self.game_font.render('УСПЕХ!', False, 'Black')
                    scene_surface.blit(message, (x + 160, y + 20))
                else:
                    message = self.game_font.render('Неудача', False, 'Black')
                    scene_surface.blit(message, (x + 160, y + 20))
                # cчет заказов
                message = self.game_font.render('Заказов выполнено:', False, 'Black')
                scene_surface.blit(message, (x + 20, y + 50))
                message = self.game_font.render(str(self.score[0]), False, 'Black')
                scene_surface.blit(message, (x + 205 + (self.score[0] > 9) * 10, y + 50))
                # счет неудач
                message = self.game_font.render('Ошибок:', False, 'Black')
                scene_surface.blit(message, (x + 250, y + 50))
                message = self.game_font.render(str(self.score[1]), False, 'Black')
                scene_surface.blit(message, (x + 330, y + 50))
                # кнопки
                if self.score[0] >= self.rules[0]:
                    message = self.game_font.render('Закончить [Q]     Повторить [E]', False, 'Black')
                    scene_surface.blit(message, (x + 60, y + 100))
                else:
                    message = self.game_font.render('               Повторить [E]', False, 'Black')
                    scene_surface.blit(message, (x + 60, y + 100))

            # процесс игры бариста
            else:
                # счет игры: заказы
                x = 235
                y = 473 # 473
                h = 50
                pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 150, h))
                pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 150, h), 2)
                message = self.game_font.render('Заказов:', False, 'Black')
                scene_surface.blit(message, (x, y + 10))
                message = self.game_font.render(str(self.score[0]) + '/' + str(self.rules[0]), False, 'Black')
                scene_surface.blit(message, (x + 100 - (len(str(self.score[0])) - 1) * 10, y + 10))

                # счет игры: ошибки
                y = y + 50
                pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 150, h))
                pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 150, h), 2)
                message = self.game_font.render('Ошибок:', False, 'Black')
                scene_surface.blit(message, (x, y + 10))
                message = self.game_font.render(str(self.score[1]) + '/' + str(self.rules[1]), False, 'Black')
                scene_surface.blit(message, (x + 100 - (len(str(self.score[0])) - 1) * 10, y + 10))


                # таймер ожидающих в очереди
                x = 335
                y = y + 55
                pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, h, h))
                pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, h, h), 2)
                message = self.game_font.render(str(self.queue[0][2]), False, 'Black')
                scene_surface.blit(message, (x + 20 - (self.queue[0][2] > 9) * 10 , y + 10))


                # интерфейс списка заказов
                if self.list != []:

                    x = 505
                    y = 150
                    h = 50
                    # строка "Выполняемые заказы"
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 300, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 300, h), 2)
                    message = self.game_font.render('Выполняемые заказы:', False, 'Black')
                    scene_surface.blit(message, (x, y + 10))
                    # строка "Заказы в очереди"
                    if self.skill + len(self.done_animation[1]) < len(self.list):
                        pygame.draw.rect(scene_surface, 'Gray', (x - 4, y + h * (self.skill + len(self.done_animation[1]) + 1), 300, h))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y + h * (self.skill + len(self.done_animation[1])  + 1), 300, h), 2)
                        message = self.game_font.render('В очереди:', False, 'Black')
                        scene_surface.blit(message, (x, y + 10 + h * (self.skill + len(self.done_animation[1]) + 1)))

                    # поля позиций в заказе
                    for line in range(len(self.list)):
                        rlc = h * (line + 1 + (self.skill + len(self.done_animation[1]) < line + 1)) # relative line coordinate

                        # отображение фона полей заказов, если это не выполненный заказ
                        if self.done_animation == [[], [], []] or line not in self.done_animation[1]:
                            pygame.draw.rect(scene_surface, 'Gray', (x - 4, y + rlc, 300, h))

                        # отображение фона поля заказа, если заказ выполнен
                        elif self.done_animation != [[], [], []] and line in self.done_animation[1] and self.done_animation[2][self.done_animation[1].index(line)] == True:
                            ind = self.done_animation[1].index(line)
                            pygame.draw.rect(scene_surface, (self.done_animation[0][ind], self.done_animation[0][ind], self.done_animation[0][ind]), (x - 4, y + rlc, 300, h))

                        # отображение фона поля заказа, если таймер вышел
                        elif self.done_animation != [[], [], []] and line in self.done_animation[1] and self.done_animation[2][self.done_animation[1].index(line)] == False:
                            ind = self.done_animation[1].index(line)
                            pygame.draw.rect(scene_surface, (255, self.done_animation[0][ind], self.done_animation[0][ind]), (x - 4, y + rlc, 300, h))

                        # названия заказа и его таймеры
                        pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y + rlc, 300, h), 2)
                        
                        message = self.game_font.render(self.list[line][0], False, 'Black')
                        scene_surface.blit(message, (x, y + 10 + rlc))
                        if self.list[line][-1] != None and self.list[line][-1] != 'неудача':
                            message = self.game_font.render(str(self.list[line][-1]), False, 'Black')
                            scene_surface.blit(message, (x + 270 - self.list[line][-1]//10 * 11, y + 10 + rlc))

                        # перечисление ингредиентов
                        for i in range(1, len(self.list[line]) -2):
                            # отображение засчитанного ингредиента темной иконкой
                            if self.preparing[line][i-1] == None:
                                pygame.draw.rect(scene_surface, (100, 100, 100), (x + 100 - 4 + h * (i-1), y + rlc, h, h))
                            # отображение остальных иконок
                            pygame.draw.rect(scene_surface, (80, 80, 80), (x + 100 - 4 + h * (i-1), y + rlc, h, h), 2)
                            message = self.game_font.render(self.list[line][i], False, 'Black')
                            scene_surface.blit(message, (x + 100 + 5 + h * (i-1), y + 10 + rlc))

                # окно диалога с гостем
                if self.speach:
                    x = 220 # 200
                    y = 150
                    w = 280 # 600
                    h = 150
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, w, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, w, h), 2)
                    message = self.game_font.render('Гость', False, 'Black')
                    scene_surface.blit(message, (x, y))
                    message = self.game_font.render('Здравствуйте', False, 'Black')
                    scene_surface.blit(message, (x, y + 25))
                    message = self.game_font.render(str(self.speach_timer[1]), False, 'Black')
                    scene_surface.blit(message, (x + w - 30 - self.speach_timer[1] //10 * 11, y + 25))
                    message = self.game_font.render('Полина', False, 'Black')
                    scene_surface.blit(message, (x + w - 80 , y + 50))
                    message = self.game_font.render(self.says, False, 'Black')
                    scene_surface.blit(message, (x + w - 20 - len(self.says) * 10, y + 75))
                    message = self.game_font.render(self.to_say, False, (80, 80, 80))
                    scene_surface.blit(message, (x + w - 20 - len(self.to_say) * 10, y + 100))

                # интерфейс опций кофе-машины
                if self.machine:
                    x = 500
                    y = 377
                    w = 43
                    print_info = ((x, y, 'Эс'), (x - w, y + w, 'Ки'), (x + w, y + w, 'Мо'), (x, y + w * 2, 'Сл'))
                    for record in print_info:
                        pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                        message = self.game_font.render(record[2], False, 'Black')
                        scene_surface.blit(message, (record[0] + 5, record[1] + 5))

                # интерфейс опций чайного столика
                if self.teatable:
                    x = 280
                    y = 327
                    w = 43
                    print_info = ((x, y, 'Ча'), (x - w, y + w, 'Ка'), (x + w, y + w, 'Си'), (x, y + w * 2, 'Фи'))
                    for record in print_info:
                        pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                        message = self.game_font.render(record[2], False, 'Black')
                        scene_surface.blit(message, (record[0] + 5, record[1] + 5))

        else:
            if act[scene.act][0][0:8] == 'обучение':

                if act[scene.act][0] in ('обучение 05', 'обучение 06', 'обучение 07')  and scene.act_started == True:
                    x = 500
                    y = 377
                    w = 43
                    print_info = ((x, y, 'Эс'), (x - w, y + w, 'Ки'), (x + w, y + w, 'Мо'), (x, y + w * 2, 'Сл'))
                    for record in print_info:
                        pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                        message = self.game_font.render(record[2], False, 'Black')
                        scene_surface.blit(message, (record[0] + 5, record[1] + 5))

                elif (act[scene.act][0] == 'обучение 09' or act[scene.act][0] == 'обучение 10') and scene.act_started == True:
                    x = 280
                    y = 327
                    w = 43
                    print_info = ((x, y, 'Ча'), (x - w, y + w, 'Ка'), (x + w, y + w, 'Си'), (x, y + w * 2, 'Фи'))
                    for record in print_info:
                        pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                        message = self.game_font.render(record[2], False, 'Black')
                        scene_surface.blit(message, (record[0] + 5, record[1] + 5))

                elif act[scene.act][0] in ('обучение 12', 'обучение 13', 'обучение 14', 'обучение 15') and scene.act_started == True:
                    x = 220
                    y = 150
                    w = 280
                    h = 150
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, w, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, w, h), 2)
                    message = self.game_font.render('Гость', False, 'Black')
                    scene_surface.blit(message, (x, y))
                    message = self.game_font.render('Здравствуйте', False, 'Black')
                    scene_surface.blit(message, (x, y + 25))
                    message = self.game_font.render('Полина', False, 'Black')
                    scene_surface.blit(message, (x + w - 80, y + 50))
                    message = self.game_font.render(self.says, False, 'Black')
                    scene_surface.blit(message, (x + w - 20 - len(self.says) * 10, y + 75))
                    message = self.game_font.render(self.to_say, False, (80, 80, 80))
                    scene_surface.blit(message, (x + w - 20 - len(self.to_say) * 10, y + 100))

                elif act[scene.act][0] in ('обучение 16', 'обучение 17', 'обучение 18', 'обучение 19') and scene.act_started == True:

                    x = 500
                    y = 377
                    w = 43
                    print_info = ((x, y, 'Эс'), (x - w, y + w, 'Ки'), (x + w, y + w, 'Мо'), (x, y + w * 2, 'Сл'))
                    for record in print_info:
                        pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                        message = self.game_font.render(record[2], False, 'Black')
                        scene_surface.blit(message, (record[0] + 5, record[1] + 5))

                    x = 505
                    y = 150
                    h = 50
                    # строка "Выполняемые заказы"
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 300, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 300, h), 2)
                    message = self.game_font.render('Выполняемые заказы:', False, 'Black')
                    scene_surface.blit(message, (x, y + 10))

                    # поля позиций в заказе
                    for line in range(len(self.list)):
                        rlc = h * (line + 1 + (self.skill < line + 1))  # relative line coordinate

                        # отображение фона полей заказов, если это не выполненный заказ
                        pygame.draw.rect(scene_surface, 'Gray', (x - 4, y + rlc, 300, h))

                        # названия заказа
                        pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y + rlc, 300, h), 2)
                        message = self.game_font.render(self.list[line][0], False, 'Black')
                        scene_surface.blit(message, (x, y + 10 + rlc))

                        # перечисление ингредиентов
                        for i in range(1, len(self.list[line])):
                            # отображение засчитанного ингредиента темной иконкой
                            if self.preparing[line][i - 1] == None:
                                pygame.draw.rect(scene_surface, (100, 100, 100), (x + 100 - 4 + h * (i - 1), y + rlc, h, h))
                            # отображение остальных иконок
                            pygame.draw.rect(scene_surface, (80, 80, 80), (x + 100 - 4 + h * (i - 1), y + rlc, h, h), 2)
                            message = self.game_font.render(self.list[line][i], False, 'Black')
                            scene_surface.blit(message, (x + 100 + 5 + h * (i - 1), y + 10 + rlc))

                elif act[scene.act][0] in ('обучение 20', 'обучение 21', 'обучение 22', 'обучение 23', 'обучение 24', 'обучение 25', 'обучение 26', 'обучение 27') and scene.act_started == True:
                    if act[scene.act][0] in ('обучение 20', 'обучение 21', 'обучение 22', 'обучение 23', 'обучение 24'):
                        x = 500
                        y = 377
                        w = 43
                        print_info = ((x, y, 'Эс'), (x - w, y + w, 'Ки'), (x + w, y + w, 'Мо'), (x, y + w * 2, 'Сл'))
                        for record in print_info:
                            pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                            pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                            message = self.game_font.render(record[2], False, 'Black')
                            scene_surface.blit(message, (record[0] + 5, record[1] + 5))

                    if act[scene.act][0] == 'обучение 26' or act[scene.act][0] == 'обучение 27':
                        x = 280
                        y = 327
                        w = 43
                        print_info = ((x, y, 'Ча'), (x - w, y + w, 'Ка'), (x + w, y + w, 'Си'), (x, y + w * 2, 'Фи'))
                        for record in print_info:
                            pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                            pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                            message = self.game_font.render(record[2], False, 'Black')
                            scene_surface.blit(message, (record[0] + 5, record[1] + 5))

                    x = 505
                    y = 150
                    h = 50
                    # строка "Выполняемые заказы"
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 300, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 300, h), 2)
                    message = self.game_font.render('Выполняемые заказы:', False, 'Black')
                    scene_surface.blit(message, (x, y + 10))
                    if len(self.list) == 2:
                        pygame.draw.rect(scene_surface, 'Gray', (
                        x - 4, y + h * (self.skill + 1), 300, h))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (
                        x - 4, y + h * (self.skill + 1), 300, h), 2)
                        message = self.game_font.render('В очереди:', False, 'Black')
                        scene_surface.blit(message, (x, y + 10 + h * (self.skill + 1)))

                    # поля позиций в заказе
                    for line in range(len(self.list)):
                        rlc = h * (line + 1 + (self.skill < line + 1))  # relative line coordinate

                        # отображение фона полей заказов, если это не выполненный заказ
                        pygame.draw.rect(scene_surface, 'Gray', (x - 4, y + rlc, 300, h))

                        # названия заказа
                        pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y + rlc, 300, h), 2)
                        message = self.game_font.render(self.list[line][0], False, 'Black')
                        scene_surface.blit(message, (x, y + 10 + rlc))

                        # перечисление ингредиентов
                        for i in range(1, len(self.list[line])):
                            # отображение засчитанного ингредиента темной иконкой
                            if self.preparing[line][i - 1] == None:
                                pygame.draw.rect(scene_surface, (100, 100, 100), (x + 100 - 4 + h * (i - 1), y + rlc, h, h))
                            # отображение остальных иконок
                            pygame.draw.rect(scene_surface, (80, 80, 80), (x + 100 - 4 + h * (i - 1), y + rlc, h, h), 2)
                            message = self.game_font.render(self.list[line][i], False, 'Black')
                            scene_surface.blit(message, (x + 100 + 5 + h * (i - 1), y + 10 + rlc))

                elif act[scene.act][0] == 'обучение 28' and scene.act_started == True:
                    # счет игры: заказы
                    x = 235
                    y = 473
                    h = 50
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 150, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 150, h), 2)
                    message = self.game_font.render('Заказов:', False, 'Black')
                    scene_surface.blit(message, (x, y + 10))
                    message = self.game_font.render('0/3', False, 'Black')
                    scene_surface.blit(message, (x + 100, y + 10))

                elif act[scene.act][0] == 'обучение 30' and scene.act_started == True:
                    # счет игры: ошибки
                    x = 235
                    y = 523  # 473
                    h = 50
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 150, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 150, h), 2)
                    message = self.game_font.render('Ошибок:', False, 'Black')
                    scene_surface.blit(message, (x, y + 10))
                    message = self.game_font.render('0/4', False, 'Black')
                    scene_surface.blit(message, (x + 100, y + 10))

                elif (act[scene.act][0] == 'обучение 29' or act[scene.act][0] == 'обучение 31') and scene.act_started == True:

                    # счет игры: заказы
                    x = 235
                    y = 473
                    h = 50
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 150, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 150, h), 2)
                    message = self.game_font.render('Заказов:', False, 'Black')
                    scene_surface.blit(message, (x, y + 10))
                    message = self.game_font.render(str(self.score[0]) + '/' + str(self.rules[0]), False, 'Black')
                    scene_surface.blit(message, (x + 100 - (len(str(self.score[0])) - 1) * 10, y + 10))

                    # счет игры: ошибки
                    if act[scene.act][0] == 'обучение 31':
                        y = y + 50
                        pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 150, h))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 150, h), 2)
                        message = self.game_font.render('Ошибок:', False, 'Black')
                        scene_surface.blit(message, (x, y + 10))
                        message = self.game_font.render(str(self.score[1]) + '/' + str(self.rules[1]), False, 'Black')
                        scene_surface.blit(message, (x + 100 - (len(str(self.score[0])) - 1) * 10, y + 10))

                    # интерфейс списка заказов
                    if self.list != []:

                        x = 505
                        y = 150
                        h = 50
                        # строка "Выполняемые заказы"
                        pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 300, h))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 300, h), 2)
                        message = self.game_font.render('Выполняемые заказы:', False, 'Black')
                        scene_surface.blit(message, (x, y + 10))
                        # строка "Заказы в очереди"
                        if self.skill + len(self.done_animation[1]) < len(self.list):
                            pygame.draw.rect(scene_surface, 'Gray', (x - 4, y + h * (self.skill + len(self.done_animation[1]) + 1), 300, h))
                            pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y + h * (self.skill + len(self.done_animation[1]) + 1), 300, h), 2)
                            message = self.game_font.render('В очереди:', False, 'Black')
                            scene_surface.blit(message, (x, y + 10 + h * (self.skill + len(self.done_animation[1]) + 1)))

                        # поля позиций в заказе
                        for line in range(len(self.list)):
                            rlc = h * (line + 1 + (self.skill + len(self.done_animation[1]) < line + 1))  # relative line coordinate

                            # отображение фона полей заказов, если это не выполненный заказ
                            if self.done_animation == [[], [], []] or line not in self.done_animation[1]:
                                pygame.draw.rect(scene_surface, 'Gray', (x - 4, y + rlc, 300, h))

                            # отображение фона поля заказа, если заказ выполнен
                            elif self.done_animation != [[], [], []] and line in self.done_animation[1] and self.done_animation[2][self.done_animation[1].index(line)] == True:
                                ind = self.done_animation[1].index(line)
                                pygame.draw.rect(scene_surface, (
                                self.done_animation[0][ind], self.done_animation[0][ind],
                                self.done_animation[0][ind]), (x - 4, y + rlc, 300, h))

                            # названия заказа
                            pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y + rlc, 300, h), 2)
                            message = self.game_font.render(self.list[line][0], False, 'Black')
                            scene_surface.blit(message, (x, y + 10 + rlc))

                            # перечисление ингредиентов
                            for i in range(1, len(self.list[line])):
                                # отображение засчитанного ингредиента темной иконкой
                                if self.preparing[line][i - 1] == None:
                                    pygame.draw.rect(scene_surface, (100, 100, 100), (x + 100 - 4 + h * (i - 1), y + rlc, h, h))
                                # отображение остальных иконок
                                pygame.draw.rect(scene_surface, (80, 80, 80), (x + 100 - 4 + h * (i - 1), y + rlc, h, h), 2)
                                message = self.game_font.render(self.list[line][i], False, 'Black')
                                scene_surface.blit(message, (x + 100 + 5 + h * (i - 1), y + 10 + rlc))

                    # окно диалога с гостем
                    if self.speach:
                        x = 220
                        y = 150
                        w = 280
                        h = 150
                        pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, w, h))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, w, h), 2)
                        message = self.game_font.render('Гость', False, 'Black')
                        scene_surface.blit(message, (x, y))
                        message = self.game_font.render('Здравствуйте', False, 'Black')
                        scene_surface.blit(message, (x, y + 25))
                        message = self.game_font.render('Полина', False, 'Black')
                        scene_surface.blit(message, (x + w - 80, y + 50))
                        message = self.game_font.render(self.says, False, 'Black')
                        scene_surface.blit(message, (x + w - 20 - len(self.says) * 10, y + 75))
                        message = self.game_font.render(self.to_say, False, (80, 80, 80))
                        scene_surface.blit(message, (x + w - 20 - len(self.to_say) * 10, y + 100))

                    # интерфейс опций кофе-машины
                    if self.machine:
                        x = 500
                        y = 377
                        w = 43
                        print_info = ((x, y, 'Эс'), (x - w, y + w, 'Ки'), (x + w, y + w, 'Мо'), (x, y + w * 2, 'Сл'))
                        for record in print_info:
                            pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                            pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                            message = self.game_font.render(record[2], False, 'Black')
                            scene_surface.blit(message, (record[0] + 5, record[1] + 5))

                    # интерфейс опций чайного столика
                    if self.teatable:
                        x = 280
                        y = 327
                        w = 43
                        print_info = ((x, y, 'Ча'), (x - w, y + w, 'Ка'), (x + w, y + w, 'Си'), (x, y + w * 2, 'Фи'))
                        for record in print_info:
                            pygame.draw.rect(scene_surface, 'Gray', (record[0], record[1], 45, 45))
                            pygame.draw.rect(scene_surface, (80, 80, 80), (record[0], record[1], 45, 45), 2)
                            message = self.game_font.render(record[2], False, 'Black')
                            scene_surface.blit(message, (record[0] + 5, record[1] + 5))

                elif act[scene.act][0] == 'обучение 33' and scene.act_started == True:
                    x = 220  # 200
                    y = 150
                    w = 280  # 600
                    h = 150
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, w, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, w, h), 2)
                    message = self.game_font.render('Гость', False, 'Black')
                    scene_surface.blit(message, (x, y))
                    message = self.game_font.render('Здравствуйте', False, 'Black')
                    scene_surface.blit(message, (x, y + 25))
                    message = self.game_font.render('15', False, 'Black')
                    scene_surface.blit(message, (x + w - 30 - 11, y + 25))
                    message = self.game_font.render('Полина', False, 'Black')
                    scene_surface.blit(message, (x + w - 80, y + 50))
                    message = self.game_font.render(' ', False, 'Black')
                    scene_surface.blit(message, (x + w - 30, y + 75))
                    message = self.game_font.render('Привет', False, (80, 80, 80))
                    scene_surface.blit(message, (x + w - 80, y + 100))

                elif act[scene.act][0] == 'обучение 34' and scene.act_started == True:
                    x = 505
                    y = 150
                    h = 50
                    # строка "Выполняемые заказы"
                    pygame.draw.rect(scene_surface, 'Gray', (x - 4, y, 300, h))
                    pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y, 300, h), 2)
                    message = self.game_font.render('Выполняемые заказы:', False, 'Black')
                    scene_surface.blit(message, (x, y + 10))
                    if len(self.list) == 2:
                        pygame.draw.rect(scene_surface, 'Gray', (
                        x - 4, y + h * (self.skill + 1), 300, h))
                        pygame.draw.rect(scene_surface, (80, 80, 80), (
                        x - 4, y + h * (self.skill + 1), 300, h), 2)
                        message = self.game_font.render('В очереди:', False, 'Black')
                        scene_surface.blit(message, (x, y + 10 + h * (self.skill + 1)))

                    # поля позиций в заказе
                    for line in range(len(self.list)):
                        rlc = h * (line + 1 + (self.skill < line + 1))  # relative line coordinate

                        # отображение фона полей заказов, если это не выполненный заказ
                        pygame.draw.rect(scene_surface, 'Gray', (x - 4, y + rlc, 300, h))

                        # названия заказа
                        pygame.draw.rect(scene_surface, (80, 80, 80), (x - 4, y + rlc, 300, h), 2)
                        message = self.game_font.render(self.list[line][0], False, 'Black')
                        scene_surface.blit(message, (x, y + 10 + rlc))
                        message = self.game_font.render('15', False, 'Black')
                        scene_surface.blit(message, (x + 270 - 11, y + 10 + rlc))

                        # перечисление ингредиентов
                        for i in range(1, len(self.list[line])):
                            # отображение засчитанного ингредиента темной иконкой
                            if self.preparing[line][i - 1] == None:
                                pygame.draw.rect(scene_surface, (100, 100, 100), (x + 100 - 4 + h * (i - 1), y + rlc, h, h))
                            # отображение остальных иконок
                            pygame.draw.rect(scene_surface, (80, 80, 80), (x + 100 - 4 + h * (i - 1), y + rlc, h, h), 2)
                            message = self.game_font.render(self.list[line][i], False, 'Black')
                            scene_surface.blit(message, (x + 100 + 5 + h * (i - 1), y + 10 + rlc))

if __name__ == '__main__':
    pass