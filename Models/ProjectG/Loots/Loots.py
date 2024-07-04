import math

import pygame.sprite


class Loots(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None

    def move_towards(self, target_x, target_y, speed=2):
        dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            dx, dy = dx / distance, dy / distance  # Normaliser le vecteur
            self.rect.x += dx * speed
            self.rect.y += dy * speed

    def gain_loot(self):
        print("gain loot")