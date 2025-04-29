import pygame

from System import init_game, events_tracking, transfering_room
from Objects.scene import Scene
from Objects.furniture import Furniture
from Objects.characters import Character, Hero

SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock_on, screen, animation_timer, game_running = init_game.init_game()



objects = []
hero = Hero()
scene = Scene()
scene_room = 2
scene_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# table1 = (0, 350, 200, 100)
# table2 = (400, 250, 150, 130)
# table3 = (0, 0, 250, 200)
# table4 = (400, 0, 100, 150)
# table5 = (550, 0, 100, 100)
# table6 = (780, 230, 100, 100)
# table7 = (720, 420, 150, 130)
#
#
# Furniture (objects, table1[0], table1[1], table1[2], table1[3])
# Furniture (objects, table2[0], table2[1], table2[2], table2[3])
# Furniture (objects, table3[0], table3[1], table3[2], table3[3])
# Furniture (objects, table4[0], table4[1], table4[2], table4[3])
# Furniture (objects, table5[0], table5[1], table5[2], table5[3])
# Furniture (objects, table6[0], table6[1], table6[2], table6[3])
# Furniture (objects, table7[0], table7[1], table7[2], table7[3])



while game_running:
    scene_surface.fill('Black')

    #отслеживание событий: --Таймер и --Выход из игры
    timer, game_running = events_tracking.events_tracking (animation_timer)

    if game_running:

        # управление персонажем
        if pygame.key.get_pressed() != None:
            hero.move(pygame.key.get_pressed(), objects)
        # перемещение между комнатами
        scene_room, hero = transfering_room.transfering_room(hero, pygame.key.get_pressed(), scene_room)

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