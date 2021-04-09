import pygame, sys
from pygame.locals import *


class player:

    def __init__(self):
        self.player_img = pygame.image.load('Caracter/player.png')
        self.player_box = pygame.Rect(0, 0, self.player_img.get_width(), self.player_img.get_height() - 10)

    def setLocation(self, x, y):
        self.player_box.y = y
        self.player_box.x = x

    def move(self, movement, tile_rects):
        self.movement = movement
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.tiles = tile_rects

        self.player_box.x += self.movement[0]

        hit_list = []
        for tile in self.tiles:
            if self.player_box.colliderect(tile):
                hit_list.append(tile)

        for tile in hit_list:
            if self.movement[0] > 0:
                self.player_box.right = tile.left
                self.collision_types['right'] = True
            elif self.movement[0] < 0:
                self.player_box.left = tile.right
                self.collision_types['left'] = True

        self.player_box.y += self.movement[1]

        for tile in self.tiles:
            if self.player_box.colliderect(tile):
                hit_list.append(tile)

        for tile in hit_list:
            if self.movement[1] > 0:
                self.player_box.bottom = tile.top
                self.collision_types['bottom'] = True
            elif self.movement[1] < 0:
                self.player_box.top = tile.bottom
                self.collision_types['top'] = True

    def update(self, display, scroll):

        display.blit(self.player_img, (self.player_box.x - scroll[0], self.player_box.y - scroll[1]))
