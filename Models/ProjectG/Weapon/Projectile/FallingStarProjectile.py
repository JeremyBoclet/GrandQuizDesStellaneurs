import math

import pygame
import time

from Models.ProjectG.Animation.Animation import Animation
from Models.ProjectG.Weapon.Projectile.Projectile import Projectile


class FallingStarProjectile(Projectile):
    def __init__(self, start_x, end_y, weapon):
        super().__init__(1,1,1,1,weapon,None)
        self.animation_started = False
        self.damage_center = None
        self.damage_surface = None
        self.weapon = weapon
        self.image = weapon.image
        pygame.draw.circle(self.image, (255, 255, 0), (10, 10), 10)
        self.rect = self.image.get_rect(midtop=(start_x, 0))

        self.end_y = end_y
        self.screen_height = 1080

        self.impact_damage = weapon.damage
        self.persistent_damage = 1
        self.persistent_duration = 2
        self.fall_speed = weapon.speed
        self.falling = True
        self.explosion_started = False
        self.start_time = None
        self.damage_rect = None
        self.position = None

    def update(self):
        if self.falling:
            self.rect.y += self.fall_speed
            self.rect.x -= 2
            if self.rect.bottom >= self.end_y:
                self.position = (self.rect.centerx, self.rect.centery)
                self.rect.bottom = self.end_y
                self.falling = False
                self.start_time = time.time()
                self.explode()
        else:
            current_time = time.time()
            if current_time - self.start_time >= self.persistent_duration:
                self.kill()

    def explode(self):
        print("Falling star impacted!")
        self.explosion_started = True
        self.create_persistent_damage_area()

    def create_persistent_damage_area(self):
        self.damage_surface = pygame.Surface((self.weapon.explosion_radius * 2, self.weapon.explosion_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.damage_surface, (255, 0, 0, 128), (self.weapon.explosion_radius, self.weapon.explosion_radius),
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
            if not enemy.is_flashing:
                distance = math.hypot(enemy.rect.centerx - self.damage_center[0],
                                      enemy.rect.centery - self.damage_center[1])
                if distance <= self.weapon.explosion_radius:
                    enemy.take_damage(self.persistent_damage)
                    self.mark_enemy_hit(enemy)

    def trigger_animation(self, position, all_sprites):
        if not self.animation_started:
            self.animation_started = True
            animation = Animation(position, self.weapon.animation_image_path, frame_duration=3,
                                  size=(self.weapon.explosion_radius * 3, self.weapon.explosion_radius * 3))
            all_sprites.add(animation)
