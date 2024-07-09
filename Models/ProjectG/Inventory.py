import pygame

from Models.ProjectG.Weapon.MainWeapon.New_Sword import New_Sword
from Models.ProjectG.Weapon.MainWeapon.Sword import Sword


class Inventory:
    def __init__(self, player, screen):
        self.last_pos_mouse = (0,0)
        self.player = player
        # [Laser(), Lightning(),Saw(),magic_staff(),Star(),Scythe(), Bomb()]
        self.weapons = []
        self.screen = screen
        self.enemy_targeted = None

    def add_weapon(self, weapon):
        self.weapons.append(weapon)

    def set_enemy(self, enemy):
        self.enemy_targeted = enemy

    def update(self):
        for item in self.weapons:
            if not isinstance(item, New_Sword):
                item.update(self.player, self.enemy_targeted)
            elif item.is_swinging:
                item.update(self.player, self.last_pos_mouse)

            if item.show_image:
                item.projectile.draw(self.screen)

    def start_swing(self):
        for item in self.weapons:
            if isinstance(item, New_Sword):
                item.is_swinging = True
                self.last_pos_mouse = pygame.mouse.get_pos()
