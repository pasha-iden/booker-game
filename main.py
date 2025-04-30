import pygame

from System import init_game, events_tracking
# импорт классов: --Сцена, -- Мебель, --Герой
from Objects.game import Game
from Objects.scene import Scene
from Objects.characters import Hero

SCREEN_WIDTH, SCREEN_HEIGHT, FPS, clock_on, screen, animation_timer = init_game.init_game()



game = Game()
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

            # управление персонажем
            if pygame.key.get_pressed() != None:
                hero.move(pygame.key.get_pressed(), scene.furniture)






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

            #проверка на существование интерактивной области и отрисовка интерактивного сообщения
            if scene.interactive != None:
                hero.action(scene_surface, scene.interactive)

            for object in scene.furniture:
                if object.hitbox[1] >= hero.hitbox[1]:
                    object.draw(scene_surface, timer)

        # рендер графики и обновление экрана
        screen.blit(scene_surface, (0, 0))
        pygame.display.update()


        clock_on.tick(FPS)
pygame.quit()