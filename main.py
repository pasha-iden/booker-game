import pygame

from System import init_game, events_tracking
# импорт классов: --Сцена, -- Мебель, --Герой
from Objects.game import Game
from Objects.scene import Scene
from Objects.characters import Hero
# импорт функций: -- Расстановка мебели, -- Расстановка интерактивных областей
from System.rooms_furniture import room_furniture
from System.rooms_interactive import room_interactive

SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock_on, screen, animation_timer = init_game.init_game()



#редактируется эта часть
game = Game()

furniture = []
interactive = []
hero = Hero()
scene = Scene()
scene_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))



while game.running:
    scene_surface.fill('Black')

    #отслеживание событий: --Таймер и --Выход из игры
    timer, game.running = events_tracking.events_tracking (animation_timer)

    if game.running:

        # работа меню (редактируется)
        if game.just_started or game.pause or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            hero, scene = game.menu_window(scene_surface, hero, scene)
        else:

            # перемещение между комнатами
            scene.room_before = scene.room
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                hero, scene = game.transfering_room(hero, scene)

            # расстановка --Мебели и -- Интерактива
            if scene.room != scene.room_before:
                furniture = room_furniture(scene.room)
                interactive = room_interactive(scene.room)

            # управление персонажем
            if pygame.key.get_pressed() != None:
                hero.move(pygame.key.get_pressed(), furniture)






            # отрисовка сцены
            scene.draw(scene_surface)

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
pygame.quit()