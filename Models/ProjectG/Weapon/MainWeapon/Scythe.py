import pygame

from Models.ProjectG.Weapon.Projectile.MultiScythe import MultiScythe
from Models.ProjectG.Weapon.MainWeapon.Weapon import Weapon


class Scythe(Weapon):
    def __init__(self) -> object:
        super().__init__()
        self.name = "Faux"

        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/scythe.png").convert_alpha(),
                                            (45, 45))

        self.original_image = self.image

        self.damage = 50
        self.speed = 1.5
        self.rect = self.image.get_rect(center=(100, 100))
        self.max_projectile = 1
        self.radius = 250
        self.delete_on_hit = False
        self.rotation_speed = 0.1
        self.next_upgrade = "Une faux qui tourne en orbite"
        self.ico = self.image

    def fire(self, player, enemy):
        if len(self.projectile) < self.max_projectile:
            MultiScythe(self, player, self.max_projectile)

    def update(self, player, enemy):
        self.fire(player, enemy)

        self.projectile.update()

    def set_new_level_attribute(self):
        if 1 < self.current_level < 6:
            self.max_projectile += 1
        else:
            self.speed += 0.2

        self.projectile.empty()
