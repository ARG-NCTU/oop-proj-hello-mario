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
Right_mario_img = pygame.image.load(os.path.join('img', 'Right_mario1.png')).convert()
Left_mario_img = pygame.image.load(os.path.join('img', 'Left_mario1.png')).convert()
Right_mario_jump_img = pygame.image.load(os.path.join('img', 'Right_mario_jump.jpg')).convert()
Left_mario_jump_img = pygame.image.load(os.path.join('img', 'Left_mario_jump.jpg')).convert()
enemy1_img = pygame.image.load(os.path.join('img', 'Left_enemy.png')).convert()
enemy2_img = pygame.image.load(os.path.join('img', 'Right_enemy.png')).convert()
Right_flying_turtle=pygame.image.load(os.path.join('img', 'Right_flying_turtle.png')).convert()
Left_flying_turtle=pygame.image.load(os.path.join('img', 'Left_flying_turtle.png')).convert()
background = pygame.image.load(os.path.join('img', 'background.png')).convert()
background = pygame.transform.scale(background, (3000, HEIGHT))
coin_img = pygame.image.load(os.path.join('img', 'coin.png')).convert()
flag_img = pygame.image.load(os.path.join('img', 'mario_flag.png')).convert()

#載入音樂

eatcoin_sound = pygame.mixer.Sound(os.path.join('sound', 'eatcoin.wav'))
gameover_sound = pygame.mixer.Sound(os.path.join('sound', 'gameover.ogg'))
jump_sound = pygame.mixer.Sound(os.path.join('sound', 'jump.ogg'))  # Load jump sound
pygame.mixer.music.load(os.path.join('sound', 'background.ogg'))

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
        self.image_right = pygame.transform.scale(Right_mario_img, (55, 62))
        self.image_right.set_colorkey(BLACK)
        self.image_left = pygame.transform.scale(Left_mario_img, (55, 62))
        self.image_left.set_colorkey(BLACK)
        self.image = self.image_right  # Initial image set to right
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL  # Get rectangle of image
        self.rect.x = 10
        self.speed = 5
        self.jump_speed = 10
        self.vel_y = 0  # Initial vertical velocity
        self.on_ground = True  # Initialize jump to false

    def update(self):
        keys = pygame.key.get_pressed()

        # Flag variables to ensure certain actions are executed only once
        self.flag1 = True
        self.flag2 = True

        if keys[pygame.K_LEFT]:
            if self.rect.x < -50:
                # Player goes too far to the left, initiate fast descent
                show_game_over()  # Show game over message
                pygame.mixer.stop()  # Stop playing music
                pygame.quit()  # Quit the game
            self.rect.x -= self.speed
            self.image = self.image_left
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = self.image_right
        if keys[pygame.K_UP] and self.on_ground: #if on ground and up key is pressed
            # Play jump sound
            jump_sound.play()
            #image jumps
            if self.image == self.image_right:
                self.image = pygame.transform.scale(Right_mario_jump_img, (55, 62))  # import jump image
            else:
                self.image = pygame.transform.scale(Left_mario_jump_img, (55, 62))  # import jump image
            self.image.set_colorkey(WHITE)
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
                if self.image == self.image_right:
                    self.image = pygame.transform.scale(Right_mario_img, (55, 62))  # import original image
                else:
                    self.image = pygame.transform.scale(Left_mario_img, (55, 62))  # import original image
                self.image.set_colorkey(BLACK) #set white background to transparent

        if keys[pygame.K_DOWN]:
            if self.rect.y > GROUND_LEVEL:  # Preventing the player from moving below the ground level
                self.rect.y = GROUND_LEVEL
            self.rect.y += self.speed
        if self.rect.left > 2900 and self.flag1: #let 3000 be the end of the game 1 
            self.flag1 = False
            darken_screen()
            self.rect.right = 90


class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(enemy2_img, (40, 40))
        self.image_right.set_colorkey(BLACK)
        self.image_left = pygame.transform.scale(enemy1_img, (40, 40))
        self.image_left.set_colorkey(BLACK)
        self.image = self.image_right  # Initial image set to right
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL + 20  # Set the enemy to the same level as Mario
        self.rect.x = WIDTH // 2 - self.rect.width // 2  # Start at the center of the screen
        self.speed = 2  # Fixed speed
        self.direction = -1  # Move left
        self.left_bound = self.rect.x - 100  # Left bound of movement range
        self.right_bound = self.rect.x + 100  # Right bound of movement range

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.direction == 1:  # Moving right
            self.image = self.image_right
        else:  # Moving left
            self.image = self.image_left
            
        if self.rect.right >= self.right_bound or self.rect.left <= self.left_bound:
            self.direction *= -1  # Reverse direction if hitting the boundary
class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(enemy2_img, (40, 40))
        self.image_right.set_colorkey(BLACK)
        self.image_left = pygame.transform.scale(enemy1_img, (40, 40))
        self.image_left.set_colorkey(BLACK)
        self.image = self.image_right  # Initial image set to right
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL + 20  # Set the enemy to the same level as Mario
        self.rect.x = WIDTH - self.rect.width-100 # Start at the rightmost side 100
        self.speed = 3 # Fixed speed
        self.direction = -1  # Move left
        self.left_bound = self.rect.x - 50  # Left bound of movement range
        self.right_bound = self.rect.x + 50  # Right bound of movement range

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.direction == 1:  # Moving right
            self.image = self.image_right
        else:  # Moving left
            self.image = self.image_left

        if self.rect.right >= self.right_bound or self.rect.left <= self.left_bound:
            self.direction *= -1  # Reverse direction if hitting the boundary

class FlyingTurtle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(Right_flying_turtle, (55, 62))
        self.image_right.set_colorkey(BLACK)
        self.image_left = pygame.transform.scale(Left_flying_turtle, (55, 62))
        self.image_left.set_colorkey(BLACK)
        self.image = self.image_right  # Initial image set to right
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL - 90  # Set the initial y position
        self.rect.x = WIDTH // 2 - self.rect.width // 2  # Start at the center of the screen
        self.speed = 2  # Fixed speed
        self.direction = -1  # Move left
        self.left_bound = self.rect.x - 200  # Left bound of movement range
        self.right_bound = self.rect.x + 200  # Right bound of movement range

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.direction == 1:  # Moving right
            self.image = self.image_right
        else:  # Moving left
            self.image = self.image_left

        if self.rect.right >= self.right_bound or self.rect.left <= self.left_bound:
            self.direction *= -1  # Reverse direction if hitting the boundary

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
enemy1 = Enemy1()
all_sprites.add(enemy1)
flying_turtle = FlyingTurtle()
all_sprites.add(flying_turtle)
player = Player()
all_sprites.add(player)
all_sprites.add(flags)
players.add(player)

# Create initial enemy
enemy1 = Enemy1()
all_sprites.add(enemy1)
enemies.add(enemy1)
enemy2 = Enemy2()  # Create the new enemy
all_sprites.add(enemy2)
enemies.add(enemy2)  # Add the new enemy to the enemies group
enemy3=FlyingTurtle()
all_sprites.add(enemy3)
enemies.add(enemy3)
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
pygame.mixer.music.play(-1)  # Loop infinitely
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
    pygame.display.update()
pygame.mixer.stop()
pygame.quit()