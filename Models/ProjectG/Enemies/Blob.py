import math

import pygame.sprite


class Blob(pygame.sprite.Sprite):

    def __init__(self,x,y, player):
        super().__init__()
        self.player = player
        self.base_health = 20
        self.health = 20

        size_factor = self.health / self.base_health
        new_size = [int(52 * size_factor), int(28 * size_factor)]


        self.image = pygame.image.load("../Assets/ProjectG/blob.png")
        self.image = pygame.transform.scale(self.image, (new_size[0], new_size[1])).convert_alpha()

        self.sprite_left = pygame.transform.flip(self.image, True, False)
        self.sprite_right = self.image

        self.rect = self.image.get_rect(center=(x,y))
        self.speed = 2

        self.spawn_cooldown = 200
        self.last_spawn = 0

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

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def update(self):
        self.movement()
