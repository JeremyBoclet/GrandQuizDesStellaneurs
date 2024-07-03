from pygame import *

import math
import pygame
import time
from Models.ProjectG.Inventory import Inventory


class ProjectGPlayer(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.pos = [200, 200]
        self.image = pygame.image.load("../Assets/ProjectG/Mage.png")
        self.image = pygame.transform.scale(self.image, (48, 54)).convert_alpha()

        self.sprite_left = pygame.transform.flip(self.image, True, False)
        self.sprite_right = self.image

        self.rect = self.image.get_rect(center=(200, 200))
        self.speed = 7

        self.last_fire = 0

        self.inventory = Inventory(self,screen)

        # Gestion de l'experience
        self.experience = 0
        self.next_level_experience_needed = 2
        self.level = 1
        self.base_health = 100
        self.health = 100
        self.is_flashing = False
        self.flash_timer = 0
        self.flash_duration = 0.005
        self.default_sprite = self.image

        self.image_hit = pygame.image.load("../Assets/ProjectG/Mage_hit.png")
        self.image_hit = pygame.transform.scale(self.image_hit, (48, 54)).convert_alpha()

    def movement(self):
        key_pressed = key.get_pressed()
        move_x = 0
        move_y = 0
        if key_pressed[pygame.K_LEFT]:
            move_x = -1
            self.image = self.sprite_left
        if key_pressed[pygame.K_RIGHT]:
            move_x = 1
            self.image = self.sprite_right
        if key_pressed[pygame.K_UP]:
            move_y = -1
        if key_pressed[pygame.K_DOWN]:
            move_y = 1

            # Normalisation de la vitesse pour les mouvements diagonaux
        if move_x != 0 and move_y != 0:
            move_x *= self.speed / math.sqrt(2)
            move_y *= self.speed / math.sqrt(2)
        else:
            move_x *= self.speed
            move_y *= self.speed

        self.pos[0] += move_x
        self.pos[1] += move_y

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

    def update(self):
        self.movement()
        self.inventory.update()

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

    def gain_experience(self, experience):
        self.experience += experience
        if self.experience >= self.next_level_experience_needed:
            self.level += 1
            self.experience = self.next_level_experience_needed - self.experience
            self.next_level_experience_needed *= 1.6

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
        #if self.health <= 0:

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