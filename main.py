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




            # СОБЫТИЯ NPC
            character_go_away = None
            can_go_away = len(scene.characters[scene.room-1]) > (len(scene.chairs) // 2)
            # NPC принимают решения и идут к своей цели
            for character in scene.characters[scene.room-1]:
                scene.interactive, go_away = character.decision(game.timer, scene.room_map, scene.interactive, can_go_away)
            # передвижение NPC
                if character.path_to_deal != None:
                    character.walk()
            # если NPC решил уйти
                if go_away == True:
                    character_go_away = character
                    go_away = False
            if character_go_away != None:
                scene.empty_chairs[scene.room-1].append(character_go_away.chair)
                scene.characters[scene.room-1].pop(scene.characters[scene.room-1].index(character_go_away))
            # приход нового NPC
            scene.adding_character(game.timer)





            # отрисовка сцены
            scene.draw(scene_surface)

            # отрисовка интерактивных областей
            for object in scene.interactive:
                object.draw(scene_surface, game.timer)
            for object in scene.chairs:
                object.draw(scene_surface, game.timer)




            rendering_objects = []
            for object in scene.characters[scene.room -1]:
                rendering_objects.append((object.y + hero.height * 1.5, object.type, scene.characters[scene.room -1].index(object)))
            for object in scene.furniture:
                rendering_objects.append((object.y + object.height, object.type, scene.furniture.index(object)))
            rendering_objects.append((hero.y + hero.height * 1.5, 'герой', 0))
            rendering_objects.sort(key=lambda x: x[0])

            for object in rendering_objects:
                if object[1] == 'sub_character':
                    scene.characters[scene.room -1][object[2]].draw(scene_surface, game.timer)
                elif object[1] == 'furniture':
                    scene.furniture[object[2]].draw(scene_surface, game.timer)
                else:
                    hero.draw(scene_surface, game.timer)



            # отрисовка объектов и игрока
            # for object in scene.furniture:
            #     if object.hitbox[1] < hero.hitbox[1]:
            #         object.draw(scene_surface, game.timer)
            #
            # hero.draw(scene_surface, game.timer)
            # for object in scene.characters[scene.room-1]:
            #     object.draw(scene_surface, game.timer)

            #проверка на существование интерактивной области и отрисовка интерактивного сообщения
            # if scene.interactive != None:
            #     hero.action(scene_surface, scene.interactive)
            #
            # for object in scene.furniture:
            #     if object.hitbox[1] >= hero.hitbox[1]:
            #         object.draw(scene_surface, game.timer)

        # рендер графики и обновление экрана
        game.screen.blit(scene_surface, (0, 0))
        pygame.display.update()


        game.clock_on.tick(game.FPS)
pygame.quit()