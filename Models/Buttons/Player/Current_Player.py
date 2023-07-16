import pygame


class Current_Player(pygame.sprite.Sprite):
    def __init__(self, current_player):
        super().__init__()
        self.name = "Current Player"
        self.category_id = 0
        self.image = pygame.image.load("Assets/Player/{}".format(current_player)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (600, 150)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 650
        self.rect.y = 50
        self.text = ""
        self.font = pygame.font.SysFont("Verdana", 50)

    def get_rect(self):
        return self.rect
