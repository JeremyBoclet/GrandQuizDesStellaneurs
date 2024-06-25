import math
import time

import pygame.sprite


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = [1000, 700]
        self.image = None
        self.image_hit = None
        self.default_sprite = None
        self.rect = None
        self.health = None
        self.base_health = None
        self.is_flashing = False
        self.flash_timer = 0
        self.flash_duration = 0.5  # Durée du clignotement en secondes
        self.is_targeted = False
        self.player = None

    def take_damage(self, damage):
        self.is_targeted = True
        self.health -= damage
        self.is_flashing = True  # Activer le clignotement
        self.flash_timer = time.time()

        if self.health <= 0:
            self.kill()

    def update(self, ennemies):
        # Éviter la superposition avec d'autres blobs
        self.avoid_overlap(ennemies)

        # Gestion du clignotement
        if self.is_flashing:
            current_time = time.time()
            if current_time - self.flash_timer < self.flash_duration:
                # Alterner la couleur pour le clignotement
                if int(current_time * 10) % 2 == 0:
                    self.image = self.image_hit  # Rouge pour le clignotement
                else:
                    self.image = self.default_sprite  # Vert pour la couleur normale
            else:
                self.is_flashing = False
                self.image = self.default_sprite

    def draw_health_bar(self, surface):
        if not self.is_targeted:
            return
        # Dimensions des barres de vie
        bar_width = self.rect.width
        bar_height = 5
        health_bar_x = self.rect.x
        health_bar_y = self.rect.y - 10

        # Barre de fond (noir)
        pygame.draw.rect(surface, (0, 0, 0), (health_bar_x, health_bar_y, bar_width, bar_height))

        # Barre de vie actuelle (rouge)
        current_health_ratio = self.health / self.base_health
        current_health_width = bar_width * current_health_ratio
        pygame.draw.rect(surface, (255, 0, 0), (health_bar_x, health_bar_y, current_health_width, bar_height))

    def avoid_overlap(self, enemies):
        for ennemi in enemies:
            if ennemi != self and self.rect.colliderect(ennemi.rect):
                # Calculer la direction d'éloignement
                dx = self.rect.centerx - ennemi.rect.centerx
                dy = self.rect.centery - ennemi.rect.centery
                distance = math.hypot(dx, dy)

                if distance == 0:
                    distance = 1  # Pour éviter la division par zéro
                overlap = (self.rect.width / 2 + ennemi.rect.width / 2) - distance
                if overlap > 0:
                    move_x = overlap * (dx / distance)
                    move_y = overlap * (dy / distance)
                    self.rect.x += move_x
                    self.rect.y += move_y

    def movement(self):
        # Calculer la direction vers le joueur
        direction_x = self.player.rect.centerx - self.rect.centerx
        direction_y = self.player.rect.centery - self.rect.centery
        distance = math.hypot(direction_x, direction_y)

        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Mettre à jour la position
        self.rect.x += direction_x * self.speed
        self.rect.y += direction_y * self.speed

