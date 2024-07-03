import math

import pygame
import time

from Models.ProjectG.Animation.Animation import Animation
from Models.ProjectG.Weapon.Projectile.Projectile import Projectile


class FallingStarProjectile(Projectile):
    def __init__(self, start_x, end_y, weapon):
        super().__init__(1, 1, 1, 1, weapon, None)
        self.animation_started = False
        self.damage_center = None
        self.damage_surface = None
        self.weapon = weapon
        self.image = weapon.image
        self.rect = self.image.get_rect(midtop=(start_x, 0))

        self.end_y = end_y
        self.screen_height = 1080

        self.impact_damage = weapon.damage
        self.fall_speed = weapon.speed
        self.falling = True
        self.explosion_started = False
        self.start_time = None
        self.damage_rect = None
        self.position = None

    def update(self):
        if self.falling:
            self.rotation()
            self.rect.y += self.fall_speed
            self.rect.x -= 2
            if self.rect.bottom >= self.end_y:
                self.rect.bottom = self.end_y
                self.position = (self.rect.centerx, self.rect.centery)
                self.falling = False
                self.start_time = time.time()
                self.explode()
        else:
            current_time = time.time()
            if current_time - self.start_time >= self.weapon.persistent_duration:
                self.kill()

    def explode(self):
        self.explosion_started = True
        self.create_persistent_damage_area()

    def explode_damage(self, all_enemies):
        if not self.animation_started:
            # Logique de dégâts en zone
            for enemy in all_enemies:
                if self.rect.centerx - self.weapon.explosion_radius <= enemy.rect.centerx <= self.rect.centerx + self.weapon.explosion_radius and \
                        self.rect.centery - self.weapon.explosion_radius <= enemy.rect.centery <= self.rect.centery + self.weapon.explosion_radius:
                    enemy.take_damage(self.damage)

    def create_persistent_damage_area(self):
        self.damage_surface = pygame.Surface((self.weapon.explosion_radius * 2, self.weapon.explosion_radius * 2),
                                             pygame.SRCALPHA)
        # affiche la hitbox
        pygame.draw.circle(self.damage_surface, (255, 0, 0, 128),
                           (self.weapon.explosion_radius, self.weapon.explosion_radius),
                           self.weapon.explosion_radius)
        self.damage_center = self.rect.center
        self.damage_rect = self.damage_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        if self.falling:
            surface.blit(self.image, self.rect)
        elif self.explosion_started:
            surface.blit(self.damage_surface, self.rect.move(-self.weapon.explosion_radius + self.rect.width // 2,
                                                             -self.weapon.explosion_radius + self.rect.height // 2))

    def inflict_persistent_damage(self, all_enemies):
        if not self.explosion_started:
            return
        for enemy in all_enemies:
            distance = math.hypot(enemy.rect.centerx - self.damage_center[0],
                                  enemy.rect.centery - self.damage_center[1])
            if distance <= self.weapon.explosion_radius:
                self.attract_enemy(enemy)

                if not enemy.is_flashing:
                    enemy.take_damage(self.weapon.persistent_damage)
                    self.mark_enemy_hit(enemy)

    def trigger_animation(self, position, all_sprites):
        if not self.animation_started:
            self.animation_started = True
            animation = Animation(position, self.weapon.animation_image_path, frame_duration=2,
                                  size=(2.5 * self.weapon.explosion_radius, 2.5 * self.weapon.explosion_radius))
            all_sprites.add(animation)

    def attract_enemy(self, enemy):
        direction_x = self.damage_center[0] - enemy.rect.centerx
        direction_y = self.damage_center[1] - enemy.rect.centery
        distance = max(1, math.hypot(direction_x, direction_y))  # Éviter la division par zéro
        attraction_x = self.weapon.attraction_force * direction_x / distance
        attraction_y = self.weapon.attraction_force * direction_y / distance
        enemy.rect.x += int(attraction_x)
        enemy.rect.y += int(attraction_y)
