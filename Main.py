import sys
from time import sleep
from Class import *
import csv
import os
from tkinter import messagebox
import tkinter as tk

WINDOW_SIZE = (1280, 720)
TILE_SIZE = 32
FPS = 60


clock = pygame.time.Clock()
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("The Shadow of the past")

def Menu(screen,Initiale):
    if not Initiale:
        screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("The Shadow of the past")
        pygame.display.update()
        pygame.font.init()
    # Chargement et collage du fond
    display = pygame.Surface((1280, 720))
    fond = pygame.image.load('Assets/Menu/bg_menu.png')
    display.blit(fond, (-2, 0))

    menu_music = pygame.mixer.Sound('Assets/Sounds/music.wav')
    menu_music.play()
    menu_music.set_volume(0.01)

    # Création des polices d'écriture avec différentes tailles
    title_font = pygame.font.Font('Assets/Menu/Wargate.ttf', 85)
    button_font = pygame.font.Font('Assets/Menu/Cold_Warm.otf', 40)

    # Création du texte pour le bouton jouer avec une police présente plus haut
    title = title_font.render("Shadow Of Past", False, (243, 233, 210))
    display.blit(title, (350, 80))

    # Buttons
    img_play = pygame.Surface((270, 60))
    img_play.fill((26, 126, 95))
    txt_play = button_font.render("Play", False, (243, 233, 210))
    img_play.blit(txt_play,(90,10))
    play_button = Button(500, 320, img_play, 1)

    img_editor = pygame.Surface((270, 60))
    img_editor.fill((26, 126, 95))
    txt_editor = button_font.render("Level Editor", False, (243, 233, 210))
    img_editor.blit(txt_editor, (15, 10))
    editor_button = Button(500, 400, img_editor, 1)

    play = False
    editor = False

    continuer = True
    # Boucle infinie
    while continuer:
        play = play_button.draw(display)
        editor = editor_button.draw(display)
        if play:
            menu_music.fadeout(300)
            Game(screen)
            play = False
        if editor:
            LevelEditor()
            editor = False

        for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
            if event.type == QUIT:  # Si un de ces événements est de type QUIT
                continuer = False  # On arrête la boucle

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        pygame.display.update()
        screen.blit(surf, (0, 0))
        clock.tick(FPS)


