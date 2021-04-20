import pygame
from math import *
from pygame import *


class Map():
    def __init__(self, path, screen, TILE_SIZE):
        self.TILE_SIZE = TILE_SIZE
        self.screen = screen
        self.path = path
        self.background = pygame.image.load('textures/Background/Map_ville.png')
        self.wall_block = pygame.image.load('textures/wall_building.png')
        self.windows_block = pygame.image.load('textures/building_night_light_on.png')

        f = open(path + '.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        self.game_map = []
        for row in data:
            self.game_map.append(list(row))

    def set_mobs(self, ennemi_groupe):
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == '5':
                    ennemi_groupe.add(Ennemi(20, 2, x * self.TILE_SIZE, y * self.TILE_SIZE))
                x += 1
            y += 1
        return ennemi_groupe

    def update(self, scroll):
        self.screen.fill((146, 244, 255))
        self.screen.blit(self.background, (0 - scroll[0] * 0.15, -200 - scroll[1] * 0.15))
        self.tile_rects = []
        y = 0
        for row in self.game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    self.screen.blit(self.wall_block, (x * self.TILE_SIZE - scroll[0], y * self.TILE_SIZE - scroll[1]))
                if tile == '2':
                    self.screen.blit(self.windows_block,
                                     (x * self.TILE_SIZE - scroll[0], y * self.TILE_SIZE - scroll[1]))
                if tile != '0' and tile != '5':
                    self.tile_rects.append(
                        pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE))
                x += 1
            y += 1

        return self.tile_rects


class Animations():

    def __init__(self):
        global animation_frames
        self.animation_frames = {}

    def load_animation(self, path, frame_durations):
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = animation_name + '_' + str(n)
            img_loc = path + "/" + animation_frame_id + '.png'
            animation_image = pygame.image.load(img_loc)
            self.animation_frames[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1
        return animation_frame_data

    def change_action(self, action_var, frame, new_value):
        if action_var != new_value:
            action_var = new_value
            frame = 0
        return action_var, frame


class Player(pygame.sprite.Sprite):

    def __init__(self, pseudo, health, lives, attack, nbr_grenade):
        super().__init__()
        self.player_img = pygame.image.load('Characters/Player/idle/idle_0.png')
        self.heart = pygame.image.load('Assets/life.gif')
        self.shoot_sound = pygame.mixer.Sound('Assets/Sounds/tir.wav')
        self.shoot_sound.set_volume(0.01)
        self.grenade_img = pygame.image.load('Assets/grenade/grenade_0.png')
        self.player_box = self.player_img.get_rect()
        self.pseudo = pseudo
        self.health = health
        self.health_bar_under = pygame.Surface((20, 2))
        self.attack = attack
        self.lives = lives
        self.nbr_grenade = nbr_grenade
        self.weapon = None
        self.armor = 5

    def setLocation(self, x, y):
        self.player_box.y = y
        self.player_box.x = x

    def move(self, movement, tile_rects):
        self.movement = movement
        self.tiles = tile_rects
        self.collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}

        if self.player_box.x > 399:
            self.player_box.x += self.movement[0]
        else:
            self.player_box.x += 1

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

        hit_list = []
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

    def update(self, player_img, display, scroll):
        display.blit(player_img, (self.player_box.x - scroll[0], self.player_box.y - scroll[1]))

        for i in range(self.lives):
            display.blit(self.heart, (self.heart.get_width() * i + 10 + i * 5, 10))

        for i in range(self.nbr_grenade):
            display.blit(pygame.transform.scale(self.grenade_img, (108, 110)),
                         (self.heart.get_width() * i - 33 + i * 5, -5))

        if self.health < 1:
            self.health = 20
            self.lives -= 1

        if self.health > 0:
            self.health_bar = pygame.Surface((self.health, 2))
            self.health_bar.fill((0, 255, 0))
            self.health_bar_under.fill((220, 220, 220))
            display.blit(self.health_bar_under, (self.player_box.x + 5 - scroll[0], self.player_box.y - 5 - scroll[1]))
            display.blit(self.health_bar, (self.player_box.x + 5 - scroll[0], self.player_box.y - 5 - scroll[1]))

        if self.lives > 0:
            return True
        else:
            return False

    def shoot(self, display, direction):
        self.shoot_sound.play()
        if direction:
            return BulletLeft(self.player_box.x - 25, self.player_box.y, self.attack, display)
        else:
            return BulletRight(self.player_box.x + 25, self.player_box.y, self.attack, display)

    def grenade(self, display, direction, v0):
        if direction:
            self.nbr_grenade -= 1
            return GrenadeLeft(self.player_box.x, self.player_box.y, display, v0)
        else:
            self.nbr_grenade -= 1
            return GrenadeRight(self.player_box.x, self.player_box.y, display, v0)

    def get_pseudo(self):
        return self.pseudo

    def get_health(self):
        return self.health

    def get_attack_value(self):
        return self.attack

    def damage(self, damage):
        if self.armor > 0:
            self.armor -= 1

        self.health -= damage

    def refill_armor(self):
        self.armor = 5

    def get_armor_point(self):
        return self.armor

    def set_weapon(self, weapon):
        self.weapon = weapon

    def has_weapon(self):
        return self.weapon is not None


