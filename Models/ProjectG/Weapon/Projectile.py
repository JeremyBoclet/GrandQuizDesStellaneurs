import math

import pygame

WIDTH = 1920
HEIGHT = 1080

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, target_x,target_y, speed, image,damage):
        super().__init__()
        self.speed = speed
        self.image = image
        self.rect = self.image.get_rect(center=(pos_x,pos_y))
        self.angle = math.atan2(target_y - pos_y, target_x - pos_x)
        self.damage = damage
        self.cooldown = 400

        self.dx = self.speed * math.cos(self.angle)
        self.dy = self.speed * math.sin(self.angle)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Vérifier si le projectile sort de l'écran
        if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()  # Détruire le projectile
