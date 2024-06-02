import pygame
import os

FPS = 60
WIDTH, HEIGHT = 800, 600  # screen size
GRAVITY = 0.5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# INITIALIZE PYGAME
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Group 5 Final Project')
clock = pygame.time.Clock()
GROUND_LEVEL = HEIGHT - 140

# Load images
mario_img = pygame.image.load(os.path.join('img', 'mario1.png')).convert()
mario_jump_img = pygame.image.load(os.path.join('img', 'mario_jump.jpg')).convert()
background = pygame.image.load(os.path.join('img', 'background.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Transition of the screen
def darken_screen():
    dark_img = screen.convert_alpha()
    for opacity in range(0, 255, 15):
        clock.tick(FPS)
        dark_img.fill((*BLACK, opacity))
        screen.blit(dark_img, (0, 0))
        pygame.display.update()
        pygame.time.delay(100)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(mario_img, (120, 62))  # import image
        self.image.set_colorkey(BLACK)  # set black background to transparent
        self.rect = self.image.get_rect()  # get rectangle of image
        self.rect.y = GROUND_LEVEL  # get rectangle of image
        self.rect.x = 10
        self.speed = 5
        self.jump_speed = 10
        self.vel_y = 0  # initial vertical velocity
        self.on_ground = True  # initialize jump to false

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.on_ground:  # if on ground and up key is pressed
            # image jumps
            self.image = pygame.transform.scale(mario_jump_img, (55, 62))  # import jump image
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
                self.image = pygame.transform.scale(mario_img, (120, 62))  # import original image
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
        if self.rect.y > HEIGHT - self.rect.height:
            self.rect.y = HEIGHT - self.rect.height

        if self.rect.left > WIDTH:
            darken_screen()
            self.rect.right = 90

all_sprites = pygame.sprite.Group()
player = Player()
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
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)  # Draw the group

    pygame.display.update()

pygame.quit()
