import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, name, category_id, x, y, scale_x, scale_y):
        super().__init__()
        self.name = name
        self.category_id = category_id
        self.image = pygame.image.load("Assets/{}.png".format(name)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (scale_x, scale_y)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.had_been_chosen = False

    def get_rect(self):
        return self.rect
