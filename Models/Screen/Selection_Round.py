import pygame

from Models.Buttons.Category.Rounds import Rounds


class Selection_Round:
    def __init__(self, screen):
        self.screen = screen
        self.is_selecting_round = True
        self.group_buttons = pygame.sprite.Group()
        #self.group_buttons.add(Rounds(1, screen))
        #self.group_buttons.add(Rounds(2, screen))
        #self.group_buttons.add(Rounds(3, screen))
        #self.group_buttons.add(Rounds(4, screen))
        #self.group_buttons.add(Rounds(5, screen))  # Finale
        self.group_buttons.add(Rounds(6, screen))  # Classement
        self.group_buttons.add(Rounds(7, screen))  # Password
        self.group_buttons.add(Rounds(8, screen))  # Money Drop
        self.group_buttons.add(Rounds(9, screen))  # Wordle
        self.group_buttons.add(Rounds("Quit", screen)) # Quitter

    def update(self):
        self.group_buttons.draw(self.screen)
