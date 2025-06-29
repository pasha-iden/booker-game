import pygame

import time

from Objects.game import Game
from Objects.scene import Scene
from Objects.characters import Hero



game = Game()
hero = Hero()
scene = Scene()
scene_surface = pygame.Surface((game.SCREEN_WIDTH, game.SCREEN_HEIGHT))

while game.running:
    scene_surface.fill('Black')

    # отслеживание событий: --Таймер, --Кнопка Escape, --Выход из игры
    game.events_tracking()


    if game.running:

        start_time = time.perf_counter()
        # меню игры
        if game.just_started or game.pause or game.pushed_ESCAPE:
            hero, scene = game.menu_window(scene_surface, hero, scene)
        else:


            # менеджер кат-сцены
            game.cut_scene(hero, scene)



            # перемещение между комнатами
            if game.pushed_SPACE and game.fade_animation == None and game.cut_data[1] == True:
                game.transfering_room_initiation(hero, scene)
            if game.fade_animation == 0:
                game.transfering_room(hero, scene)
                game.fade_animation = 1
            if game.fade_animation == 12:
                game.fade_animation = None


            # управление игроком
            if game.fade_animation == None and game.cut_data[0] == True and pygame.key.get_pressed() != None:
                hero.move(pygame.key.get_pressed(), scene.furniture)



            # СОБЫТИЯ NPC
            character_go_away = None
            can_go_away = len(scene.characters[scene.room-1]) > (len(scene.chairs) // 2)
            # NPC принимают решения и идут к своей цели
            for character in scene.characters[scene.room-1]:
                scene.interactive, go_away = character.decision(game.timer, scene.room_map, scene.interactive, can_go_away)
            # передвижение NPC
                if character.path_to_deal != []:
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



            # МИНИ-ИГРЫ
            game.mini_games_logica(hero, scene)



            # рендер всех объектов
            game.render(scene_surface, hero, scene)
            game.cut_effects_render(scene_surface, hero, scene)
            game.mini_game_render(scene_surface, hero, scene)
            game.after_effects(scene_surface)


        # if not game.pause:
        #     print(pygame.mouse.get_pos())


        # рендер графики и обновление экрана
        game.screen.blit(scene_surface, (game.screen_shift[game.screen_mod][0], game.screen_shift[game.screen_mod][1]))
        pygame.display.update()

        end_time = time.perf_counter()
        execution_time = end_time - start_time
        # print(f"{execution_time:.6f}")

        game.clock_on.tick(game.FPS)
pygame.quit()