import pygame


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


class Player(pygame.sprite.Sprite):

    def __init__(self, pseudo, health, lives, attack):
        super().__init__()
        self.player_img = pygame.image.load('Character/player.png')
        self.heart = pygame.image.load('textures/life.gif')
        self.player_box = self.player_img.get_rect()
        self.pseudo = pseudo
        self.health = health
        self.attack = attack
        self.lives = lives
        self.weapon = None
        self.armor = 5

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

    def update(self, display, scroll):
        display.blit(self.player_img, (self.player_box.x - scroll[0], self.player_box.y - scroll[1]))

        for i in range(self.lives):
            display.blit(self.heart, (self.heart.get_width() * i + 10 + i * 5, 10))

        if self.health < 1:
            self.health = 20
            self.lives -= 1

    def shoot(self, display):
        return BulletRight(self.player_box.x + 25, self.player_box.y, self.attack, display)

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
        self.rect = self.image.get_rect(center=(pos_x + 40, pos_y + 35))

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
        self.rect = self.image.get_rect(center=(pos_x + 40, pos_y + 35))

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


class Grenade(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, display):
        super().__init__()
        self.display = display
        self.image = pygame.Surface((5, 2))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(pos_x + 40, pos_y + 35))

    def update(self, display, scroll, tiles):

        display.blit(self.image, (self.rect.x - scroll[0], self.rect.y - scroll[1]))
        self.rect.x += 25

        if self.rect.x >= self.display[0] + scroll[0] + 200:
            self.kill()

        for tile in tiles:
            if self.rect.colliderect(tile):
                self.kill()


class Ennemi(pygame.sprite.Sprite):
    def __init__(self, health, attack, pos_x, pos_y):
        super().__init__()
        self.ennemi_img = pygame.image.load('Character/ennemi.png')
        self.ennemi_box = self.ennemi_img.get_rect()
        self.ennemi_box.x = pos_x
        self.ennemi_box.y = pos_y
        self.health = health
        self.attack = attack
        self.cpt = 0
        self.shootCooldown = 0
        self.direction = -1
        self.ennemi_momentum = 0

    def shoot(self, display, direction):

        if direction == 'LEFT':
            return BulletLeft(self.ennemi_box.x - 30, self.ennemi_box.y - 7, self.attack, display)
        elif direction == 'RIGHT':
            return BulletRight(self.ennemi_box.x + 30, self.ennemi_box.y - 7, self.attack, display)

    def get_attack_value(self):
        return self.attack

    def update(self, display, scroll, tile_rects, player, bullet_groupe):

        display.blit(self.ennemi_img, (self.ennemi_box.x - scroll[0], self.ennemi_box.y - scroll[1]))
        self.tiles = tile_rects
        if self.cpt > 240:
            self.cpt = 0
            self.direction *= -1
        if self.direction == -1:
            self.ennemi_box.x -= 1
        if self.direction == 1:
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

        if self.health < 1:
            self.kill()

        if self.ennemi_box.x - player.player_box.x < 400 and self.ennemi_box.x - player.player_box.x > 0:
            if self.shootCooldown == 0:
                bullet_groupe.add(self.shoot(display, 'LEFT'))
                self.shootCooldown = 50

        if self.ennemi_box.x - player.player_box.x < 0 and self.ennemi_box.x - player.player_box.x > -400:
            if self.shootCooldown == 0:
                bullet_groupe.add(self.shoot(display, 'RIGHT'))
                self.shootCooldown = 50
        if self.shootCooldown > 0:
            self.shootCooldown -= 1

    def damage(self, damage):

        self.health -= damage
