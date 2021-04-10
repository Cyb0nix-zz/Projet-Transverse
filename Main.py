import pygame, sys
from pygame.locals import *
from Class import *

WINDOW_SIZE = (1280, 720)
TILE_SIZE = 32

clock = pygame.time.Clock()

pygame.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface((1280, 704))
pygame.display.set_caption("The Shadow of the past")

map = Map("map", display, TILE_SIZE)

player = Player("Cybonix", 20, 5)
player.setLocation(400, 500)

true_scroll = [0, 0]
move_right = False
move_left = False
player_y_momentum = 0
air_timer = 0
ennemi_groupe = pygame.sprite.Group()
ennemi_groupe = map.set_mobs(ennemi_groupe)
bullet_groupe = pygame.sprite.Group()

while True:

    true_scroll[0] += (player.player_box.x - true_scroll[0] - 400) / 20
    true_scroll[1] += (player.player_box.y - true_scroll[1] - 555) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    tile_rects = map.update(scroll)

    player_movement = [0, 0]

    if move_right:
        player_movement[0] += 3
    if move_left:
        player_movement[0] -= 3
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.6
    if player_y_momentum > 3:
        player_y_momentum = 3

    player.move(player_movement, tile_rects)
    if player.collision_types['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    bullet_groupe.update(display, scroll, tile_rects, ennemi_groupe, player)
    player.update(display, scroll)
    ennemi_groupe.update(display, scroll, tile_rects,player,bullet_groupe)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullet_groupe.add(player.shoot(WINDOW_SIZE))

        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                move_right = True
            if event.key == K_LEFT:
                move_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    player_y_momentum = -7
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                move_right = False
            if event.key == K_LEFT:
                move_left = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(120)
