import pygame
import os
import random
import math
from os import listdir
from os.path import isfile, join

from pygame.sprite import Group

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 2400, 1000
FPS = 60
PLAYER_SPEED = 5

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Group 5 Final Project')

# Load images
mario_jpg = pygame.image.load(os.path.join('img', 'mario.jpg')).convert()


# Get background tiles
def get_background(name):
    image = pygame.image.load(join('img', name))
    _, _, w, h = image.get_rect()
    tiles = []
    for x in range(WIDTH // w + 1):
        for y in range(HEIGHT // h + 1):
            pos = (x * w, y * h)
            tiles.append(pos)
    return tiles, image

# Draw background tiles
def draw_background(screen, background, bg_img, player, blocks):
    for tile in background:
        screen.blit(bg_img, tile)

    for block in blocks:
        block.draw(screen)
    player.draw(screen)
    pygame.display.update()

# Player class
class Player(pygame.sprite.Sprite):
    Gravity = 1

    def __init__(self,x,y,width,height):
        super().__init__()
        self.image = pygame.transform.scale(mario_jpg, (120, 62)) 
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left" # keep track of which way the player is facing
        self.animation_count = 0    # to change animation frame
        self.fall_time = 0 # more time in air means higher falling speed

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self,vel):
        self.move(-vel, 0)
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0


    def move_right(self,vel):
        self.move(vel, 0)
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0
    
    def landed(self):
        self.y_vel = 0
        self.fall_time = 0
        self.jump_count = 0

    def hit_head(self):
        self.y_vel *= -1
        self.count = 0

    # called per while loop, to move player and handle animation
    def loop(self, fps):
        self.y_vel += min(1, (self.fall_time/fps)*self.Gravity)
        self.move(self.x_vel, self.y_vel)

        self.fall_time += 1
    
    def update(self):
        self.rect = self.image.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Pixel perfect collision
def handle_vertical_collision(player, objects,dy):
    collided_objs = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0 : 
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
            collided_objs.append(obj)
    return collided_objs

# Handle player movement
def handle_movement(player, objects):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_SPEED)
    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_SPEED)
    handle_vertical_collision(player, objects, player.y_vel)

# Terrain
class Object(pygame.sprite.Sprite):
    def __init__(self, x,y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width =  width
        self.height = height
        self.name = name

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x,self.rect.y))

def get_block(width, height):
    path = join('img','brick_with_grass_resized.png') # size = 64, 54
    img = pygame.image.load(path).convert_alpha()
    img.set_colorkey((255, 255, 255))
    surface = pygame.Surface((width,height),pygame.SRCALPHA,32)
    rect = pygame.Rect(0,0, width,height)
    surface.blit(img, (0,0),rect)
    return surface #pygame.transform.scale2x(surface)

class Block(Object):
    def __init__(self, x, y, width, height, name=None):
        super().__init__(x, y, width, height, name)
        block = get_block(width, height)
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)



# Main function
def main(screen):
    clock = pygame.time.Clock()
    background, bg_img = get_background('blue.png')
    block_width, block_height = 64, 56
    player = Player(1000, 100, 50, 50)
    floor = [Block(i*block_width,HEIGHT-block_height,block_width,block_height) for i in range(-WIDTH//block_width,(WIDTH*2)//block_width)]
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        player.loop(FPS)
        player.update()
        handle_movement(player,floor)
        draw_background(screen, background, bg_img, player, floor)   
    
    pygame.quit()

if __name__ == '__main__':
    main(screen)
