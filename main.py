import pygame

from System import init_game, events_tracking
# импорт классов: --Сцена, -- Мебель, --Герой
from Objects.game import Game
from Objects.scene import Scene
from Objects.characters import Hero

SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock_on, screen, animation_timer = init_game.init_game()



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
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                hero, scene = game.transfering_room(hero, scene)

            # расстановка --Мебели и -- Интерактива
            if game.recreate_room:
                game.recreate_room = scene.placing_furniture()
                scene.placing_interactive()

            # управление персонажем
            if pygame.key.get_pressed() != None:
                hero.move(pygame.key.get_pressed(), furniture)






            # отрисовка сцены
            scene.draw(scene_surface)

            # отрисовка интерактивных областей
            for object in scene.interactive:
                object.draw(scene_surface, timer)

            # отрисовка объектов и персонажа
            for object in scene.furniture:
                if object.hitbox[1] < hero.hitbox[1]:
                    object.draw(scene_surface, timer)

            hero.draw(scene_surface, timer)

            #проверка на нахождение в интерактивной области (временная)
            if interactive != []:
                #отрисовка интерактивного сообщения
                hero.action(scene_surface, interactive[0])

            for object in scene.furniture:
                if object.hitbox[1] >= hero.hitbox[1]:
                    object.draw(scene_surface, timer)

        # рендер графики и обновление экрана
        screen.blit(scene_surface, (0, 0))
        pygame.display.update()


        clock_on.tick(FPS)
pygame.quit()