import pygame

FPS = 60
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Group 5 Final Project')
clock = pygame.time.Clock()

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    screen.fill(WHITE)
    pygame.display.update()
    