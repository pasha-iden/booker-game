import pygame

def init_game():
    pygame.init()

    SCREEN_WIDTH = 960
    SCREEN_HEIGHT = 540
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.NOFRAME)  # базовое разрешение
    # screen = pygame.display.set_mode((1920, 1040), pygame.FULLSCREEN)

    pygame.display.set_caption('Booker - The Coffee Adventure')
    icon = pygame.image.load('Booker.png')
    pygame.display.set_icon(icon)

    clock_on = pygame.time.Clock()
    FPS = 60

    animation_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(animation_timer, 1000)  # в милисекундах

    game_running = True

    return FPS, clock_on, screen, animation_timer, game_running

if __name__ == '__main__':
    init_game()