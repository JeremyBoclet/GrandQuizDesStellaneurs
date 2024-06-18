import pygame

from Models.Buttons.Category.GameRound import GameRounds
from Models.Buttons.Category.Rounds import Rounds


class Selection_Round:
    def __init__(self, screen, quiz):
        self.screen = screen
        self.is_selecting_round = True
        self.group_buttons = pygame.sprite.Group()
        if quiz:
            self.group_buttons.add(Rounds(1, screen))
            self.group_buttons.add(Rounds(2, screen))
            self.group_buttons.add(Rounds(3, screen))
            self.group_buttons.add(Rounds(4, screen))
            self.group_buttons.add(Rounds(5, screen))  # Finale
        else:
            self.group_buttons.add(GameRounds("password", screen))  # Password
            self.group_buttons.add(GameRounds("drop", screen))  # Money Drop
            self.group_buttons.add(GameRounds("wordle", screen))  # Wordle
            self.group_buttons.add(GameRounds("timer", screen))  # Timer

        self.group_buttons.add(Rounds(6, screen))  # Classement
        self.group_buttons.add(Rounds("Quit", screen)) # Quitter

    def update(self):
        self.group_buttons.draw(self.screen)
