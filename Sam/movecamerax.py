import pygame
import os

# Constants
FPS = 60
WIDTH, HEIGHT = 1500, 900  # Screen size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Group 5 Final Project')
clock = pygame.time.Clock()

# Load images
mario_jpg = pygame.image.load(os.path.join('img', 'mario.jpg')).convert()
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
        self.image = pygame.transform.scale(mario_jpg, (120, 62))  # Import image
        self.image.set_colorkey(WHITE)  # Set white background to transparent
        self.rect = self.image.get_rect()  # Get rectangle of image
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
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

# Create sprite group and player instance
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

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

    # Update camera offset based on player movement
    camera_offset.x = player.rect.centerx - WIDTH / 2
 #   camera_offset.y = player.rect.centery - HEIGHT / 2 # Camera also moves in y direction
    camera_offset.y = 0 # Camera only moves in x direction

    # Draw everything
    screen.fill(WHITE)

    # Draw background with camera offset
    screen.blit(background, (-camera_offset.x, -camera_offset.y))

    # Draw sprites with camera offset
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect.topleft - camera_offset)

    pygame.display.update()

pygame.quit()
