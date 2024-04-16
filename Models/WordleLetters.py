import pygame

from Models.WordleAnswer import WordleAnswer


class WordleLetters:
    def __init__(self, letter_length):
        self.letter_length = letter_length

        self.all_letters = pygame.sprite.Group()
        self.set_letters()

    def set_letters(self):
        self.all_letters.empty()

        for i in range(0, self.letter_length):
            self.all_letters.add(WordleAnswer(""))