class BulletRight(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, damage, display):
        super().__init__()
        self.display = display
        self.damage = damage
        self.image = pygame.Surface((5, 2))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(pos_x + 15, pos_y + 24))

    def update(self, display, scroll, tiles, ennemi_groupe, player):

        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        self.rect.x += 25

        if self.rect.x >= 1280 + scroll[0] + 200:
            self.kill()

        for tile in tiles:
            if self.rect.colliderect(tile):
                self.kill()

        for ennemi in ennemi_groupe.sprites():
            if self.rect.colliderect(ennemi.ennemi_box):
                ennemi.damage(self.damage)
                self.kill()
        if self.rect.colliderect(player.player_box):
            player.damage(self.damage)
            self.kill()


class BulletLeft(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, damage, display):
        super().__init__()
        self.damage = damage
        self.display = display
        self.image = pygame.Surface((5, 2))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(pos_x + 15, pos_y + 24))

    def update(self, display, scroll, tiles, ennemi_groupe, player):

        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        self.rect.x -= 25

        if self.rect.x <= 0 + scroll[0] - 200:
            self.kill()

        for tile in tiles:
            if self.rect.colliderect(tile):
                self.kill()

        for ennemi in ennemi_groupe.sprites():
            if self.rect.colliderect(ennemi.ennemi_box):
                ennemi.damage(self.damage)
                self.kill()
        if self.rect.colliderect(player.player_box):
            player.damage(self.damage)
            self.kill()


class GrenadeRight(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, display, v0):
        super().__init__()
        self.display = display
        self.v0 = v0
        self.animation = Animations()
        self.animation_list = self.animation.load_animation('Assets/grenade', [5, 5, 5])
        self.explosion_sound = pygame.mixer.Sound('Assets/Sounds/explosion.wav')
        self.explosion_sound.set_volume(0.01)
        self.image_id = 0
        self.alpha = 45
        self.hit = False
        self.animation_frame = 0
        self.cpt = 1
        self.image = pygame.image.load('Assets/grenade/grenade_0.png')
        self.rect = self.image.get_rect(center=(pos_x + 40, pos_y - 25))

    def update(self, display, scroll, tiles, ennemis):
        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))

        if not self.hit:
            x = (self.v0 * cos(self.alpha)) * self.cpt
            self.rect.x += x / 11
            self.rect.y -= (((-9.8 * (x ** 2)) / (2 * (self.v0 ** 2) * (cos(self.alpha) ** 2))) + (
                    tan(self.alpha) * x)) / 11

            self.cpt += 0.5

        for tile in tiles:
            if self.rect.colliderect(tile):
                self.rect.bottom = tile.top + 20
                self.hit = True
                self.explosion_sound.play()

        if self.hit:
            self.animation_frame += 1
            if self.animation_frame < len(self.animation_list):
                self.image_id = self.animation_list[self.animation_frame]
                self.image = self.animation.animation_frames[self.image_id]
            else:
                for ennemi in ennemis:
                    if abs(self.rect.x - ennemi.ennemi_box.x) < 100:
                        ennemi.damage(10)
                self.kill()


