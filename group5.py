import pygame
import os


FPS = 60
WIDTH, HEIGHT = 800, 600 #screen size
WHITE = (255, 255, 255)
BLACK = (0,0,0)

#INITIALIZE PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Group 5 Final Project')
clock = pygame.time.Clock()

#jpg
mario_jpg = pygame.image.load(os.path.join('img', 'mario.jpg')).convert()
background = pygame.image.load(os.path.join('img', 'background.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

#transition of the screen
def darken_screen():
    dark_img = screen.convert_alpha()
    for opacity in range(0, 255, 15):
        clock.tick(FPS)
        dark_img.fill((*BLACK, opacity))
        screen.blit(dark_img, (0,0))
        pygame.display.update()
        pygame.time.delay(100)



class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(mario_jpg,(120,62)) #import image
        self.image.set_colorkey(WHITE) #set white background to transparent
        self.rect = self.image.get_rect()  #get rectangle of image
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.speed = 5
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if self.rect.left > WIDTH:
            darken_screen()
        
            self.rect.right = 90

all_sprites = pygame.sprite.Group()
player = player()
all_sprites.add(player)


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # update
    all_sprites.update()
    # display
    screen.fill(WHITE)
    screen.blit(background, (0,0))
    all_sprites.draw(screen) # Draw the group
    pygame.display.update()

pygame.quit()
    