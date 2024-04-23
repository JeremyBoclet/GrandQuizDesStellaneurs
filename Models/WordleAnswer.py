from random import random

import pygame

class WordleAnswer(pygame.sprite.Sprite):
    def __init__(self, answer):
        super().__init__()

        match answer:
            case "valid":
                self.pin = pygame.image.load("../Assets/WordleLettreOK.png")
            case "wrong":
                self.pin = pygame.image.load("../Assets/WordleLettreWrong.png")
            case "nok":
                self.pin = pygame.image.load("../Assets/WordleLettreNOK.png")
            case _:
                self.pin = pygame.image.load("../Assets/WordleTemplate.png")

        self.pin = pygame.transform.scale(self.pin, (106, 120)).convert_alpha()