def Game(screen):
    display = pygame.Surface((1280, 704))

    map = Map(1, display, TILE_SIZE)

    animation = Animations()

    animation_database = {}

    animation_database['walk'] = animation.load_animation('Assets/Characters/Player/walk', [5, 5, 5, 5, 5, 5])
    animation_database['idle'] = animation.load_animation('Assets/Characters/Player/idle', [7, 7])
    animation_database['jump'] = animation.load_animation('Assets/Characters/Player/jump', [7, 7, 7, 7])
    animation_database['jumpold'] = animation.load_animation('Assets/Characters/Player/jumpold', [7, 7, 7, 7, 7])

    player_action = 'idle'
    player_frame = 0
    player_flip = False

    player = Player("Cybonix", 20, 4, 3, 35)
    player.setLocation(450, 600)

    true_scroll = [0, 0]
    move_right = False
    move_left = False
    player_y_momentum = 0
    v0_grenade = 30
    launch_grenade = False
    air_timer = 0
    ennemi_groupe = pygame.sprite.Group()
    ennemi_groupe = map.set_mobs(ennemi_groupe)
    bullet_groupe = pygame.sprite.Group()
    grenade_groupe = pygame.sprite.Group()
    run = True
    alive = True
    replay = False
    menu = False
    pause = False
    play = False
    while run:
        if alive and not pause:
            true_scroll[0] += (player.player_box.x - true_scroll[0] - 400) / 20
            true_scroll[1] += (player.player_box.y - true_scroll[1] - 555) / 20
            scroll = true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            tile_rects = map.update(scroll)

            player_movement = [0, 0]

            if move_right:
                player_movement[0] += 4
            if move_left:
                player_movement[0] -= 4
            player_movement[1] += player_y_momentum
            player_y_momentum += 0.8
            if player_y_momentum > 3:
                player_y_momentum = 3

            if player_movement[0] > 0 and player_movement[1] == 0:
                player_action, player_frame = animation.change_action(player_action, player_frame, 'walk')
                player_flip = False

            if player_movement[0] == 0:
                player_action, player_frame = animation.change_action(player_action, player_frame, 'idle')

            if player_movement[0] < 0 and player_movement[1] == 0:
                player_action, player_frame = animation.change_action(player_action, player_frame, 'walk')
                player_flip = True

            if player_movement[1] < 0 and player_movement[0] == 0:
                player_action, player_frame = animation.change_action(player_action, player_frame, 'jumpold')

            if player_movement[1] < 0 and player_movement[0] > 0:
                player_action, player_frame = animation.change_action(player_action, player_frame, 'jump')

            player.move(player_movement, tile_rects,map,ennemi_groupe)
            if player.collision_types['bottom']:
                player_y_momentum = 0
                air_timer = 0
            else:
                air_timer += 1

            player_frame += 1
            if player_frame >= len(animation_database[player_action]):
                player_frame = 0

            player_image_id = animation_database[player_action][player_frame]
            player_img = animation.animation_frames[player_image_id]

            bullet_groupe.update(display, scroll, tile_rects, ennemi_groupe, player)
            alive = player.update(pygame.transform.flip(player_img, player_flip, False), display, scroll)
            ennemi_groupe.update(display, scroll, tile_rects, player, bullet_groupe)
            grenade_groupe.update(display, scroll, tile_rects, ennemi_groupe)

            if launch_grenade:
                if v0_grenade < 60:
                    v0_grenade += 0.8

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 1:
                        bullet_groupe.add(player.shoot(WINDOW_SIZE, player_flip))
                    if event.button == 3:
                        if player.nbr_grenade > 0:
                            launch_grenade = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        if player.nbr_grenade > 0:
                            grenade_groupe.add(player.grenade(WINDOW_SIZE, player_flip, v0_grenade))
                            launch_grenade = False
                            v0_grenade = 30

                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        move_right = True
                    if event.key == K_LEFT:
                        move_left = True
                    if event.key == K_UP:
                        if air_timer < 6:
                            player_y_momentum = -9
                    if event.key == K_ESCAPE:
                        pause = True
                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                        move_right = False
                    if event.key == K_LEFT:
                        move_left = False
        elif not alive:
            fond = pygame.image.load('Assets/Menu/bg_menu.png')
            display.blit(fond, (-2, 0))
            title_font = pygame.font.Font('Assets/Menu/Wargate.ttf', 85)
            button_font = pygame.font.Font('Assets/Menu/Cold_Warm.otf', 40)

            title = title_font.render("Game over", False, (243, 233, 210))
            display.blit(title, (440, 150))

            img_replay = pygame.Surface((270, 60))
            img_replay.fill((26, 126, 95))
            txt_replay = button_font.render("Replay", False, (243, 233, 210))
            img_replay.blit(txt_replay, (60, 10))
            replay_button = Button(500, 320, img_replay, 1)

            img_menu = pygame.Surface((270, 60))
            img_menu.fill((26, 126, 95))
            txt_menu = button_font.render("Menu", False, (243, 233, 210))
            img_menu.blit(txt_menu, (75, 10))
            menu_button = Button(500, 400, img_menu, 1)

            replay = replay_button.draw(display)
            menu = menu_button.draw(display)
            if replay:
                Game(screen)
                replay = False
            if menu:
                menu = False
                sleep(0.1)
                Menu(screen,False)


            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                if event.type == QUIT:  # Si un de ces événements est de type QUIT
                    pygame.quit()  # On arrête la boucle

        elif pause:
            fond = pygame.image.load('Assets/Menu/bg_menu.png')
            display.blit(fond, (-2, 0))
            title_font = pygame.font.Font('Assets/Menu/Wargate.ttf', 85)
            button_font = pygame.font.Font('Assets/Menu/Cold_Warm.otf', 40)

            title = title_font.render("Pause", False, (243, 233, 210))
            display.blit(title, (520, 150))

            img_play = pygame.Surface((270, 60))
            img_play.fill((26, 126, 95))
            txt_play = button_font.render("Play", False, (243, 233, 210))
            img_play.blit(txt_play, (90, 10))
            play_button = Button(500, 320, img_play, 1)

            img_menu = pygame.Surface((270, 60))
            img_menu.fill((26, 126, 95))
            txt_menu = button_font.render("Menu", False, (243, 233, 210))
            img_menu.blit(txt_menu, (85, 10))
            menu_button = Button(500, 400, img_menu, 1)

            play = play_button.draw(display)
            menu = menu_button.draw(display)
            if play:
                pause = False
            if menu:
                menu = False
                sleep(0.1)
                Menu(screen,False)


            for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
                if event.type == QUIT:  # Si un de ces événements est de type QUIT
                    pygame.quit()  # On arrête la boucle
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pause = False

        surf = pygame.transform.scale(display, WINDOW_SIZE)
        pygame.display.update()
        screen.blit(surf, (0, 0))
        clock.tick(FPS)


