import pygame.sprite


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.pos = [1000, 700]
        self.image = enemy.image
        self.rect = enemy.rect
        self.health = enemy.health

