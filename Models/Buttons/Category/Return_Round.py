import pygame


class Return_Round(pygame.sprite.Sprite):
    def __init__(self, round):
        super().__init__()
        self.name = "Current Round"
        self.category_id = -10
        self.image = pygame.image.load("Assets/Round{}.png".format(round)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 100)).convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.x = 1500
        self.rect.y = 5

    def get_rect(self):
        return self.rect
