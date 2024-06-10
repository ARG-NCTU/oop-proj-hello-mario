import pygame
import os
import random
from os.path import isfile, join


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

# Images
Right_mario_img = pygame.image.load(os.path.join('img', 'Right_mario1.png')).convert()
Left_mario_img = pygame.image.load(os.path.join('img', 'Left_mario1.png')).convert()
Right_mario_jump_img = pygame.image.load(os.path.join('img', 'Right_mario_jump.jpg')).convert()
Left_mario_jump_img = pygame.image.load(os.path.join('img', 'Left_mario_jump.jpg')).convert()
enemy1_img = pygame.image.load(os.path.join('img', 'Left_enemy.png')).convert()
enemy2_img = pygame.image.load(os.path.join('img', 'Right_enemy.png')).convert()
Right_flying_turtle = pygame.image.load(os.path.join('img', 'Right_flying_turtle.png')).convert()
Left_flying_turtle = pygame.image.load(os.path.join('img', 'Left_flying_turtle.png')).convert()
background = pygame.image.load(os.path.join('img', 'background.png')).convert()
background = pygame.transform.scale(background, (3000, HEIGHT))
coin_img = pygame.image.load(os.path.join('img', 'coin.png')).convert()
flag_img = pygame.image.load(os.path.join('img', 'mario_flag.png')).convert()
gold_brick_img = pygame.image.load(os.path.join('img', 'gold_brick.png')).convert()

# Sounds
eatcoin_sound = pygame.mixer.Sound(os.path.join('sound', 'eatcoin.wav'))
gameover_sound = pygame.mixer.Sound(os.path.join('sound', 'gameover.ogg'))
jump_sound = pygame.mixer.Sound(os.path.join('sound', 'jump.ogg'))
pygame.mixer.music.load(os.path.join('sound', 'background.ogg'))

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def darken_screen():
    dark_img = screen.convert_alpha()
    for opacity in range(0, 255, 15):
        clock.tick(FPS)
        dark_img.fill((*BLACK, opacity))
        screen.blit(dark_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(100)

def show_game_over():
    gameover_sound.play()
    pygame.time.delay(500)
    font = pygame.font.SysFont(None, 74)
    text = font.render('GAME OVER', True, BLACK)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)

