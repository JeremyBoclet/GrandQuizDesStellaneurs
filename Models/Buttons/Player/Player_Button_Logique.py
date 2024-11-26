import pygame


class Player_Button_Logique(pygame.sprite.Sprite):
    def __init__(self, name, x, y, scale_x, scale_y):
        super().__init__()
        self.name = name
        self.image_selected = pygame.image.load("../Assets/Logique/{}.png".format(name)).convert_alpha()
        self.image_selected = pygame.transform.scale(self.image_selected, (scale_x, scale_y)).convert_alpha()

        self.image_unselected = pygame.image.load("../Assets/Logique/{}_gray.png".format(name)).convert_alpha()
        self.image_unselected = pygame.transform.scale(self.image_unselected, (scale_x, scale_y)).convert_alpha()

        self.image = self.image_unselected
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.is_selected = False

    def get_rect(self):
        return self.rect

    def change_selection(self):
        self.is_selected = not self.is_selected
        if self.is_selected:
            self.image = self.image_selected
        else:
            self.image = self.image_unselected

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y