import pygame

from System import init_game, events_tracking, transfering_room
# импорт классов: --Сцена, -- Мебель, --Герой
from Objects.scene import Scene
from Objects.characters import Hero
# импорт функций: -- Расстановка мебели, -- Расстановка интерактивных областей
from System.rooms_furniture import room_furniture
from System.rooms_interactive import room_interactive

SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock_on, screen, animation_timer, game_running = init_game.init_game()



furniture = []
interactive = []
hero = Hero()
scene = Scene()
scene_room = 2
scene_room_before = scene_room
scene_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))



while game_running:
    scene_surface.fill('Black')

    #отслеживание событий: --Таймер и --Выход из игры
    timer, game_running = events_tracking.events_tracking (animation_timer)

    if game_running:

        # перемещение между комнатами
        scene_room_before = scene_room
        scene_room, hero = transfering_room.transfering_room(hero, pygame.key.get_pressed(), scene_room)

        # расстановка --Мебели и -- Интерактива
        if scene_room != scene_room_before:
            furniture = room_furniture(scene_room)
            interactive = room_interactive(scene_room)

        # управление персонажем
        if pygame.key.get_pressed() != None:
            hero.move(pygame.key.get_pressed(), furniture)






        # отрисовка сцены
        scene.draw(scene_surface, scene_room)

        # отрисовка интерактивных областей
        for object in interactive:
            object.draw(scene_surface, timer)

        # отрисовка объектов и персонажа
        for object in furniture:
            if object.hitbox[1] < hero.hitbox[1]:
                object.draw(scene_surface, timer)

        hero.draw(scene_surface, timer)

        #проверка на нахождение в интерактивной области (временная)
        if interactive != []:
            #отрисовка интерактивного сообщения
            hero.action(scene_surface, interactive[0])

        for object in furniture:
            if object.hitbox[1] >= hero.hitbox[1]:
                object.draw(scene_surface, timer)

        # рендер графики и обновление экрана
        screen.blit(scene_surface, (0, 0))
        pygame.display.update()


        clock_on.tick(FPS)