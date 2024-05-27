import pygame
import os


FPS = 60
WIDTH, HEIGHT = 800, 600 #screen size
GRAVITY = 0.2
WHITE = (255, 255, 255)
BLACK = (0,0,0)

#INITIALIZE PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Group 5 Final Project')
clock = pygame.time.Clock()

#jpg
mario_img = pygame.image.load(os.path.join('img', 'mario1.png')).convert()
mario_jump_img = pygame.image.load(os.path.join('img', 'mario_jump.jpg')).convert()
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
        self.image = pygame.transform.scale(mario_img,(120,62)) #import image
        self.image.set_colorkey(BLACK) #set white background to transparent
        self.rect = self.image.get_rect()  #get rectangle of image
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.rect.y = HEIGHT - 62
        self.speed = 5
        self.jump_speed = 10
        self.vel_y = 0 #initial vertical velocity
        self.on_ground = True #initialize jump to false

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.on_ground: #if on ground and up key is pressed
            #image jumps
            self.image = pygame.transform.scale(mario_jump_img,(55,62)) #import jump image
            self.image.set_colorkey(WHITE) #set white background to transparent
            self.vel_y = -self.jump_speed
            self.on_ground = False
        #gravity
        if not self.on_ground:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y
            if self.rect.y > HEIGHT - 62:
                self.rect.y = HEIGHT - 62
                self.on_ground = True
                self.vel_y = 0
                self.image = pygame.transform.scale(mario_img,(120,62)) #import original image
                self.image.set_colorkey(BLACK) #set white background to transparent

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
    