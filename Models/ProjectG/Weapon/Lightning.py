import pygame

from Models.ProjectG.Weapon.LightningProjectile import LightningProjectile
from Models.ProjectG.Weapon.Weapon import Weapon


class Lightning(Weapon):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)# pygame.transform.scale(pygame.image.load("../Assets/ProjectG/scythe.png").convert_alpha(),(45, 45))
        self.rect = self.image.get_rect(center=(100, 100))

        self.original_image = self.image

        self.damage = 2
        self.speed = 10
        self.projectile = pygame.sprite.Group()
        self.max_projectile = 5
        self.cooldown = 1000
        self.delete_on_hit = False
        self.rotation_speed = 0
        self.max_bounce = 3

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown and len(self.projectile) < self.max_projectile:
                self.last_fire = pygame.time.get_ticks()
                self.projectile.add(
                    LightningProjectile(player.rect.centerx, player.rect.centery, enemy, self, self.max_bounce))

    def update(self, player, enemy):
        self.fire(player, enemy)

        self.projectile.update()
