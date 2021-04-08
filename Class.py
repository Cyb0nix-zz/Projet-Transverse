import pygame, sys
from pygame.locals import *


class player:

    def __init__(self, screen, tile_rects):
        self.player_img = pygame.image.load('Caracter/player.png')
        self.movement = [0,0]
        self.tiles = tile_rects


    def setLocation(self,x,y):
        self.player_box = pygame.Rect(x, y, self.player_img.get_width(), self.player_img.get_height() - 10)

    def move(self):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        self.player_box.x += self.movement[0]

        hit_list = []
        for tile in self.tiles:
            if self.player_box.colliderect(tile):
                hit_list.append(tile)

        for tile in hit_list:
            if self.movement[0] > 0:
                self.player_box.right = tile.left
                collision_types['right'] = True
            elif self.movement[0] < 0:
                self.player_box.left = tile.right
                collision_types['left'] = True
        self.player_box.y += self.movement[1]

        for tile in self.tiles:
            if self.player_box.colliderect(tile):
                hit_list.append(tile)

        for tile in hit_list:
            if self.movement[1] > 0:
                self.player_box.bottom = tile.top
                collision_types['bottom'] = True
            elif self.movement[1] < 0:
                self.player_box.top = tile.bottom
                collision_types['top'] = True
