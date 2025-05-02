import pygame

from Objects.game import Game
from Objects.scene import Scene
from Objects.characters import Hero, Character



game = Game()
hero = Hero()
scene = Scene()
scene_surface = pygame.Surface((game.SCREEN_WIDTH, game.SCREEN_HEIGHT))



while game.running:
    scene_surface.fill('Black')

    #отслеживание событий: --Таймер, --Кнопка Escape, --Выход из игры
    game.events_tracking()

    if game.running:

        # меню игры
        if game.just_started or game.pause:
            hero, scene = game.menu_window(scene_surface, hero, scene)
        else:

            # перемещение между комнатами
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                hero, scene = game.transfering_room(hero, scene)

            # управление игроком
            if pygame.key.get_pressed() != None:
                hero.move(pygame.key.get_pressed(), scene.furniture)


            # NPC принимают решения и идут к своей цели
            for character in scene.characters[scene.room-1]:
                character.decision(game.timer, scene.room_map, scene.interactive[0])
            # передвижение NPC
                if character.path_to_deal != None:
                    character.walk()





            # отрисовка сцены
            scene.draw(scene_surface)

            # отрисовка интерактивных областей
            for object in scene.interactive:
                object.draw(scene_surface, game.timer)
            for object in scene.chairs:
                object.draw(scene_surface, game.timer)

            # отрисовка объектов и игрока
            for object in scene.furniture:
                if object.hitbox[1] < hero.hitbox[1]:
                    object.draw(scene_surface, game.timer)

            hero.draw(scene_surface, game.timer)
            for object in scene.characters[scene.room-1]:
                object.draw(scene_surface, game.timer)

            #проверка на существование интерактивной области и отрисовка интерактивного сообщения
            if scene.interactive != None:
                hero.action(scene_surface, scene.interactive)

            for object in scene.furniture:
                if object.hitbox[1] >= hero.hitbox[1]:
                    object.draw(scene_surface, game.timer)

        # рендер графики и обновление экрана
        game.screen.blit(scene_surface, (0, 0))
        pygame.display.update()


        game.clock_on.tick(game.FPS)
pygame.quit()