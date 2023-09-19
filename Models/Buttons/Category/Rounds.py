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

        match round_number:
            case 1:
                self.rect.y = 40
            case 3:
                self.rect.x = self.screen.get_width() / 2 - 660
                spacing = (2 * 90) + 40
                self.rect.y = spacing + (2 * 100)
            case 4:
                self.rect.x = self.screen.get_width() / 2 + 10
                spacing = (2 * 90) + 40
                self.rect.y = spacing + (2 * 100)
            case 2:
                spacing = ((round_number - 1) * 90) + 40
                self.rect.y = spacing + ((round_number - 1) * 100)
            case 5 | 6:
                spacing = ((round_number - 1) * 90) + 40
                self.rect.y = spacing + ((round_number - 3) * 100)
            case "Quit":
                self.rect.x = 10
                self.rect.y = self.screen.get_height() - 60
                self.image = pygame.transform.scale(self.image, (200, 60)).convert_alpha()