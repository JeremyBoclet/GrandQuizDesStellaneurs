import pygame
from PinsAnswer import PinsAnswer


class PasswordPins:
    def __init__(self, max_attempt):
        self.max_attempt = max_attempt
        self.background_width = max_attempt * 250
        self.background_image = pygame.image.load("../Assets/LongBlank.png")
        self.background_image = pygame.transform.scale(self.background_image,
                                                       (self.background_width, 200)).convert_alpha()

        self.answered_password = []

        self.all_pins = pygame.sprite.Group()
        self.set_pins()

    def set_pins(self):
        self.all_pins.empty()
        for answer in self.answered_password:
            self.all_pins.add(PinsAnswer(answer))

        for i in range(len(self.answered_password), self.max_attempt):
            self.all_pins.add(PinsAnswer(""))

    def add_answer(self, answer):
        self.answered_password.append(answer)

