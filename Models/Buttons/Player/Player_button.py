import pygame

from Models.Buttons.Player.Players import Players


class Player_button(pygame.sprite.Sprite):
    def __init__(self, name, x, y, main_category_id):
        super().__init__()
        self.image = pygame.image.load("Assets/Player/{}.png".format(name)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (600, 150))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = Players(name, main_category_id)
