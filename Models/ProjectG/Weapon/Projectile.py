import math
import time

import pygame

WIDTH = 1920
HEIGHT = 1080


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, target_x, target_y, weapon, player, can_return=False, delete_outside_screen=True):
        super().__init__()
        self.weapon = weapon
        self.image = weapon.image
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.angle = math.atan2(target_y - pos_y, target_x - pos_x)
        self.start_x = pos_x
        self.start_y = pos_y
        self.dx = self.weapon.speed * math.cos(self.angle)
        self.dy = self.weapon.speed * math.sin(self.angle)
        self.can_return = can_return
        self.angle_rotation = 0
        self.delete_outside_screen = delete_outside_screen
        self.hit_enemies = []  # Liste pour stocker les ennemis déjà touchés
        self.player = player
        self.is_currently_returning = False

    def update_direction(self):
        # Calculer la direction vers le joueur
        player_x, player_y = self.player.rect.center
        self.angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx)
        self.dx = self.weapon.speed * math.cos(self.angle)
        self.dy = self.weapon.speed * math.sin(self.angle)

    def can_damage(self, enemy):
        # Vérifier si l'ennemi a déjà été touché
        return enemy not in self.hit_enemies

    def mark_enemy_hit(self, enemy):
        # Ajouter l'ennemi à la liste des ennemis touchés
        self.hit_enemies.append(enemy)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Vérifier si le projectile sort de l'écran
        if ((self.rect.right < 0 or self.rect.left > WIDTH or
             self.rect.bottom < 0 or self.rect.top > HEIGHT)) and self.delete_outside_screen:
            self.kill()

        # Si le projectile est en mode retour et atteint le joueur, le détruire
        if self.is_currently_returning and self.rect.colliderect(self.player.rect):
            self.kill()

        # Vérifier la portée maximale
        distance_travelled = math.hypot(self.rect.x - self.start_x, self.rect.y - self.start_y)
        if distance_travelled > self.weapon.max_range and not self.is_currently_returning:
            # Changement de direction
            self.is_currently_returning = True
            self.hit_enemies = []  # Permet de retoucher les ennemis sur les retours

        # check max distance
        if self.is_currently_returning:
            self.update_direction()

        # Rotation de l'image du projectile
        if self.weapon.rotation_speed > 0:
            self.angle_rotation += self.weapon.rotation_speed
            self.image = pygame.transform.rotate(self.weapon.original_image, math.degrees(self.angle_rotation))
            self.rect = self.image.get_rect(center=self.rect.center)
