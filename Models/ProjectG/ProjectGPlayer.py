from pygame import *

import math
import pygame
import time
from Models.ProjectG.Inventory import Inventory


class ProjectGPlayer(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()

        self.background_x = 0
        self.background_y = 0
        self.screen = screen
        self.image = pygame.image.load("../Assets/ProjectG/Mage.png")
        self.image = pygame.transform.scale(self.image, (48, 54)).convert_alpha()

        self.sprite_left = pygame.transform.flip(self.image, True, False)
        self.sprite_right = self.image

        self.pos = [self.screen.get_width()//2 - 24, self.screen.get_height()//2-27]

        self.rect = self.image.get_rect(center=self.pos)


        self.speed = 5

        self.last_fire = 0

        self.inventory = Inventory(self,screen)

        # Gestion de l'experience
        self.experience = 0
        self.next_level_experience_needed = 1000
        self.level = 1
        self.base_health = 100
        self.health = 100
        self.is_flashing = False
        self.flash_timer = 0
        self.flash_duration = 0.005
        self.default_sprite = self.image

        self.image_hit = pygame.image.load("../Assets/ProjectG/Mage_hit.png")
        self.image_hit = pygame.transform.scale(self.image_hit, (48, 54)).convert_alpha()

        self.attraction_radius = 170

        self.direction = pygame.math.Vector2()
        self.sprite_to_move = None

    def movement(self):
        key_pressed = key.get_pressed()
        move_x = 0
        move_y = 0
        if key_pressed[pygame.K_LEFT]:
            for sprite_to_move in self.sprite_to_move:
                sprite_to_move.rect.x += self.speed
            move_x = -1
            self.background_x += self.speed

            self.image = self.sprite_left
        if key_pressed[pygame.K_RIGHT]:
            for sprite_to_move in self.sprite_to_move:
                sprite_to_move.rect.x -= self.speed
            self.background_x -= self.speed
            move_x = 1
            self.image = self.sprite_right
        if key_pressed[pygame.K_UP]:
            for sprite_to_move in self.sprite_to_move:
                sprite_to_move.rect.y += self.speed
            self.background_y += self.speed
            move_y = -1
        if key_pressed[pygame.K_DOWN]:
            for sprite_to_move in self.sprite_to_move:
                sprite_to_move.rect.y -= self.speed
            self.background_y -= self.speed
            move_y = 1

            # Normalisation de la vitesse pour les mouvements diagonaux
        if move_x != 0 and move_y != 0:
            move_x *= self.speed / math.sqrt(2)
            move_y *= self.speed / math.sqrt(2)
        else:
            move_x *= self.speed
            move_y *= self.speed

        self.rect.x += move_x
        self.rect.y += move_y

        # check pour ne pas sortir de l'écran
        if self.pos[0] <= 0:
            self.pos[0] = 0
        if self.pos[0] >= self.screen.get_width() - 48:
            self.pos[0] = self.screen.get_width() - 48
        if self.pos[1] <= 0:
            self.pos[1] = 0
        if self.pos[1] >= self.screen.get_height() - 54:
            self.pos[1] = self.screen.get_height() - 54

        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def additional_update(self, sprite_to_move):
        self.sprite_to_move = sprite_to_move


    def update(self):
        self.movement()
        self.inventory.update()

        # affichage de la zone d'attraction du loot
        pygame.draw.circle(self.screen, (0, 0, 255), self.rect.center, self.attraction_radius, 1)

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

        self.rect.center += self.direction * self.speed

        # check pour ne pas sortir de l'écran
        if self.pos[0] <= 0:
            self.pos[0] = 0
        if self.pos[0] >= self.screen.get_width() - 48:
            self.pos[0] = self.screen.get_width() - 48
        if self.pos[1] <= 0:
            self.pos[1] = 0
        if self.pos[1] >= self.screen.get_height() - 54:
            self.pos[1] = self.screen.get_height() - 54

    def draw_experience_bar(self, surface):
        # Dimensions de la barre
        bar_width = 1800
        bar_height = 5
        xp_bar_x = 50
        xp_bar_y = 10

        # Barre de fond (noir)
        pygame.draw.rect(surface, (0, 0, 0), (xp_bar_x, xp_bar_y, bar_width, bar_height))

        # Barre de vie actuelle (rouge)
        current_xp_ratio = self.experience / self.next_level_experience_needed
        current_xp_width = bar_width * current_xp_ratio
        pygame.draw.rect(surface, (0, 255, 0), (xp_bar_x, xp_bar_y, current_xp_width, bar_height))


    def take_damage(self, damage):
        if not self.is_flashing:
            self.health -= damage

        self.is_flashing = True
        self.flash_timer = time.time()
        if self.health <= 0:
            self.health = 0

    def draw_health_bar(self, surface):
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

    def attract_loots(self, loots, speed=15):
        for loot in loots:
            dx, dy = loot.rect.centerx - self.rect.centerx, loot.rect.centery - self.rect.centery
            distance = math.hypot(dx, dy)
            if distance <= self.attraction_radius:
                loot.move_towards(self.rect.centerx, self.rect.centery, speed)
