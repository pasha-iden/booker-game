import pygame

def scene():
    room = pygame.image.load('files/images/room.jpg').convert()
    scene_surface = pygame.Surface((960, 540))
    scene_surface.blit(room, (0, 0))

    return scene_surface

if __name__ == '__main__':
    scene()