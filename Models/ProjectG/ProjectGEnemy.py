import math
import random
import time

import pygame.sprite

from Models.ProjectG.Loots.RegenHealth import RegenHealth
from Models.ProjectG.Loots.Shards import Shards


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
        self.loot = None
        self.damage = 0
        self.detection_range = 400  # La distance maximale du triangle
        self.angle_range = 30  # L'angle de la vision en degrés
        self.player_in_sight = False
        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.change_direction_time = pygame.time.get_ticks()
        self.target = None

    def take_damage(self, damage):
        self.is_targeted = True
        self.health -= damage
        self.is_flashing = True
        self.flash_timer = time.time()

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

        if self.is_player_in_detection_area(self.player):
            self.player_in_sight = True
            self.move_towards(self.player)
        elif self.is_player_in_aggro_circle(self.player) and self.player_in_sight:
            self.move_towards(self.player)
        else:
            self.player_in_sight = False
            #self.wander()

    def draw_health_bar(self, surface):
        # if not self.is_targeted:
        #     return
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

    def spawn_loots(self):
        # Probabilités de drop : [shard, potion, rien]
        loot_types = ['shard', 'potion', 'none']
        drop_rates = [0.6, 0.2, 0.2]  # 60% shard, 20% potion, 20% rien

        loot_choice = random.choices(loot_types, drop_rates)[0]

        if loot_choice == 'shard':
            return Shards(self.rect.centerx, self.rect.centery, "shard_1", 2)
        elif loot_choice == 'potion':
            return RegenHealth(self.rect.centerx, self.rect.centery)
        else:
            return None  # Aucun loot n'est généré

    def is_player_in_aggro_circle(self, player):
        distance = math.hypot(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery)
        return distance < self.detection_range

    def is_player_in_detection_area(self, player):
        if self.player_in_sight:
            return False

        # Calculez les coordonnées des trois points du triangle de repérage
        angle_offset = math.atan2(self.direction.y, self.direction.x)
        angle_left = angle_offset + math.radians(self.angle_range / 2)
        angle_right = angle_offset - math.radians(self.angle_range / 2)

        x1, y1 = self.rect.center
        x2 = x1 + self.detection_range * math.cos(angle_left)
        y2 = y1 + self.detection_range * math.sin(angle_left)
        x3 = x1 + self.detection_range * math.cos(angle_right)
        y3 = y1 + self.detection_range * math.sin(angle_right)

        # Utilisez la fonction pygame pour détecter si le joueur est dans le triangle
        triangle = [(x1, y1), (x2, y2), (x3, y3)]
        return self.point_in_triangle(player.rect.center, triangle)

    def point_in_triangle(self, point, triangle):
        # Utilise l'algorithme de barycentric coordinates pour vérifier si un point est dans un triangle
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(point, triangle[0], triangle[1]) < 0.0
        b2 = sign(point, triangle[1], triangle[2]) < 0.0
        b3 = sign(point, triangle[2], triangle[0]) < 0.0

        return ((b1 == b2) and (b2 == b3))

    def move_towards(self, player):
        self.target = player
        dx, dy = player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.direction = pygame.Vector2(dx, dy).normalize()
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def wander(self):
        if self.target and math.hypot(self.rect.centerx - self.target.rect.centerx, self.rect.centery - self.target.rect.centery) < self.detection_range:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.change_direction_time > 1000:  # Change de direction toutes les secondes
            self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
            self.change_direction_time = current_time

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def draw_detection_area(self, screen):
        angle_offset = math.atan2(self.direction.y, self.direction.x)
        angle_left = angle_offset + math.radians(self.angle_range / 2)
        angle_right = angle_offset - math.radians(self.angle_range / 2)

        x1, y1 = self.rect.center
        x2 = x1 + self.detection_range * math.cos(angle_left)
        y2 = y1 + self.detection_range * math.sin(angle_left)
        x3 = x1 + self.detection_range * math.cos(angle_right)
        y3 = y1 + self.detection_range * math.sin(angle_right)

        pygame.draw.polygon(screen, (0, 255, 0), [(x1, y1), (x2, y2), (x3, y3)], 2)