import pygame
import os
import random

# Constants
FPS = 60
WIDTH, HEIGHT = 800, 600  # Screen size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.19
GROUND_LEVEL = HEIGHT - 140

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Group 5 Final Project')
clock = pygame.time.Clock()

#jpg
mario_img = pygame.image.load(os.path.join('img', 'mario1.png')).convert()
mario_jump_img = pygame.image.load(os.path.join('img', 'mario_jump.jpg')).convert()
background = pygame.image.load(os.path.join('img', 'background.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
coin_img = pygame.image.load(os.path.join('img', 'coin.png')).convert()

# Transition of the screen
def darken_screen():
    dark_img = screen.convert_alpha()
    for opacity in range(0, 255, 15):
        clock.tick(FPS)
        dark_img.fill((*BLACK, opacity))
        screen.blit(dark_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(100)

class Coin(pygame.sprite.Sprite):
    def __init__(self,type,coin_num):
        super().__init__()
        self.image = pygame.transform.scale(coin_img,(50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        if type ==1:
            self.rect.y = GROUND_LEVEL
        else:
            self.rect.y = GROUND_LEVEL - 250 #if type 2, place coin higher
        self.rect.x = random.randrange(0,WIDTH-200) + coin_num*100
        self.coin_num = coin_num

    def update(self):
        if self.rect.x<= 0 or self.rect.x >=WIDTH : #if coin reaches end of screen
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(mario_img,(120,62)) #import image
        self.image.set_colorkey(BLACK) #set white background to transparent
        self.rect = self.image.get_rect()  #get rectangle of image
        self.rect.y = GROUND_LEVEL #get rectangle of image
        self.rect.x = 10
        #self.rect.center = (WIDTH/2, HEIGHT/2)
        #self.rect.y = HEIGHT - 62
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
            if self.rect.y > GROUND_LEVEL:
                self.rect.y = GROUND_LEVEL
                self.on_ground = True
                self.vel_y = 0
                self.image = pygame.transform.scale(mario_img,(120,62)) #import original image
                self.image.set_colorkey(BLACK) #set white background to transparent

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if self.rect.left > WIDTH:
            darken_screen()
        
            self.rect.right = 90

# Create sprite group and player instance
all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()
players = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
players.add(player)

type_num = random.randint(1,2)
coin_num = random.randint(1,10)

for i in range(coin_num):
    coin_num = i+1
    coin = Coin(type_num,coin_num)
    all_sprites.add(coin)
    coins.add(coin)


# Camera offset
camera_offset = pygame.Vector2(0, 0)

# Main game loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update sprites
    all_sprites.update()
    pygame.sprite.groupcollide(players, coins, False, True) #if player collides with coin, kill coin

    # Update camera offset based on player movement
    camera_offset.x = player.rect.centerx - WIDTH / 2
    #camera_offset.y = player.rect.centery - HEIGHT / 2 # Camera also moves in y direction
    camera_offset.y = 0 # Camera only moves in x direction

    # Draw everything
    screen.fill((93, 147, 253))

    # Draw background with camera offset
    screen.blit(background, (-camera_offset.x, -camera_offset.y))

    # Draw sprites with camera offset
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect.topleft - camera_offset)

    pygame.display.update()

pygame.quit()