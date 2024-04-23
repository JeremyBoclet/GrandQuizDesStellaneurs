from random import random

import pygame

class PinsAnswer(pygame.sprite.Sprite):
    def __init__(self, answer):
        super().__init__()
        self.password = ""
        self.passwords = []

        match answer:
            case "valid":
                self.pin = pygame.image.load("../Assets/PwValid.png")
            case "error":
                self.pin = pygame.image.load("../Assets/PwError.png")
            case "end":
                self.pin = pygame.image.load("../Assets/PwEnd.png")
            case _:
                self.pin = pygame.image.load("../Assets/PwPending.png")

        self.pin = pygame.transform.scale(self.pin, (200, 200)).convert_alpha()
