import pygame


def events_tracking (animation_timer):
    timer = False
    game_running = True
    for event in pygame.event.get():

        if event.type == animation_timer:
            timer = True

        if event.type == pygame.QUIT:
            game_running = False

    return timer, game_running

if __name__ == '__main__':
    pass