import pygame

from Models.ProjectG.Weapon.Projectile import Projectile


class magic_staff(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 8
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/fireball.png").convert_alpha(),(60, 60))
        self.damage = 10
        self.rect = self.image.get_rect(center=(100,100))
        self.cooldown = 400
        self.last_fire = 0
        self.projectile = pygame.sprite.Group()

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown:
                self.last_fire = pygame.time.get_ticks()
                self.projectile.add(Projectile(player.rect.centerx,  player.rect.centery, enemy.rect.centerx, enemy.rect.centery, self.speed, self.image, self.damage))

    def update(self, player, enemy):
        self.fire(player, enemy)
        self.projectile.update()
