import math

import pygame.sprite


class Shards(pygame.sprite.Sprite):
    def __init__(self, x, y, image, experience_gain):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/{}.png".format(image)).convert_alpha(),
                                            (20, 30))
        self.experience_gain = experience_gain
        self.rect = self.image.get_rect(center=(x, y))

    def move_towards(self, target_x, target_y, speed=2):
        dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            dx, dy = dx / distance, dy / distance  # Normaliser le vecteur
            self.rect.x += dx * speed
            self.rect.y += dy * speed
