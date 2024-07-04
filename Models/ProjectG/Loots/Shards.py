import math

import pygame.sprite

from Models.ProjectG.Loots.Loots import Loots


class Shards(Loots):
    def __init__(self, x, y, image, experience_gain):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("../Assets/ProjectG/{}.png".format(image)).convert_alpha(),
            (20, 30))
        self.rect = self.image.get_rect(center=(x, y))
        self.experience_gain = experience_gain

    def gain_loot(self, player):
        player.experience += self.experience_gain
        if player.experience >= player.next_level_experience_needed:
            player.level += 1
            player.experience = player.next_level_experience_needed - player.experience
            player.next_level_experience_needed *= 1.6
