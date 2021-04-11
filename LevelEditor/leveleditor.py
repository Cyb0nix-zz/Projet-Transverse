import pygame
import button
import csv
import os
from tkinter import messagebox
import tkinter as tk

pygame.init()

clock = pygame.time.Clock()
FPS = 120

# Taille de la fenêtre (avec taille marges)
SCREEN_WIDTH = 1281
SCREEN_HEIGHT = 897
LOWER_MARGIN = 100
SIDE_MARGIN = 500

# Variables
ROWS = 29
MAX_COLS = 312
TILE_SIZE = 32
TILE_TYPES = 133
level = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1
current_tile = 0
grid = 0

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT))
pygame.display.set_caption('Level editor')

# Background
bg_0 = pygame.image.load('bg/0.png').convert_alpha()
bg = bg_0.convert_alpha()

# Créer les différentes tile
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'32x32/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# Boutton pour sauvegarder et charger les niveaux
save_btn = pygame.image.load('save_btn.png').convert_alpha()
load_btn = pygame.image.load('load_btn.png').convert_alpha()
grid_btn = pygame.image.load('grid_btn.png').convert_alpha()
hide_btn = pygame.image.load('hide_btn.png').convert_alpha()
trash_btn = pygame.image.load('trash.png').convert_alpha()

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 25, 25)
GREEN = (144, 201, 120)

font = pygame.font.SysFont('Futura', 30)

# Liste vide de Tiles
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Dessiner background
def draw_bg(bgd):
    screen.fill(BLACK)
    width = bgd.get_width()
    for x in range(1):
        screen.blit(bgd, ((x * width) - scroll, 0))


# Dessiner les grid pour placer les éléments
def draw_grid(val):
    # Ligne verticales
    if val ==1:
        for x in range(MAX_COLS + 1):
            pygame.draw.line(screen, WHITE, (x * TILE_SIZE - scroll, 0), (x * TILE_SIZE - scroll, SCREEN_HEIGHT))
        # Ligne horizontales
        for y in range(ROWS + 1):
            pygame.draw.line(screen, WHITE, (0, y * TILE_SIZE), (SCREEN_WIDTH, y * TILE_SIZE))
    else:
        pass


def del_function(level):
    try:
        msgbox = messagebox.askquestion('Delete level ', 'Voulez-vous vraiment supprimer le niveau ? ', icon="warning")
        if msgbox == 'yes':
            os.remove(f'level{level}_data.csv')
        else:
            pass
    except FileNotFoundError:
        pass


# Dessiner les tiles dans le monde
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))


# Boutons paramètres
button_list = []
button_col = 0
button_row = 0

for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (50 * button_col) + 50, 50 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 9:
        button_row += 1
        button_col = 0

root = tk.Tk()
root.withdraw()
run = True
while run:
    clock.tick(FPS)
    draw_text(f'{FPS}', font, WHITE, 1200, 870)
    draw_bg(bg)
    draw_world()
    draw_grid(grid)
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    save_button = button.Button(SCREEN_WIDTH + 30, 845, save_btn, 1)
    load_button = button.Button(SCREEN_WIDTH + 120, 845, load_btn, 1)
    hide_button = button.Button(SCREEN_WIDTH + 210, 845, hide_btn, 1)
    grid_button = button.Button(SCREEN_WIDTH + 300, 845, grid_btn, 1)
    trash_button = button.Button(SCREEN_WIDTH + 430, 840, trash_btn, 1)
    draw_text(f'Level: {level} ', font, WHITE, 1190, 870)
    draw_text(f'FPS:{FPS} ', font, WHITE, 1190, 830)
    if trash_button.draw(screen):
        del_function(level)
    if save_button.draw(screen):
        with open(f'level{level}_data.txt', 'w', newline='') as txtfile:
            writer = csv.writer(txtfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen):
        scroll = 0
        try:
            with open(f'level{level}_data.txt', newline='') as txtfile:
                reader = csv.reader(txtfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
        except FileNotFoundError:
            pass
    if hide_button.draw(screen):
        grid = 0
    if grid_button.draw(screen):
        grid = 1
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    rectangle = pygame.draw.rect(screen, WHITE, button_list[current_tile].rect, 3)
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
            run = False
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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1
    pygame.display.update()
pygame.quit()
