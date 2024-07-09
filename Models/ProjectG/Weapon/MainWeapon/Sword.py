import math
import pygame

class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/sword.png").convert_alpha(),(50,150))  # chargez votre image d'épée ici
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.swinging = False
        self.swing_speed = 10
        self.swing_angle = 90
        self.current_angle = 0
        self.damage = 20

    def update(self):
        if self.swinging:
            self.current_angle += self.swing_speed
            if self.current_angle >= self.swing_angle:
                self.swinging = False
                self.current_angle = 0
            else:
                # Pivoter l'épée autour de son pommeau (0,0)
                self.image = pygame.transform.rotate(self.original_image, -self.current_angle)
                offset_x = self.rect.width // 2
                offset_y = self.rect.height // 2
                self.rect = self.image.get_rect(
                    center=(self.player.rect.centerx + offset_x, self.player.rect.centery + offset_y))

    def start_swing(self):
        if not self.swinging:
            self.swinging = True

    def check_collision(self, enemies):
        if self.swinging:
            for enemy in enemies:
                if self.rect.colliderect(enemy.rect):
                    enemy.take_damage(self.damage)
