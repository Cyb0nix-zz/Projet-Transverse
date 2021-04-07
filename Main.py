import pygame, sys
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()

WINDOW_SIZE = (1280, 720)

screen = pygame.display.set_mode(WINDOW_SIZE)

display = pygame.Surface((1000, 544))

pygame.display.set_caption("The Shadow of the past")

player_img = pygame.image.load('Caracter/player.png')
background = pygame.image.load('textures/Background/Map_ville.png')

wall_block = pygame.image.load('textures/wall_building.png')
windows_block = pygame.image.load('textures/building_night_light_on.png')
TILE_SIZE = windows_block.get_width()

true_scroll = [0, 0]


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


game_map = load_map('map')


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


move_right = False
move_left = False

player_y_momentum = 0
air_timer = 0

player_box = pygame.Rect(400, 500, player_img.get_width(), player_img.get_height()-10)
test_rect = pygame.Rect(100, 100, 100, 50)

while True:
    display.fill((146, 244, 255))

    true_scroll[0] += (player_box.x - true_scroll[0] - 400) / 20
    true_scroll[1] += (player_box.y - true_scroll[1] - 390) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    display.blit(background, (0 - scroll[0] * 0.15, -250 - scroll[1] * 0.15))

    tile_rects = []
    y = 0

    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(wall_block, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(windows_block, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1

    player_movement = [0, 0]

    if move_right:
        player_movement[0] += 3
    if move_left:
        player_movement[0] -= 3
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.5
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_box, collisions = move(player_box, player_movement, tile_rects)
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_img, (player_box.x - scroll[0], player_box.y - scroll[1]))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                move_right = True
            if event.key == K_LEFT:
                move_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -10
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                move_right = False
            if event.key == K_LEFT:
                move_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(240)
