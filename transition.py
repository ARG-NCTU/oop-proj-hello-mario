import pygame

BLACK = (255,255,255)
WHITE = (0,0,0)

FPS = 60  # frames per second
screen = pygame.display.set_mode((100,100))
screen.fill(WHITE)
clock = pygame.time.Clock()
def darken_screen():
    dark_img = screen.convert_alpha()
    for opacity in range(0, 255,15):
        clock.tick(FPS)
        dark_img.fill((*BLACK, opacity))
        screen.blit(dark_img, (0,0))
        pygame.display.update()
        pygame.time.delay(10)
