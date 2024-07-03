import math
import random
import time

import pygame

from Models.ProjectG.Animation.Animation import Animation
from Models.ProjectG.Weapon.Projectile.Projectile import Projectile

WIDTH = 1980
HEIGHT = 1080


class BombProjectile(Projectile):
    def __init__(self, player, weapon):
        super().__init__(1, 1, 1, 1, weapon, player)
        self.weapon = weapon
        self.player = player
        self.min_distance = 200
        self.max_distance = 400

        self.start_time = time.time()
        self.image = weapon.image
        self.rect = self.image.get_rect(center=player.rect.center)

        # Définir la position cible aléatoire en s'assurant qu'elle est dans les limites de l'écran
        self.target_x, self.target_y = self.generate_target_position()

        # Paramètres de la trajectoire en arc
        self.arc_height = 150

        self.start_position = pygame.Vector2(player.rect.center)
        self.end_position = pygame.Vector2(self.target_x, self.target_y)
        self.elapsed_time = 0
        self.last_update_time = time.time()
        self.is_exploding = False
        self.explosion_started = False
        self.detonation_animation_started = False
        self.explosion_animation_started = False

    def generate_target_position(self):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(self.min_distance, self.max_distance)
        target_x = self.player.rect.centerx + distance * math.cos(angle)
        target_y = self.player.rect.centery + distance * math.sin(angle)

        # Assurer que la position cible est dans les limites de l'écran
        target_x = max(self.weapon.explosion_radius, min(target_x, WIDTH - self.weapon.explosion_radius))
        target_y = max(self.weapon.explosion_radius, min(target_y, HEIGHT - self.weapon.explosion_radius))

        self.weapon.target_indicator_rect = self.weapon.target_indicator_image.get_rect(center=(target_x, target_y))

        return target_x, target_y

    def update(self):
        current_time = time.time()
        dt = current_time - self.last_update_time
        self.last_update_time = current_time

        self.elapsed_time += dt
        t = min(self.elapsed_time / self.weapon.travel_time, 1)
        # Interpolation linéaire
        current_position = self.start_position.lerp(self.end_position, t)
        # Ajout de la hauteur de l'arc
        height = self.arc_height * (1 - (2 * t - 1) ** 2)
        self.rect.center = (current_position.x, current_position.y - height)

        if not self.explosion_started and t >= 1:
            self.explosion_started = True
            self.start_time = current_time

        if self.elapsed_time >= self.weapon.travel_time + self.weapon.explosion_delay:
            self.is_exploding = True

    def explode(self, all_enemies):
        print("Bomb exploded!")
        # Logique de dégâts en zone
        for enemy in all_enemies:
            if self.rect.centerx - self.weapon.explosion_radius <= enemy.rect.centerx <= self.rect.centerx + self.weapon.explosion_radius and \
                    self.rect.centery - self.weapon.explosion_radius <= enemy.rect.centery <= self.rect.centery + self.weapon.explosion_radius:
                enemy.take_damage(self.damage)
        self.kill()

    def draw(self, surface):
        if not self.explosion_started:
            surface.blit(self.weapon.target_indicator_image, self.weapon.target_indicator_rect)
            surface.blit(self.image, self.rect)

        # Dessiner un cercle autour de la bombe pour indiquer la portée de l'explosion
        #pygame.draw.circle(surface, (255, 0, 0), self.rect.center, self.weapon.explosion_radius, 2)

    def trigger_detonation_animation(self, position, all_sprites):
        if not self.detonation_animation_started:
            print((-(8 * 2))+24)
            self.detonation_animation_started = True
            animation = Animation(position, self.weapon.detonation_animation_image_path,
                                  frame_duration= 8 * self.weapon.explosion_delay,
                                  size=self.weapon.size)
            print(self.weapon.explosion_delay)
            all_sprites.add(animation)

    def trigger_explosion_animation(self, position, all_sprites):
        if not self.explosion_animation_started:
            self.weapon.last_fire = pygame.time.get_ticks()
            self.explosion_animation_started = True
            animation = Animation(position, self.weapon.explosion_animation_image_path, frame_duration=2,
                                  size=(self.weapon.explosion_radius * 2.2, self.weapon.explosion_radius * 2.2))
            all_sprites.add(animation)
