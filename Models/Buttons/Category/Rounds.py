import pygame


class Rounds(pygame.sprite.Sprite):
    def __init__(self, round_number, screen):
        super().__init__()
        self.screen = screen
        self.category_id = -10
        self.round_id = round_number
        self.image = pygame.image.load("../Assets/Round{}.png".format(round_number)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (650, 150)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.screen.get_width() / 2 - 325
        if round_number == 1:
            spacing = (round_number * 20 + 50)
        else:
            spacing = ((round_number - 1) * 90) + 70
        self.rect.y = spacing + ((round_number - 1) * 100)
