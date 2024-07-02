import pygame

from Models.ProjectG.Weapon.Projectile.LaserProjectile import LaserProjectile
from Models.ProjectG.Weapon.Weapon import Weapon


class Laser(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Laser"
        self.current_length = 0
        self.damage = 10
        self.max_length = 200
        self.growth_rate = 3
        self.width = 10
        self.image = pygame.Surface((self.current_length, self.width), pygame.SRCALPHA)
        self.original_image = self.image
        self.delete_on_hit = False
        self.cooldown = 7000
        self.projectile = pygame.sprite.Group()
        self.max_projectile = 1
        self.rotation_speed = 0.05
        self.max_turn = 4
        self.next_upgrade = "Un laser grandit vers l'ennemi le plus proche"
        self.ico = self.image

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if (now - self.last_fire >= self.cooldown and len(self.projectile) < self.max_projectile) or self.last_fire == 0:
                self.last_fire = pygame.time.get_ticks()
                self.projectile.add(
                    LaserProjectile(player.rect.centerx, player.rect.centery, enemy, self, player))

    def update(self, player, enemy):
        self.fire(player, enemy)

        self.projectile.update()