import pygame
from pygame.locals import *

pygame.init()

screen_width = 1900
screen_height = 1000

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Platformer')


tile_size = 50

# Image
bg_img = pygame.image.load('bg_night.jpg')


def draw_grid():
    for line in range(0,38):
        pygame.draw.line(screen,(255,255,255),(0,line * tile_size), (screen_width, line * tile_size))
        pygame.draw.line(screen,(255,255,255),(line * tile_size,0), (line * tile_size, screen_height))

run = True
while run:

    screen.blit(bg_img, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw_grid()
    pygame.display.update()
pygame.quit()