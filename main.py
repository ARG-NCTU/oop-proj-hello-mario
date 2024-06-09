import pygame
import os
import random

# Constants
FPS = 60
WIDTH, HEIGHT = 800, 600  # Screen size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.19
GROUND_LEVEL = HEIGHT - 150

# Initialize Pygame
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Group 5 Final Project')
clock = pygame.time.Clock()

#jpg
mario_img = pygame.image.load(os.path.join('img', 'mario1.png')).convert()
mario_jump_img = pygame.image.load(os.path.join('img', 'mario_jump.jpg')).convert()
background = pygame.image.load(os.path.join('img', 'background.png')).convert()
background = pygame.transform.scale(background, (3000, HEIGHT))
coin_img = pygame.image.load(os.path.join('img', 'coin.png')).convert()
enemy1_img = pygame.image.load(os.path.join('img', 'enemy.png')).convert()
flag_img = pygame.image.load(os.path.join('img', 'mario_flag.png')).convert()

#載入音樂
background_sound = pygame.mixer.Sound(os.path.join('sound', 'background.mp3'))
jump_sound = pygame.mixer.Sound(os.path.join('sound', 'jump.wav'))
eatcoin_sound = pygame.mixer.Sound(os.path.join('sound', 'eatcoin.wav'))
gameover_sound = pygame.mixer.Sound(os.path.join('sound', 'gameover.ogg'))

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

# Transition of the screen
def darken_screen():
    dark_img = screen.convert_alpha()
    for opacity in range(0, 255, 15):
        clock.tick(FPS)
        dark_img.fill((*BLACK, opacity))
        screen.blit(dark_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(100)

# Display Game Over message
def show_game_over():
    gameover_sound.play()  # Play game over sound
    pygame.time.delay(500)  # Delay to ensure the sound plays fully
    font = pygame.font.SysFont(None, 74)
    text = font.render('GAME OVER', True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)

class Coin(pygame.sprite.Sprite):
    def __init__(self,type,coin_num,coin_start):
        super().__init__()
        self.image = pygame.transform.scale(coin_img,(50,50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coin_start = coin_start
        if type ==1:
            self.rect.y = GROUND_LEVEL
        else:
            self.rect.y = GROUND_LEVEL - 250 #if type 2, place coin higher
        self.rect.x = coin_start+ coin_num*80
        self.coin_num = coin_num

    def update(self):
        if self.rect.x<= 0 or self.rect.x >=3000 : #if coin reaches end of screen
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(mario_img,(55,71)) #import image
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
        self.flag1 = True
        self.flag2 = True

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.on_ground: #if on ground and up key is pressed
            #image jumps
            self.image = pygame.transform.scale(mario_jump_img,(55,71)) #import jump image
            self.image.set_colorkey(WHITE) #set white background to transparent
            jump_sound.play()
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
                self.image = pygame.transform.scale(mario_img,(55,71)) #import original image
                self.image.set_colorkey(BLACK) #set white background to transparent

        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if self.rect.left > 2900 and self.flag1: #let 3000 be the end of the game 1 
            self.flag1 = False
            darken_screen()
            self.rect.right = 90


class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(enemy1_img, (40, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL + 20  # Set the enemy to the same level as Mario
        self.rect.x = WIDTH - self.rect.width  # Start at the right edge
        self.speed = 2  # Fixed speed
        self.direction = -1  # Move left

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0:  # Reset to the right edge if it goes off the left side
            self.rect.x = WIDTH - self.rect.width

class Flag(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(flag_img, (131, 300))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL - 230  # Set the enemy to the same level as Mario
        self.rect.x = 2900  # Start at the right edge


# Create sprite group and player instance
all_sprites = pygame.sprite.Group()

coins = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()

flags = Flag()
player = Player()
all_sprites.add(player)
all_sprites.add(flags)
players.add(player)

# Create initial enemy
enemy1 = Enemy1()
all_sprites.add(enemy1)
enemies.add(enemy1)

def create_coin(existing_end_positions):
    type_num = random.randint(1,2)
    coin_num = random.randint(1,10)
    if existing_end_positions:
        coin_start = max(existing_end_positions) + random.randint(50,150)
    else: coin_start = random.randrange(0,WIDTH-200)

    coin_end = coin_start + coin_num*80

    #create coins
    for i in range(coin_num): #create 一組連續金幣
        coin_num = i+1
        coin = Coin(type_num,coin_num,coin_start)
        all_sprites.add(coin)
        coins.add(coin)
    return coin_end

coin_end_positions = [] #store the end positions of coins
for i in range(5): #create 5 sets of coins
    coin_end_positions.append(create_coin(coin_end_positions))

# type_num = random.randint(1,2)
# coin_num = random.randint(1,10)
# coin_start = random.randrange(0,WIDTH-200)

# for i in range(coin_num): #create 一組連續金幣
#     coin_num = i+1
#     coin = Coin(type_num,coin_num,coin_start)
#     all_sprites.add(coin)
#     coins.add(coin)

# type_num = random.randint(1,2)
# coin_num = random.randint(1,10)
# coin_start = random.randrange(coin_start,WIDTH)

# for i in range(coin_num): #create 一組連續金幣
#     coin_num = i+1
#     coin = Coin(type_num,coin_num,coin_start)
#     all_sprites.add(coin)
#     coins.add(coin)

score = 0

# Camera offset
camera_offset = pygame.Vector2(0, 0)


# Main game loop
running = True
game_over = False
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if not game_over:
        # Update
        all_sprites.update()
    
        # Check for collisions
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True
            show_game_over()
            running = False

    eat_coin = pygame.sprite.groupcollide(players, coins, False, True) #if player collides with coin, kill coin

    for eat in eat_coin: #if player collides with coin, score +1
        eatcoin_sound.play()
        score += 1
        print(score)

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

    draw_text(screen, 'score is: '+ str(score), 18, WIDTH / 2, 10) #分數顯示在最上層
    #background_sound.play()
    pygame.display.update()

pygame.quit()