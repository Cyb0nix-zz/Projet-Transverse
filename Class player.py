class Player:

    def __init__(self, pseudo, health, attack):
        self.pseudo = pseudo
        self.health = health
        self.attack = attack
        self.weapon = None
        self.armor = 5

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
    def refillarmor(self):
        self.armor = 5

    def get_armor_point(self):
        return self.armor

    def attack_player(self, target_player):
        damage = self.attack


        if self.has_weapon():

            damage += self.weapon.get_damage_amount()

        target_player.damage(damage)


    def set_weapon(self, weapon):
        self.weapon = weapon


    def has_weapon(self):
        return self.weapon is not None