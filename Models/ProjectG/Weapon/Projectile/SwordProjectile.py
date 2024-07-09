import pygame
import math

from Models.ProjectG.Animation.Animation import Animation
from Models.ProjectG.Weapon.Projectile.Projectile import Projectile


class SwordProjectile(Projectile):
    def __init__(self, x, y, target_x, target_y, weapon, player):
        super().__init__(x, y, target_x, target_y, weapon, player)
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.current_length = 0
        self.rect = self.image.get_rect(center=(x, y))
        print(f"direction = {target_x},{target_y}")
        self.angle = math.atan2(target_y - self.y, target_x - self.x) - math.radians(45)
        self.dx = self.weapon.growth_rate * math.cos(self.angle)
        self.dy = self.weapon.growth_rate * math.sin(self.angle)
        self.turn_count = 0
        self.spawn_time = pygame.time.get_ticks()
        self.animation_started = False
        self.position=(x,y)
    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_seconds = (current_time - self.spawn_time) / 1000.0  # Temps écoulé depuis la création en secondes

        if elapsed_seconds >= self.weapon.max_lifetime:
            self.weapon.is_swinging = False
            self.kill()  # Détruire le projectile après le temps maximal

        self.x = self.player.rect.centerx
        self.y = self.player.rect.centery

        if self.current_length < self.weapon.max_length:
            self.current_length += self.weapon.growth_rate
            if self.current_length >= self.weapon.max_length:
                self.current_length = self.weapon.max_length
        elif self.weapon.max_turn != 0:
            # Une fois la taille maximale atteinte, commencer la rotation
            self.angle += self.weapon.rotation_speed
            if self.angle >= 2 * math.pi:
                self.angle -= 2 * math.pi
                self.turn_count += 1
                self.hit_enemies = []
        else:
            self.weapon.is_swinging = False
            self.kill()

        if self.turn_count == self.weapon.max_turn and self.weapon.max_turn != 0:
            self.weapon.is_swinging = False
            self.kill()

        self.image = pygame.Surface((self.current_length, self.weapon.width), pygame.SRCALPHA)
        end_x = self.current_length * math.cos(self.angle)
        end_y = self.current_length * math.sin(self.angle)
        pygame.draw.line(self.image, self.color, (0, self.weapon.width // 2),
                         (self.current_length, self.weapon.width // 2),
                         self.weapon.width)

        self.image = pygame.transform.rotate(self.image, -math.degrees(self.angle))
        self.rect = self.image.get_rect(center=(self.x + end_x // 2, self.y + end_y // 2))

    def trigger_animation(self, position, all_sprites):
        if not self.animation_started:
            self.animation_started = True
            animation = Animation(position, self.weapon.animation_image_path, frame_duration=10,
                                  size=(100,200))
            all_sprites.add(animation)
