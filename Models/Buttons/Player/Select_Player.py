import pygame


class Select_Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = "Select Player"
        self.category_id = 0
        self.image = pygame.image.load("../Assets/Select_Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (600, 150)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50

    def get_rect(self):
        return self.rect
