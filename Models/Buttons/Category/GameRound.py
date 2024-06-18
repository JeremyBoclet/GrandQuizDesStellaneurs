import pygame


class GameRounds(pygame.sprite.Sprite):
    def __init__(self, round_number, screen):
        super().__init__()
        self.screen = screen
        self.category_id = -10
        self.round_id = round_number
        self.image = pygame.image.load("../Assets/{}.png".format(round_number)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (180, 180)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = self.screen.get_height() / 2 - 200
        self.rect.x = 0
        self.margin = 85
        self.spacing = 190

        match round_number:
            case "password":
                self.rect.x = self.screen.get_width() / 2 - 390

            case "drop": # MoneyDrop
                self.rect.x = self.screen.get_width() / 2 - 190

            case "wordle": # Wordle
                self.rect.x = self.screen.get_width() / 2 + 10

            case "timer": # Timer
                self.rect.x = self.screen.get_width() / 2 + 210

            case "Quit":
                self.rect.x = 10
                self.rect.y = self.screen.get_height() - 60
                self.image = pygame.transform.scale(self.image, (200, 60)).convert_alpha()

