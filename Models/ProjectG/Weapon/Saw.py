import pygame.sprite

from Models.ProjectG.Weapon.Projectile import Projectile
from Models.ProjectG.Weapon.Weapon import Weapon


class Saw(Weapon):
    def __init__(self):
        pygame.sprite.Sprite().__init__()
        super().__init__()
        self.speed = 10
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/saw.png").convert_alpha(),
                                            (60, 60))
        self.damage = 2
        self.max_range = 600
        self.cooldown = 1500
        self.delete_on_hit = False
        self.last_damage_time = 0
        self.damage_cooldown = 1
        self.rect = self.image.get_rect(center=(100, 100))
        self.projectile = pygame.sprite.Group()
        self.angle = 0
        self.rotation_speed = 0.2
        self.original_image = self.image

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown:
                self.last_fire = pygame.time.get_ticks()
                self.projectile.add(
                    Projectile(player.rect.centerx, player.rect.centery, enemy.rect.centerx, enemy.rect.centery,
                               self,is_returning=True))

    def update(self, player, enemy):
        self.fire(player, enemy)

        self.projectile.update()