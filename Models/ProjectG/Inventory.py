from Models.ProjectG.Weapon.Saw import Saw
from Models.ProjectG.Weapon.Scythe import Scythe
from Models.ProjectG.Weapon.Star import Star
from Models.ProjectG.Weapon.magic_staff import magic_staff


class Inventory:
    def __init__(self, player, screen):
        self.player = player
        self.weapons = [Scythe(), magic_staff(),Saw(), Star()]
        self.screen = screen
        self.enemy_targeted = None

    def add_weapon(self, weapon):
        self.weapons.append(weapon)

    def set_enemy(self,enemy):
        self.enemy_targeted = enemy
        # enemy.is_targeted = True

    def update(self):
        for item in self.weapons:
            item.update(self.player, self.enemy_targeted)
            item.projectile.draw(self.screen)

