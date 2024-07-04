import pygame.sprite

from Models.ProjectG.Loots.Loots import Loots


class RegenHealth(Loots):
    def __init__(self,x, y):
        super().__init__()
        self.name = "Potion de soin"
        self.image = pygame.transform.scale(pygame.image.load("../Assets/ProjectG/health_potion.png").convert_alpha(),
                                            (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.health_regen = 50
        self.ico = self.image.copy()
        self.next_upgrade = "Soigne 50 pv"
        self.attribute = "loot"

    def gain_loot(self, player):
        player.health += self.health_regen
        if player.health >= player.base_health:
            player.health = player.base_health
