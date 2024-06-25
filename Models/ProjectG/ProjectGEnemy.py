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

    def take_damage(self, damage):
        self.is_targeted = True
        if not self.is_flashing:
            self.health -= damage
            self.is_flashing = True  # Activer le clignotement
            self.flash_timer = time.time()

        if self.health <= 0:
            self.kill()

    def update(self):
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
