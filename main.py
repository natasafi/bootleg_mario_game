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

def draw(window, background, background_image):
    """Adds the backgroud image to the whole of background area"""
    for tile in background:
        window.blit(background_image, tuple(tile))  # tile contains x,y position

    pygame.display.update()


def main(window):
    """Main function which when it runs the game starts"""
    clock = pygame.time.Clock()
    background, background_image = get_background("Pink.png")

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        draw(window, background, background_image)


if __name__ == "__main__":
    main(window)
