import pygame

from Models.InputBox import InputBox


class DropScreen:
    def __init__(self, screen):
        self.is_playing = False
        self.screen = screen

        self.input_box1 = InputBox(100, 100, 140, 32, True, 32)
        self.input_box2 = InputBox(100, 300, 140, 32, True, 32)
        self.input_box3 = InputBox(400, 100, 140, 32, True, 32)
        self.input_box4 = InputBox(400, 300, 140, 32, True, 32)

        self.cancel_image = pygame.image.load("../Assets/Cancel.png")
        self.cancel_image = pygame.transform.scale(self.cancel_image,
                                                   (200, 65)).convert_alpha()
        self.cancel_rect = self.cancel_image.get_rect()

    def update(self):
        self.input_box1.draw(self.screen)
        self.input_box2.draw(self.screen)
        self.input_box3.draw(self.screen)
        self.input_box4.draw(self.screen)

       # Bouton annuler
        self.screen.blit(self.cancel_image,
                            (20, self.screen.get_height() - self.cancel_image.get_height()))
        self.cancel_rect = pygame.Rect(20, self.screen.get_height() - self.cancel_image.get_height(), 200, 65)