import random

import pygame

from Models.ProjectG.Weapon.Projectile.FallingStarProjectile import FallingStarProjectile
from Models.ProjectG.Weapon.Weapon import Weapon

WIDTH = 1920
HEIGHT = 1080
class FallingStar(Weapon):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.cooldown = 2000
        self.speed = 10  # Durée de trajet en secondes
        self.damage = 2
        self.delete_on_hit = False
        self.damage_on_hit = False
        self.show_image = False
        self.animation_image_path = [f'..\Assets\ProjectG\Animation\\fallingstar\\fallingstar_{i}.png' for i in range(1, 57)]
        self.explosion_radius = 100

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown or self.last_fire == 0:
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                self.last_fire = pygame.time.get_ticks()
                for i in range(0, self.max_projectile):
                    self.projectile.add(
                       FallingStarProjectile(x, y, self))

    def update(self, player, enemy):
        self.fire(player, enemy)
        self.projectile.update()
