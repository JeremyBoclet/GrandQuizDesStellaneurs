import pygame


class TimerEventBar:
    # lors du chargement > Compteur
    def __init__(self, surface, game):
        self.percent = 0
        self.surface = surface
        self.game = game
        self.percent_speed = 60 / 10

    def add_percent(self):
        self.percent += self.percent_speed / 100

    def is_full_loaded(self):
        return self.percent >= 100

    def attempt_fall(self):
        if self.is_full_loaded():
            self.reset_percent()

    def reset_percent(self):
        self.percent = 0

    def update_bar(self, surface):
        self.add_percent()
        self.attempt_fall()
        pygame.draw.rect(surface, (0, 0, 0), [0, surface.get_height() - 20, surface.get_width(), 10])
        pygame.draw.rect(surface, (187, 11, 11),
                         [0, surface.get_height() - 20, (surface.get_width() / 100) * self.percent, 10])
