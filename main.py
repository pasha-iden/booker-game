import pygame

from System import init_game, events_tracking, transfering_room
from Objects.scene import Scene
from Objects.furniture import Furniture
from Objects.characters import Character, Hero
from Objects.rooms_furniture import room_furniture

SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock_on, screen, animation_timer, game_running = init_game.init_game()



objects = []
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

        # расстановка мебели
        if scene_room != scene_room_before:
            objects = room_furniture(scene_room)

        # управление персонажем
        if pygame.key.get_pressed() != None:
            hero.move(pygame.key.get_pressed(), objects)






        # отрисовка сцены
        scene.draw(scene_surface, scene_room)

        # отрисовка объектов и персонажа
        for object in objects:
            if object.hitbox[1] < hero.hitbox[1]:
                object.draw(scene_surface, timer)

        hero.draw(scene_surface, timer)

        for object in objects:
            if object.hitbox[1] >= hero.hitbox[1]:
                object.draw(scene_surface, timer)

        # рендер графики и обновление экрана
        screen.blit(scene_surface, (0, 0))
        pygame.display.update()


        clock_on.tick(FPS)