class Coin(pygame.sprite.Sprite):
    def __init__(self, type, coin_num, coin_start):
        super().__init__()
        self.image = pygame.transform.scale(coin_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.coin_start = coin_start
        if type == 1:
            self.rect.y = GROUND_LEVEL
        else:
            self.rect.y = GROUND_LEVEL - 250
        self.rect.x = coin_start + coin_num * 80
        self.coin_num = coin_num

    def update(self):
        if self.rect.x <= 0 or self.rect.x >= 3000:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(Right_mario_img, (55, 62))
        self.image_right.set_colorkey(BLACK)
        self.image_left = pygame.transform.scale(Left_mario_img, (55, 62))
        self.image_left.set_colorkey(BLACK)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL+5
        self.rect.x = 10
        self.speed = 5
        self.jump_speed = 10
        self.vel_y = 0
        self.on_ground = True

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            if self.rect.x < -50:
                show_game_over()
                pygame.mixer.stop()
                pygame.quit()
            self.rect.x -= self.speed
            self.image = self.image_left
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = self.image_right
        if keys[pygame.K_UP] and self.on_ground:
            jump_sound.play()
            if self.image == self.image_right:
                self.image = pygame.transform.scale(Right_mario_jump_img, (55, 62))
            else:
                self.image = pygame.transform.scale(Left_mario_jump_img, (55, 62))
            self.image.set_colorkey(WHITE)
            self.vel_y = -self.jump_speed
            self.on_ground = False

        if not self.on_ground:
            self.vel_y += GRAVITY
            self.rect.y += self.vel_y
            if self.rect.y > GROUND_LEVEL:
                self.rect.y = GROUND_LEVEL
                self.on_ground = True
                self.vel_y = 0
                if self.image == self.image_right:
                    self.image = pygame.transform.scale(Right_mario_img, (55, 62))
                else:
                    self.image = pygame.transform.scale(Left_mario_img, (55, 62))
                self.image.set_colorkey(BLACK)

        if keys[pygame.K_DOWN]:
            if self.rect.y > GROUND_LEVEL:
                self.rect.y = GROUND_LEVEL
            self.rect.y += self.speed

        if self.rect.left > 2900:
            darken_screen()
            self.rect.right = 90

        self.collide_with_bricks()

    def collide_with_bricks(self):
        collisions = pygame.sprite.spritecollide(self, gold_bricks, False)
        for brick in collisions:
            if self.vel_y > 0:  # Falling down
                self.rect.bottom = brick.rect.top
                self.vel_y = 0
            elif self.vel_y < 0:  # Jumping up
                self.rect.top = brick.rect.bottom
                self.vel_y = 0
                # Generate coin above the brick and play sound
                coin = Coin(1, 0, brick.rect.x)
                coin.rect.y = brick.rect.y - 150  # Slightly above the brick
                all_sprites.add(coin)
                coins.add(coin)
                eatcoin_sound.play()
            else:  # Horizontal collision
                if self.rect.right > brick.rect.left and self.rect.left < brick.rect.right:
                    if self.rect.right == brick.rect.left:
                        self.rect.right = brick.rect.left
                    if self.rect.left == brick.rect.right:
                        self.rect.left = brick.rect.right



class Enemy1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(enemy2_img, (40, 40))
        self.image_right.set_colorkey(BLACK)
        self.image_left = pygame.transform.scale(enemy1_img, (40, 40))
        self.image_left.set_colorkey(BLACK)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL + 20
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.speed = 2
        self.direction = -1
        self.left_bound = self.rect.x - 100
        self.right_bound = self.rect.x + 100

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.direction == 1:
            self.image = self.image_right
        else:
            self.image = self.image_left

        if self.rect.right >= self.right_bound or self.rect.left <= self.left_bound:
            self.direction *= -1

class Enemy2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(enemy2_img, (40, 40))
        self.image_right.set_colorkey(BLACK)
        self.image_left = pygame.transform.scale(enemy1_img, (40, 40))
        self.image_left.set_colorkey(BLACK)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL + 20
        self.rect.x = WIDTH - self.rect.width - 100
        self.speed = 3
        self.direction = -1
        self.left_bound = self.rect.x - 50
        self.right_bound = self.rect.x + 50

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.direction == 1:
            self.image = self.image_right
        else:
            self.image = self.image_left

        if self.rect.right >= self.right_bound or self.rect.left <= self.left_bound:
            self.direction *= -1
class Enemy3(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(enemy2_img, (40, 40))
        self.image_right.set_colorkey(BLACK)
        self.image_left = pygame.transform.scale(enemy1_img, (40, 40))
        self.image_left.set_colorkey(BLACK)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL + 20
        self.rect.x = WIDTH//2  #plact it to the middle of background
        self.speed = 3
        self.direction = -1
        self.left_bound = self.rect.x - 200
        self.right_bound = self.rect.x + 200

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.direction == 1:
            self.image = self.image_right
        else:
            self.image = self.image_left

        if self.rect.right >= self.right_bound or self.rect.left <= self.left_bound:
            self.direction *= -1

class FlyingTurtle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(Right_flying_turtle, (55, 62))
        self.image_right.set_colorkey(BLACK)
        self.image_left = pygame.transform.scale(Left_flying_turtle, (55, 62))
        self.image_left.set_colorkey(BLACK)
        self.image = self.image_right
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL - 90
        self.rect.x = WIDTH // 2 - self.rect.width // 2
        self.speed = 2
        self.direction = -1
        self.left_bound = self.rect.x - 400
        self.right_bound = self.rect.x + 400

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.direction == 1:
            self.image = self.image_right
        else:
            self.image = self.image_left

        if self.rect.right >= self.right_bound or self.rect.left <= self.left_bound:
            self.direction *= -1

class Flag(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(flag_img, (131, 300))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL - 230
        self.rect.x = 2900


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

def get_block(width, height, scale=1.5):
    path = join('img', 'brick_with_grass_resized.png')  # size = 64, 54
    img = pygame.image.load(path).convert_alpha()
    img.set_colorkey((255, 255, 255))
    
    # Resize the image
    new_height = int(height * scale)
    new_width = width  # Assuming we only scale the height
    resized_img = pygame.transform.scale(img, (new_width, new_height))
    
    surface = pygame.Surface((new_width, new_height), pygame.SRCALPHA, 32)
    surface.blit(resized_img, (0, 0))
    surface.set_colorkey((255, 255, 255))  # Set the colorkey again after resizing
    return surface

class Block(Object):
    def __init__(self, x, y, width, height, scale=1.5, name=None):
        super().__init__(x, y, width, int(height * scale), name)
        block = get_block(width, height, scale)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

# Constants
WIDTH, HEIGHT = 800, 600  # Set your screen width and height
block_width, block_height = 64, 54  # Original block dimensions
scale = 1.5  # Scale factor

# Create the floor
floor = [
    Block(i * block_width, HEIGHT - int(block_height * scale), block_width, block_height, scale)
    for i in range(-WIDTH // block_width, (WIDTH * 4) // block_width)
]
# Create sprite group and player instance

class GoldBrick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(gold_brick_img, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create sprite groups

all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()

terrain = pygame.sprite.Group()
all_sprites.add(floor)

gold_bricks = pygame.sprite.Group()


# Create flag
flag = Flag()
all_sprites.add(flag)

# Create enemies
enemy1 = Enemy1()
enemy2 = Enemy2()
enemy3 = Enemy3()
flying_turtle = FlyingTurtle()
all_sprites.add(enemy1)
all_sprites.add(enemy2)
all_sprites.add(enemy3)
all_sprites.add(flying_turtle)
all_sprites.add(gold_bricks)
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)
enemies.add(flying_turtle)

# Create player
player = Player()
all_sprites.add(player)
players.add(player)

# Create coins
def create_coin(existing_end_positions):
    type_num = random.randint(1, 2)
    coin_num = random.randint(1, 10)
    if existing_end_positions:
        coin_start = max(existing_end_positions) + random.randint(50, 150)
    else:
        coin_start = random.randrange(0, WIDTH - 200)

    coin_end = coin_start + coin_num * 80

    for i in range(coin_num):
        coin = Coin(type_num, i + 1, coin_start)
        all_sprites.add(coin)
        coins.add(coin)
    return coin_end

coin_end_positions = []
for i in range(5):
    coin_end_positions.append(create_coin(coin_end_positions))

# Create gold bricks
num_bricks = 10
for i in range(num_bricks):
    x = (i + 1) * (3000 // (num_bricks + 1))
    y = GROUND_LEVEL - 100
    brick = GoldBrick(x, y)
    all_sprites.add(brick)
    gold_bricks.add(brick)

score = 0
camera_offset = pygame.Vector2(0, 0)

# Main game loop
# Main game loop
running = True
game_over = False
pygame.mixer.music.play(-1)
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        all_sprites.update()

        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True
            show_game_over()
            running = False

    eat_coin = pygame.sprite.groupcollide(players, coins, False, True)

    for eat in eat_coin:
        eatcoin_sound.play()
        score += 1
        print(score)

    camera_offset.x = player.rect.centerx - WIDTH / 2
    camera_offset.y = 0

    screen.fill((93, 147, 253))
    screen.blit(background, (-camera_offset.x, -camera_offset.y))

    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect.topleft - camera_offset)

    draw_text(screen, 'score is: ' + str(score), 18, WIDTH / 2, 10)
    pygame.display.update()

pygame.mixer.stop()
pygame.quit()