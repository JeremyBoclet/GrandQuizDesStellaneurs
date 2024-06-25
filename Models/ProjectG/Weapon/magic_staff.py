import pygame

from Models.ProjectG.Weapon.Projectile import Projectile
from Models.ProjectG.Weapon.Weapon import Weapon


class magic_staff(Weapon):
    def __init__(self):
        pygame.sprite.Sprite().__init__()
        super().__init__()
        self.speed = 6
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/fireball.png").convert_alpha(),(60, 60))
        self.damage = 10
        self.rect = self.image.get_rect(center=(100,100))
        self.cooldown = 1500
        self.projectile = pygame.sprite.Group()

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown:
                self.last_fire = pygame.time.get_ticks()
                self.projectile.add(Projectile(player.rect.centerx,  player.rect.centery, enemy.rect.centerx, enemy.rect.centery, self))

    def update(self, player, enemy):
        self.fire(player, enemy)
        self.projectile.update()
