import pygame

from Models.ProjectG.Weapon.Projectile.FireBall import FireBall
from Models.ProjectG.Weapon.Weapon import Weapon


class magic_staff(Weapon):
    def __init__(self):
        pygame.sprite.Sprite().__init__()
        super().__init__()
        self.name = "Bâton"

        self.speed = 6
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/fireball.png").convert_alpha(),(60, 60))
        self.damage = 10
        self.rect = self.image.get_rect(center=(100,100))
        self.cooldown = 1500
        self.projectile = pygame.sprite.Group()
        self.delete_on_hit = False
        self.max_enemy_hit = 1

    def fire(self, player, enemy):
        if enemy is not None:
            now = pygame.time.get_ticks()

            # Cooldown des projectiles
            if now - self.last_fire >= self.cooldown:
                self.last_fire = pygame.time.get_ticks()
                self.projectile.add(FireBall(player.rect.centerx,  player.rect.centery, enemy, self, player))

    def update(self, player, enemy):
        self.fire(player, enemy)
        self.projectile.update()

    def set_new_level_attribute(self):
        match self.current_level:
            case 2:
                self.max_enemy_hit += 1
            case 3:
                self.speed += 1
                self.max_enemy_hit += 1
            case 4:
                self.speed += 1
            case 5:
                self.cooldown = 1500
            case 6:
                self.max_enemy_hit += 1
                self.damage += 5
