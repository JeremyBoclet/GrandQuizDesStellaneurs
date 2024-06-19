import math
import time

import pygame

WIDTH = 1920
HEIGHT = 1080

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, target_x,target_y, weapon, is_returning = False):
        super().__init__()
        self.weapon = weapon
        self.image = weapon.image
        self.rect = self.image.get_rect(center=(pos_x,pos_y))
        self.angle = math.atan2(target_y - pos_y, target_x - pos_x)
        self.start_x = pos_x
        self.start_y = pos_y
        self.dx = self.weapon.speed * math.cos(self.angle)
        self.dy = self.weapon.speed * math.sin(self.angle)
        self.is_returning = is_returning
        self.total_distance = 0
        self.last_damage_time = 0
        self.angle_rotation = 0

    def can_damage(self):
        current_time = time.time()
        if current_time - self.last_damage_time >= self.weapon.damage_cooldown:
            self.last_damage_time = current_time
            return True
        return False

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        self.total_distance += self.weapon.speed

        # Vérifier si le projectile sort de l'écran
        if (self.rect.right < 0 or self.rect.left > WIDTH or
                self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()  # Détruire le projectile

        #check max distance
        if self.total_distance > self.weapon.max_range:
            if self.is_returning:
                # Inverser la direction du projectile pour qu'il retourne vers le joueur
                self.last_damage_time=0 #permet de reset les dégats pour le retour
                self.is_returning = False
                self.angle  += math.pi
                self.dx = self.weapon.speed * math.cos(self.angle)
                self.dy = self.weapon.speed * math.sin(self.angle)
                self.total_distance = 0
            else:
                self.kill()

        # Rotation de l'image du projectile
        if self.weapon.rotation_speed > 0:
            self.angle_rotation += self.weapon.rotation_speed
            self.image = pygame.transform.rotate(self.weapon.original_image, math.degrees(self.angle_rotation))
            self.rect = self.image.get_rect(center=self.rect.center)
