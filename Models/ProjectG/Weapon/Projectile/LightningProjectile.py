import pygame
import math

from Models.ProjectG.Animation.ElectricAnimation import ElectricAnimation
from Models.ProjectG.Weapon.Projectile.Projectile import Projectile


class LightningProjectile(Projectile):
    def __init__(self, x, y, target, weapon, max_bounces):
        super().__init__(x, y, target.rect.centerx, target.rect.centery, weapon, None)
        self.image = weapon.image
        pygame.draw.circle(self.image, (255, 255, 0), (5, 5), 5)  # Dessiner un cercle pour le projectile
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = weapon.speed
        self.max_bounces = max_bounces
        self.bounces = 0
        self.target = target

        # Calculer l'angle initial vers la cible
        self.angle = math.atan2(target.rect.centery - y, target.rect.centerx - x)
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

    def update(self):
        self.update_direction()

    def bounce(self, all_enemies):
        if self.bounces < self.max_bounces:
            self.bounces += 1
            self.damage *= 0.8  # Réduire les dégâts à chaque rebond

            # Choisir le nouvel ennemi le plus proche comme cible
            self.target = self.find_closest_enemy(self.target, all_enemies)
            if not self.target:
                self.weapon.last_fire = pygame.time.get_ticks()
                self.kill()
            else:
                self.update_direction()

        else:
            self.weapon.last_fire = pygame.time.get_ticks()
            self.kill()

    def find_closest_enemy(self, current_enemy, all_enemies):
        closest_enemy = None
        closest_distance = float('inf')
        for enemy in all_enemies:

            if enemy == current_enemy or enemy in self.hit_enemies:
                continue
            distance = math.hypot(enemy.rect.centerx - self.rect.centerx, enemy.rect.centery - self.rect.centery)
            if distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance

        return closest_enemy

    def update_direction(self):
        # Calculer la direction vers le joueur
        self.angle = math.atan2(self.target.rect.centery - self.rect.centery,
                                self.target.rect.centerx - self.rect.centerx)
        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

        self.rect.x += self.dx
        self.rect.y += self.dy

    def reroute(self,enemy):
        self.target = enemy
        self.update_direction()

    def trigger_electric_animation(self, position, all_sprites):
        animation = ElectricAnimation(position, self.weapon.animation_image_path)
        all_sprites.add(animation)
