import pygame

from Models.WordleAnswer import WordleAnswer


class WordleLetters:
    def __init__(self, letter_length):
        self.letter_length = letter_length
        self.already_answered = []
        self.all_letters = pygame.sprite.Group()
        self.set_letters()

        self.current_answer = pygame.sprite.Group()
        self.all_answer = []
        self.last_valid = []

    def set_letters(self):
        self.all_letters.empty()

        for i in range(0, self.letter_length):
            self.all_letters.add(WordleAnswer(""))

    def add_answer(self, answer):
        self.already_answered.append(answer)

    def set_answer(self):
        self.last_valid.clear()
        self.current_answer.empty()
        for answer in self.already_answered:
            self.current_answer.add(WordleAnswer(answer))
            self.last_valid.append(answer)

        self.all_answer.append(self.current_answer.copy())
        self.already_answered.clear()
