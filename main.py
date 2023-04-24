import os
import random
import math
import pygame

from os import listdir
from os.path import isfile, join


pygame.init()

pygame.display.set_caption("Bootleg Mario")

WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_VELOCITY = 5

window =  pygame.display.set_mode((WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):
    """Class which contains the properties and actions
    for the player characters of the game."""
    COLOR = (255, 0, 0)

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_velocity, self.y_velocity = 0, 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0


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
        self.y_velocity = velocity
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        """Move the character in the correct direction"""
        self.move(self.x_velocity, self.y_velocity)


    def draw_character(self, win):
        """Draws the character on the screen"""
        pygame.draw.rect(win, self.COLOR, self.rect)


def get_background(name):
    """Loads the background images"""
    image = pygame.image.load(join("background", name))
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

    player.draw_character(window)

    pygame.display.update()  # keeps the screen updated


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

        draw_tiles(window, background, background_image, player)


if __name__ == "__main__":
    main(window)
