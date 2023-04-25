"""Platform game inspired by Mario Bros."""

from os import listdir
from os.path import isfile, join

import pygame
import random
import math

pygame.init()

pygame.display.set_caption("Bootleg Mario")

WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_VELOCITY = 5

window =  pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    """Changes the rotation of the image"""
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_images(dir1, dir2, width, height, direction=False):
    """Loads all the relevant pictures we need"""
    path = join("assets", dir1, dir2)
    images = [img for img in listdir(path) if isfile(join(path, img))]

    sprites_coll = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0,0), rect)  # draw the sprite on the designated surface
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            sprites_coll[image.replace(".png", "") + "_right"] = sprites
            sprites_coll[image.replace(".png", "") + "_up"] = sprites
            sprites_coll[image.replace(".png", "") + "_down"] = sprites
            sprites_coll[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            sprites_coll[image.replace(".png", "")] = sprites
    
    return sprites_coll

class Player(pygame.sprite.Sprite):
    """Class which contains the properties and actions
    for the player characters of the game."""
    COLOUR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_images("main_characters", "PinkMan", 32, 32, True)

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_velocity, self.y_velocity = 0, 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0

    def move(self, dx, dy):
        """Determines the displacements of the character"""
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, velocity):
        """Moves to the left of the screen"""
        self.x_velocity = -velocity
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, velocity):
        """Moves to the right of the screen"""
        self.x_velocity = velocity
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def move_down(self, velocity):
        """Moves to the left of the screen"""
        self.y_velocity = velocity
        if self.direction != "down":
            self.direction = "down"
            self.animation_count = 0

    def move_up(self, velocity):
        """Moves to the right of the screen"""
        self.y_velocity = -velocity
        if self.direction != "up":
            self.direction = "up"
            self.animation_count = 0

    def loop(self, fps):
        """Move the character in the correct direction"""
        self.y_velocity += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_velocity, self.y_velocity)

        self.fall_count += 1

    def draw_sprite(self, win):
        """Draws the character on the screen"""
        self.sprite = self.SPRITES["idle_" + self.direction][0]
        win.blit(self.sprite, (self.rect.x, self.rect.y))

def get_background(name):
    """Loads the background images"""
    image = pygame.image.load(join("assets", "background", name))
    _,_, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width +1):
        for j in range(HEIGHT // height +1):
            pos = [i * width, j * height]
            tiles.append(pos)

    return tiles,image

def draw_tiles(window, background, background_image, player):
    """Adds the backgroud image to the whole of background area"""
    for tile in background:
        window.blit(background_image, tuple(tile))  # tile contains x,y position

    player.draw_sprite(window)

    pygame.display.update()  # keeps the screen updated

def handle_move(player):
    """Function to determine how to control the movement of the player"""
    keys = pygame.key.get_pressed()

    player.x_velocity = 0
    player.y_velocity = 0
    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VELOCITY)

    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VELOCITY)

    if keys[pygame.K_UP]:
        player.move_up(PLAYER_VELOCITY)
    
    if keys[pygame.K_DOWN]:
        player.move_down(PLAYER_VELOCITY)


def main(window):
    """Main function which when it runs the game starts"""
    clock = pygame.time.Clock()
    background, background_image = get_background("Green.png")

    player = Player(100, 100, 50, 50)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        handle_move(player)
        draw_tiles(window, background, background_image, player)


if __name__ == "__main__":
    main(window)