def LevelEditor():


    # Taille de la fenêtre (avec taille marges)
    SIDE_MARGIN = 500
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 897


    # Variables
    ROWS = 29
    MAX_COLS = 312
    TILE_SIZE = 32
    TILE_TYPES = 76
    level = 0
    scroll_left = False
    scroll_right = False
    scroll = 0
    scroll_speed = 1
    current_tile = 0
    grid = 0

    display = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT))
    pygame.display.set_caption("The Shadow of the past Level Editor")

    # Background
    bg_0 = pygame.image.load('Assets/bg/0.png').convert_alpha()
    bg = bg_0.convert_alpha()

    # Créer les différentes tile
    img_list = []
    for x in range(TILE_TYPES):
        if x== 75:
            img = pygame.image.load(f'Assets/Tiles/{x}.png').convert_alpha()
            img_list.append(img)
        else:
            img = pygame.image.load(f'Assets/Tiles/{x}.png').convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            img_list.append(img)

    # Boutton pour sauvegarder et charger les niveaux
    save_btn = pygame.image.load('Assets/LevelEditor/save_btn.png').convert_alpha()
    load_btn = pygame.image.load('Assets/LevelEditor/load_btn.png').convert_alpha()
    grid_btn = pygame.image.load('Assets/LevelEditor/grid_btn.png').convert_alpha()
    hide_btn = pygame.image.load('Assets/LevelEditor/hide_btn.png').convert_alpha()
    trash_btn = pygame.image.load('Assets/LevelEditor/trash.png').convert_alpha()

    # Couleurs
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (144, 201, 120)

    font = pygame.font.SysFont('Futura', 30)

    # Liste vide de Tiles
    world_data = []
    for row in range(ROWS):
        r = [-1] * MAX_COLS
        world_data.append(r)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        display.blit(img, (x, y))

    # Dessiner background
    def draw_bg(bgd):
        display.fill(BLACK)
        width = bgd.get_width()
        for x in range(1):
            display.blit(bgd, ((x * width) - scroll, 0))

    # Dessiner les grid pour placer les éléments
    def draw_grid(val):
        # Ligne verticales
        if val == 1:
            for x in range(MAX_COLS + 1):
                pygame.draw.line(display, WHITE, (x * TILE_SIZE - scroll, 0), (x * TILE_SIZE - scroll, SCREEN_HEIGHT))
            # Ligne horizontales
            for y in range(ROWS + 1):
                pygame.draw.line(display, WHITE, (0, y * TILE_SIZE), (SCREEN_WIDTH, y * TILE_SIZE))
        else:
            pass

    def del_function(level):
        try:
            msgbox = messagebox.askquestion('Delete level ', 'Voulez-vous vraiment supprimer le niveau ? ',
                                            icon="warning")
            if msgbox == 'yes':
                os.remove(f'Levels/level{level}_data.txt')
            else:
                pass
        except FileNotFoundError:
            pass

    # Dessiner les tiles dans le monde
    def draw_world():
        for y, row in enumerate(world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    display.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

    # Boutons paramètres
    button_list = []
    button_col = 0
    button_row = 0

    for i in range(len(img_list)):
        tile_button = Button(SCREEN_WIDTH + (50 * button_col) + 50, 50 * button_row + 50, img_list[i], 1)
        button_list.append(tile_button)
        button_col += 1
        if button_col == 9:
            button_row += 1
            button_col = 0

    root = tk.Tk()
    root.withdraw()
    Run = True
    while Run:
        clock.tick(FPS)
        draw_text(f'{FPS}', font, WHITE, 1200, 870)
        draw_bg(bg)
        draw_world()
        draw_grid(grid)
        pygame.draw.rect(display, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
        save_button = Button(SCREEN_WIDTH + 30, 845, save_btn, 1)
        load_button = Button(SCREEN_WIDTH + 120, 845, load_btn, 1)
        hide_button = Button(SCREEN_WIDTH + 210, 845, hide_btn, 1)
        grid_button = Button(SCREEN_WIDTH + 300, 845, grid_btn, 1)
        trash_button = Button(SCREEN_WIDTH + 430, 840, trash_btn, 1)
        draw_text(f'Level: {level} ', font, WHITE, 1190, 870)
        draw_text(f'FPS:{FPS} ', font, WHITE, 1190, 830)
        if trash_button.draw(display):
            del_function(level)
        if save_button.draw(display):
            with open(f'Levels/level{level}_data.txt', 'w', newline='') as txtfile:
                writer = csv.writer(txtfile, delimiter=',')
                for row in world_data:
                    writer.writerow(row)
        if load_button.draw(display):
            scroll = 0
            try:
                with open(f'Levels/level{level}_data.txt', newline='') as txtfile:
                    reader = csv.reader(txtfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            world_data[x][y] = int(tile)
            except FileNotFoundError:
                pass
        if hide_button.draw(display):
            grid = 0
        if grid_button.draw(display):
            grid = 1
        button_count = 0
        for button_count, i in enumerate(button_list):
            if i.draw(display):
                current_tile = button_count
        rectangle = pygame.draw.rect(display, WHITE, button_list[current_tile].rect, 3)
        if scroll_left and scroll > 0:
            scroll -= 5 * scroll_speed
        if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
            scroll += 5 * scroll_speed

        pos = pygame.mouse.get_pos()
        x = (pos[0] + scroll) // TILE_SIZE
        y = pos[1] // TILE_SIZE
        if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                if world_data[y][x] != current_tile:
                    world_data[y][x] = current_tile
            if pygame.mouse.get_pressed()[2] == 1:
                world_data[y][x] = -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    level += 1
                if event.key == pygame.K_DOWN and level > -1:
                    level -= 1
                if event.key == pygame.K_LEFT:
                    scroll_left = True
                if event.key == pygame.K_RIGHT:
                    scroll_right = True
                if event.key == pygame.K_LSHIFT:
                    scroll_speed = 5
                if event.key == K_ESCAPE:
                    Run = False
                    Menu(screen,False)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    scroll_left = False
                if event.key == pygame.K_RIGHT:
                    scroll_right = False
                if event.key == pygame.K_LSHIFT:
                    scroll_speed = 1
        pygame.display.update()

    pygame.quit()

Menu(screen,True)