class GrenadeLeft(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, display, v0):
        super().__init__()
        self.display = display
        self.v0 = v0
        self.animation = Animations()
        self.explosion_sound = pygame.mixer.Sound('Assets/Sounds/explosion.wav')
        self.explosion_sound.set_volume(0.01)
        self.animation_list = self.animation.load_animation('Assets/grenade', [5, 5, 5])
        self.image_id = 0
        self.hit = False
        self.animation_frame = 0
        self.alpha = 45
        self.cpt = 1
        self.image = pygame.image.load('Assets/grenade/grenade_0.png')
        self.rect = self.image.get_rect(center=(pos_x + 40, pos_y + 35))

    def update(self, display, scroll, tiles, ennemis):
        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        if not self.hit:
            x = (self.v0 * cos(self.alpha)) * self.cpt
            self.rect.x -= x / 11
            self.rect.y -= (((-9.8 * (x ** 2)) / (2 * (self.v0 ** 2) * (cos(self.alpha) ** 2))) + (
                    tan(self.alpha) * x)) / 11

            self.cpt += 0.5

        for tile in tiles:
            if self.rect.colliderect(tile):
                self.rect.bottom = tile.top + 20
                self.hit = True
                self.explosion_sound.play()
        if self.hit:
            self.animation_frame += 1
            if self.animation_frame < len(self.animation_list):
                self.image_id = self.animation_list[self.animation_frame]
                self.image = self.animation.animation_frames[self.image_id]
            else:
                for ennemi in ennemis:
                    if abs(self.rect.x - ennemi.ennemi_box.x) < 100:
                        ennemi.damage(10)
                self.kill()


class Ennemi(pygame.sprite.Sprite):
    def __init__(self, health, attack, pos_x, pos_y):
        super().__init__()
        self.ennemi_img = pygame.image.load('Characters/Ennemi/idle/idle_0.png')
        self.ennemi_box = self.ennemi_img.get_rect()
        self.ennemi_box.x = pos_x
        self.ennemi_box.y = pos_y
        self.health = health
        self.health_bar_under = pygame.Surface((20, 2))
        self.attack = attack
        self.cpt = 0
        self.shootCooldown = 0
        self.direction = -1
        self.ennemi_momentum = 0
        self.shoot_sound = pygame.mixer.Sound('Assets/Sounds/tir.wav')
        self.shoot_sound.set_volume(0.01)

    def shoot(self, display, direction):

        if direction:
            return BulletLeft(self.ennemi_box.x - 30, self.ennemi_box.y - 7, self.attack, display)
        else:
            return BulletRight(self.ennemi_box.x + 30, self.ennemi_box.y - 7, self.attack, display)

    def get_attack_value(self):
        return self.attack

    def update(self, display, scroll, tile_rects, player, bullet_groupe):
        display.blit(self.ennemi_img, (self.ennemi_box.x - scroll[0], self.ennemi_box.y - scroll[1]))
        if self.health < 1:
            self.kill()
        self.tiles = tile_rects
        if self.cpt > 240:
            self.cpt = 0
            self.direction *= -1
        if self.direction == -1:
            self.ennemi_img = pygame.transform.flip(pygame.image.load('Characters/Ennemi/idle/idle_0.png'), True, False)
            self.ennemi_box.x -= 1
        if self.direction == 1:
            self.ennemi_img = pygame.transform.flip(pygame.image.load('Characters/Ennemi/idle/idle_0.png'), False, False)
            self.ennemi_box.x += 1
        self.cpt += 1

        hit_list = []
        for tile in self.tiles:
            if self.ennemi_box.colliderect(tile):
                hit_list.append(tile)

        for tile in hit_list:
            if self.direction == 1:
                self.ennemi_box.right = tile.left
            elif self.direction == -1:
                self.ennemi_box.left = tile.right

        self.ennemi_momentum += 0.6
        if self.ennemi_momentum > 3:
            self.ennemi_momentum = 3

        self.ennemi_box.y += self.ennemi_momentum
        hit_list = []
        for tile in self.tiles:
            if self.ennemi_box.colliderect(tile):
                hit_list.append(tile)

        for tile in hit_list:
            self.ennemi_box.bottom = tile.top
            self.ennemi_momentum = 0

        self.health_bar_under.fill((220, 220, 220))
        display.blit(self.health_bar_under, (self.ennemi_box.x + 20 - scroll[0], self.ennemi_box.y - scroll[1]))

        if self.health > 0:
            self.health_bar = pygame.Surface((self.health, 2))
            self.health_bar.fill((255, 0, 0))
            display.blit(self.health_bar, (self.ennemi_box.x + 20 - scroll[0], self.ennemi_box.y - scroll[1]))

        if 400 > self.ennemi_box.x - player.player_box.x > 0:
            if self.shootCooldown == 0:
                self.shoot_sound.play()
                bullet_groupe.add(self.shoot(display, True))
                self.shootCooldown = 50

        if 0 > self.ennemi_box.x - player.player_box.x > -400:
            if self.shootCooldown == 0:
                self.shoot_sound.play()
                bullet_groupe.add(self.shoot(display, False))
                self.shootCooldown = 50
        if self.shootCooldown > 0:
            self.shootCooldown -= 1

    def damage(self, damage):

        self.health -= damage


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
