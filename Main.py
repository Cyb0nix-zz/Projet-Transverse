import pygame,sys
from pygame.locals import*

clock = pygame.time.Clock()

pygame.init()

WINDOW_SIZE = (1280,720)

screen = pygame.display.set_mode(WINDOW_SIZE)

pygame.display.set_caption("The Shadow of the past")

player_img = pygame.image.load('Caracter\player.png')
player_location = [50,50]
player_y_momentum = 0
move_right = False
move_left = False

player_box = pygame.Rect(player_location[0],player_location[1],player_img.get_width(),player_img.get_height())
test_rect = pygame.Rect(100,100,100,50)

while True:
    screen.fill((146,244,255))
    screen.blit(player_img,player_location)

    if player_location[1] > WINDOW_SIZE[1] - player_img.get_height():
        player_y_momentum = -player_y_momentum

    else:
        player_y_momentum += 0.2
    player_location[1] += player_y_momentum

    if move_right == True:
        player_location[0] += 4
    if move_left == True:
        player_location[0] -= 4

    player_box.x = player_location[0]
    player_box.y = player_location[1]

    if player_box.colliderect(test_rect):
        pygame.draw.rect(screen,(255,0,0),test_rect)
    else:
        pygame.draw.rect(screen, (0, 0, 0), test_rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                move_right = True
            if event.key == K_LEFT:
                move_left = True
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                move_right = False
            if event.key == K_LEFT:
                move_left = False


    pygame.display.update()
    clock.tick(60)








