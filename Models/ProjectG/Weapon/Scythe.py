import pygame

from Models.ProjectG.Weapon.Projectile.MultiScythe import MultiScythe
from Models.ProjectG.Weapon.Weapon import Weapon


class Scythe(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Faux"

        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/scythe.png").convert_alpha(),
                                            (45, 45))

        self.original_image = self.image

        self.damage = 5
        self.speed = 1.5
        self.rect = self.image.get_rect(center=(100, 100))
        self.projectile = pygame.sprite.Group()
        self.max_projectile = 6
        self.radius = 250
        self.delete_on_hit = False
        self.rotation_speed = 0.1

    def fire(self, player, enemy):
        if len(self.projectile) < self.max_projectile:
            MultiScythe(self, player, self.max_projectile)

    def update(self, player, enemy):
        self.fire(player, enemy)

        self.projectile.update()
