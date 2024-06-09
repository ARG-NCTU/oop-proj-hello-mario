import pygame
import os

FPS = 60
WIDTH, HEIGHT = 800, 600  # screen size
GRAVITY = 0.5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# INITIALIZE PYGAME
pygame.init()
pygame.mixer.init()  # Initialize the mixer for sound
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Group 5 Final Project')
clock = pygame.time.Clock()
GROUND_LEVEL = HEIGHT - 140

# Load images
Right_mario_img = pygame.image.load(os.path.join('img', 'Right_mario1.png')).convert()
Left_mario_img = pygame.image.load(os.path.join('img', 'Left_mario1.png')).convert()
Right_mario_jump_img = pygame.image.load(os.path.join('img', 'Right_mario_jump.jpg')).convert()
Left_mario_jump_img = pygame.image.load(os.path.join('img', 'Left_mario_jump.jpg')).convert()
enemy1_img = pygame.image.load(os.path.join('img', 'Left_enemy.png')).convert()
enemy2_img = pygame.image.load(os.path.join('img', 'Right_enemy.png')).convert()
Right_flying_turtle=pygame.image.load(os.path.join('img', 'Right_flying_turtle.png')).convert()
Left_flying_turtle=pygame.image.load(os.path.join('img', 'Left_flying_turtle.png')).convert()
background = pygame.image.load(os.path.join('img', 'background.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
# Load sounds
gameover_sound = pygame.mixer.Sound(os.path.join('sound', 'gameover.ogg'))
jump_sound = pygame.mixer.Sound(os.path.join('sound', 'jump.ogg'))  # Load jump sound
pygame.mixer.music.load(os.path.join('sound', 'background.ogg'))

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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_right = pygame.transform.scale(Right_mario_img, (55, 62))
        self.image_right.set_colorkey(BLACK)
        self.image_left = pygame.transform.scale(Left_mario_img, (55, 62))
        self.image_left.set_colorkey(BLACK)
        self.image = self.image_right  # Initial image set to right
        self.rect = self.image.get_rect()
        self.rect.y = GROUND_LEVEL  # initial y position
        self.rect.x = 10
        self.speed = 5
        self.jump_speed = 10
        self.vel_y = 0  # initial vertical velocity
        self.on_ground = True  # initialize jump to false

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.image = self.image_left
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.image = self.image_right
        if keys[pygame.K_UP] and self.on_ground:  # if on ground and up key is pressed
            # Play jump sound
            jump_sound.play()
            # image jumps
            if self.image == self.image_right:
                self.image = pygame.transform.scale(Right_mario_jump_img, (55, 62))  # import jump image
            else:
                self.image = pygame.transform.scale(Left_mario_jump_img, (55, 62))  # import jump image
            self.image.set_colorkey(WHITE)  # set white background to transparent
            self.vel_y = -self.jump_speed
            self.on_ground = False

        # gravity
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
                self.image.set_colorkey(BLACK)  # set black background to transparent

        if keys[pygame.K_DOWN] and self.on_ground:
            self.rect.y += self.speed

        # Limit Mario's movement within the screen
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - self.rect.width:
            self.rect.x = WIDTH - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > GROUND_LEVEL:
            self.rect.y = GROUND_LEVEL

        if self.rect.left > WIDTH:
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

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create initial enemy
enemy1 = Enemy1()
flying_turtle = FlyingTurtle()
all_sprites.add(enemy1)
all_sprites.add(flying_turtle)
enemies.add(enemy1)

# Main game loop
running = True
pygame.mixer.music.play(-1)  # Loop infinitely

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

    # Display
    screen.fill(WHITE)
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)  # Draw the group

    pygame.display.update()

pygame.mixer.music.stop()
pygame.quit()
