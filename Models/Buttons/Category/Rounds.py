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
        self.margin = 85

        match round_number:
            case 1:
                self.rect.y = self.margin
            case 2:
                spacing = ((round_number - 1) * 90) + self.margin
                self.rect.y = spacing + ((round_number - 1) * 100)
            case 3:
                self.rect.x = self.screen.get_width() / 2 - 660
                spacing = (2 * 90) + self.margin
                self.rect.y = spacing + (2 * 100)
            case 4:
                self.rect.x = self.screen.get_width() / 2 + 10
                spacing = (2 * 90) + self.margin
                self.rect.y = spacing + (2 * 100)
            case 5 | 6:
                spacing = ((round_number - 1) * 90) + self.margin
                self.rect.y = spacing + ((round_number - 3) * 100)
            case 7: # Password
                self.rect.y = self.margin
            case 8: # MoneyDrop
                self.rect.y = 275
            case 9: # Wordle
                self.rect.y = 465
            case 10: # Timer
                self.rect.y = 645
            case "Quit":
                self.rect.x = 10
                self.rect.y = self.screen.get_height() - 60
                self.image = pygame.transform.scale(self.image, (200, 60)).convert_alpha()

