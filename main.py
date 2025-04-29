import pygame

from Objects.furniture import Furniture
from System import init_game
from Objects.scene import scene
from Objects.characters import Character, Hero

FPS, clock_on, screen, animation_timer, game_running = init_game.init_game()



objects = []
hero = Hero()
table1 = (0, 350, 200, 100)
table2 = (400, 250, 150, 130)
table3 = (0, 0, 250, 200)
table4 = (400, 0, 100, 150)
table5 = (550, 0, 100, 100)
table6 = (780, 230, 100, 100)
table7 = (720, 420, 150, 130)


Furniture (objects, table1[0], table1[1], table1[2], table1[3])
Furniture (objects, table2[0], table2[1], table2[2], table2[3])
Furniture (objects, table3[0], table3[1], table3[2], table3[3])
Furniture (objects, table4[0], table4[1], table4[2], table4[3])
Furniture (objects, table5[0], table5[1], table5[2], table5[3])
Furniture (objects, table6[0], table6[1], table6[2], table6[3])
Furniture (objects, table7[0], table7[1], table7[2], table7[3])



while game_running:
    timer = False


    for event in pygame.event.get():

        if event.type == animation_timer:
            timer = True

        if event.type == pygame.QUIT:
            game_running = False
            pygame.quit()


    # управление персонажем
    if pygame.key.get_pressed() != None:
        hero.move(pygame.key.get_pressed(), objects)

    # отрисовка всей графики
    scene_surface = scene()

    for object in objects:
        if object.hitbox[1] < hero.hitbox[1]:
            object.draw(scene_surface, timer)

    hero.draw(scene_surface, timer)

    for object in objects:
        if object.hitbox[1] >= hero.hitbox[1]:
            object.draw(scene_surface, timer)

    screen.blit(scene_surface, (0, 0))
    pygame.display.update()


    clock_on.tick(FPS)