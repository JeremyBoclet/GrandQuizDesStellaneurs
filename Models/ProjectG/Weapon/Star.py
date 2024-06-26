import random

import pygame

from Models.ProjectG.Weapon.Projectile.Projectile import Projectile
from Models.ProjectG.Weapon.Weapon import Weapon

WIDTH = 1920
HEIGHT = 1080


class Star(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Etoiles"

        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/star.png").convert_alpha(),
                                            (45, 45))
        self.damage = 10
        self.max_bounce = 7
        self.cooldown = 1000
        self.speed = 10
        self.delete_on_hit = False
        self.rect = self.image.get_rect(center=(100, 100))
        self.projectile = pygame.sprite.Group()
        self.angle = 0
        self.rotation_speed = 0
        self.original_image = self.image
        self.max_projectile = 1

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown or self.last_fire == 0:
                self.last_fire = pygame.time.get_ticks()
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)

                if len(self.projectile) < self.max_projectile:
                    self.projectile.add(
                        Projectile(player.rect.centerx, player.rect.centery, x,y,
                                   self, player, can_bounce=True))

    def update(self, player, enemy):
        self.fire(player, enemy)

        self.projectile.update()
