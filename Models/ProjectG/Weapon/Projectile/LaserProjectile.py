import pygame
import math

from Models.ProjectG.Weapon.Projectile.Projectile import Projectile


class LaserProjectile(Projectile):
    def __init__(self, x, y, target, weapon, player):
        super().__init__(x, y, target.rect.centerx, target.rect.centery, weapon, player)
        self.x = x
        self.y = y
        self.target = target
        self.color = (255, 0, 0)
        self.current_length = 0
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = math.atan2(self.target.rect.centery - self.y, self.target.rect.centerx - self.x)
        self.dx = self.weapon.growth_rate * math.cos(self.angle)
        self.dy = self.weapon.growth_rate * math.sin(self.angle)
        self.turn_count = 0

    def update(self):
        self.x = self.player.rect.centerx
        self.y = self.player.rect.centery

        if self.current_length < self.weapon.max_length:
            self.current_length += self.weapon.growth_rate
            if self.current_length >= self.weapon.max_length:
                self.current_length = self.weapon.max_length
        else:
            # Une fois la taille maximale atteinte, commencer la rotation
            self.angle += self.weapon.rotation_speed
            if self.angle >= 2 * math.pi:
                self.angle -= 2 * math.pi
                self.turn_count += 1
                self.hit_enemies = []

        if self.turn_count == self.weapon.max_turn:
            self.kill()

        self.image = pygame.Surface((self.current_length, self.weapon.width), pygame.SRCALPHA)
        end_x = self.current_length * math.cos(self.angle)
        end_y = self.current_length * math.sin(self.angle)
        pygame.draw.line(self.image, self.color, (0, self.weapon.width // 2), (self.current_length, self.weapon.width // 2),
                         self.weapon.width)
        self.image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        self.rect = self.image.get_rect(center=(self.x + end_x // 2, self.y + end_y // 2))

