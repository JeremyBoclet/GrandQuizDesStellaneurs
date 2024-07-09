import math

import pygame.sprite

from Models.ProjectG.ProjectGEnemy import Enemy


class Blob(Enemy):

    def __init__(self, x, y, player):
        super().__init__()
        self.player = player
        self.base_health = 20
        self.health = 20

        size_factor = self.health / self.base_health

        new_size = [int(52 * size_factor), int(28 * size_factor)]

        self.image = pygame.image.load("../Assets/ProjectG/blob.png")
        self.image = pygame.transform.scale(self.image, (new_size[0], new_size[1])).convert_alpha()

        self.image_hit = pygame.image.load("../Assets/ProjectG/blob_hit.png")
        self.image_hit = pygame.transform.scale(self.image_hit, (new_size[0], new_size[1])).convert_alpha()

        self.sprite_left = pygame.transform.flip(self.image, True, False)
        self.sprite_right = self.image

        self.default_sprite = self.image

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

        self.spawn_cooldown = 200
        self.last_spawn = 0
        self.damage = 20

