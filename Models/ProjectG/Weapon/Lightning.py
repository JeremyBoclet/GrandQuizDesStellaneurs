import pygame

from Models.ProjectG.Weapon.Projectile.LightningProjectile import LightningProjectile
from Models.ProjectG.Weapon.Weapon import Weapon


class Lightning(Weapon):
    def __init__(self):
        super().__init__()
        self.name = "Eclair"
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(100, 100))

        self.original_image = self.image

        self.damage = 10
        self.speed = 10
        self.projectile = pygame.sprite.Group()
        self.max_projectile = 1
        self.cooldown = 1000
        self.delete_on_hit = False
        self.max_bounce = 3

        self.wait_for_new_target = False

        self.animation_image_path = [f'..\Assets\ProjectG\Animation\lightning_{i}.png' for i in range(1, 4)]

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown and len(self.projectile) < self.max_projectile:
                self.last_fire = pygame.time.get_ticks()
                self.projectile.add(
                    LightningProjectile(player.rect.centerx, player.rect.centery, enemy, self, self.max_bounce))
        else:
            self.projectile.empty()

    def update(self, player, enemy):
        self.fire(player, enemy)

        self.projectile.update()

        # check si l'enemi est mort pour rerouter le projectile
        for projectile in self.projectile:
            if self.wait_for_new_target:
                projectile.reroute(enemy)
                self.wait_for_new_target = False

            if enemy.health <= 0 or projectile.target.health <= 0:
                self.wait_for_new_target = True

