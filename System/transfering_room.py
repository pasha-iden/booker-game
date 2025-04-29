import pygame

def transfering_room (hero, key, scene_room):
    if hero.hitbox.collidepoint((25, 750)) and key[pygame.K_SPACE] and scene_room == 3:
        scene_room = 2
        hero.x = 730
        hero.y = 30
    if hero.hitbox.collidepoint((760, 30)) and key[pygame.K_SPACE] and scene_room == 2:
        scene_room = 3
        hero.x = 25
        hero.y = 700
    if hero.hitbox.collidepoint((455, 760)) and key[pygame.K_SPACE] and scene_room == 2:
        scene_room = 1
        hero.x = 455
        hero.y = 130
    if hero.hitbox.collidepoint((455, 130)) and key[pygame.K_SPACE] and scene_room == 1:
        scene_room = 2
        hero.x = 455
        hero.y = 700

    return scene_room, hero