import random

import pygame

from Models.Bdd import Bdd
from Models.Buttons.Player.Players import Players
from Models.PasswordPins import PasswordPins


class PasswordScreen:
    def __init__(self, screen):
        self.good_answer_text = None
        self.cancel_image = pygame.image.load("../Assets/Cancel.png")
        self.cancel_image = pygame.transform.scale(self.cancel_image,
                                                   (200, 65)).convert_alpha()
        self.cancel_rect = self.cancel_image.get_rect()

        self.font = pygame.font.SysFont("Futura-bold", 80)
        self.question_font_color = (240, 255, 255)

        self.button_width = 400
        self.button_height = 130

        self.win_image = pygame.image.load("../Assets/Win.png")
        self.win_image = pygame.transform.scale(self.win_image,
                                                (1000, 500)).convert_alpha()

        self.loose_image = pygame.image.load("../Assets/Loose.png")
        self.loose_image = pygame.transform.scale(self.loose_image,
                                                  (1000, 500)).convert_alpha()

        self.return_image = pygame.image.load("../Assets/Return.png")
        self.return_image = pygame.transform.scale(self.return_image,
                                                   (self.button_width, self.button_height)).convert_alpha()
        self.return_rect = self.return_image.get_rect()

        self.category_image = pygame.image.load("../Assets/Round7.png")
        self.category_image = pygame.transform.scale(self.category_image,
                                                     (600, 150)).convert_alpha()
        self.good_answer_image = pygame.image.load("../Assets/Good_Answer.png")
        self.good_answer_image = pygame.transform.scale(self.good_answer_image,
                                                        (self.button_width, self.button_height)).convert_alpha()
        self.good_answer_rect = self.good_answer_image.get_rect()

        self.bad_answer_image = pygame.image.load("../Assets/Bad_Answer.png")
        self.bad_answer_image = pygame.transform.scale(self.bad_answer_image,
                                                       (self.button_width, self.button_height)).convert_alpha()
        self.bad_answer_rect = self.bad_answer_image.get_rect()

        self.screen = screen
        self.password_pins = PasswordPins(0)

        self.good_answer_pos_x = (self.screen.get_width() - self.good_answer_image.get_width()) / 1.3
        self.good_answer_pos_y = self.screen.get_height() - self.good_answer_image.get_height()
        self.bad_answer_pos_x = (self.screen.get_width() - self.bad_answer_image.get_width()) / 4
        self.bad_answer_pos_y = self.screen.get_height() - self.bad_answer_image.get_height()

        self.pin_default_pos = (self.screen.get_width() / 2 - self.password_pins.background_width / 2) + 25

        self.is_playing = False

        self.passwords = []

        self.bdd = Bdd()

        df = self.bdd.read_excel("Password")
        df.reset_index()
        for index, row in df.iterrows():
            self.passwords.append(row["Password"])

        self.current_password = ""
        self.current_question = ""

        self.current_player = Players("Player", 1)
        self.current_player_image = pygame.sprite.Group()
        self.current_player_name = ""
        self.game_over = False
        self.defeat = False

    def set_max_attempt(self, max_attempt):
        self.password_pins = PasswordPins(max_attempt)
        self.pin_default_pos = (self.screen.get_width() / 2 - self.password_pins.background_width / 2) + 25

    def set_answer(self, answer):
        self.password_pins.add_answer(answer)
        self.password_pins.set_pins()

    def set_password(self):
        r = list(range(1, len(self.passwords)))
        random.shuffle(r)

        self.current_password = self.passwords[r[0]]
        self.passwords.pop(r[0])

    def set_end_pin(self):
        for i in range(len(self.password_pins.answered_password), self.password_pins.max_attempt):
            self.password_pins.add_answer("end")

        self.password_pins.set_pins()

    def update(self):
        if self.current_player_name != self.current_player.name:
            self.current_player_image = pygame.image.load(
                "../Assets/Player/{}.png".format(self.current_player.name)).convert_alpha()
            self.current_player_image = pygame.transform.scale(self.current_player_image, (400, 100))
            self.current_player_name = self.current_player.name

        self.screen.blit(self.current_player_image,
                         (1500, 5))
        if not self.game_over:
            if self.password_pins.answered_password.count('valid') == 5:
                # Victoire
                # self.is_playing = False
                self.game_over = True
                self.defeat = False
                self.set_end_pin()

                match self.password_pins.max_attempt:
                    case 5:
                        print("difficile")
                        self.current_player.add_point(4)
                    case 6:
                        print("moyen")
                        self.current_player.add_point(2)
                    case _:
                        print("facile")
                        self.current_player.add_point(1)

            elif self.password_pins.max_attempt - self.password_pins.answered_password.count('error') < 5:
                # Il ne reste pas assez de question pour faire 5 bonnes réponses
                # self.is_playing = False
                self.game_over = True
                self.defeat = True
                self.set_end_pin()

                print("Plus assez d'essai")
            elif len(self.password_pins.answered_password) == self.password_pins.max_attempt:
                # nombre d'essai atteint (Defaite)
                # self.is_playing = False
                self.game_over = True
                self.defeat = True
                self.set_end_pin()
                print("defaite")



        # Affichage du mot de passe
        self.current_question = self.font.render(self.current_password, True, self.question_font_color)
        self.screen.blit(self.current_question, ((self.screen.get_width() - self.current_question.get_width()) / 2,
                                                 self.screen.get_height() / 4))

        if not self.game_over:
            # Bouton annuler
            self.screen.blit(self.cancel_image,
                             (20, self.screen.get_height() - self.cancel_image.get_height()))
            self.cancel_rect = pygame.Rect(20, self.screen.get_height() - self.cancel_image.get_height(), 200, 65)

            # Bonne réponse
            self.screen.blit(self.good_answer_image,
                             (self.good_answer_pos_x,
                              self.good_answer_pos_y))

            self.good_answer_rect = pygame.Rect(self.good_answer_pos_x,
                                                self.good_answer_pos_y, self.button_width, self.button_height)

            # Mauvaise Réponse
            self.screen.blit(self.bad_answer_image,
                             (self.bad_answer_pos_x,
                              self.bad_answer_pos_y))

            self.bad_answer_rect = pygame.Rect(self.bad_answer_pos_x,
                                               self.bad_answer_pos_y, self.button_width, self.button_height)
        else:
            # Fin de partie: bouton retour
            self.screen.blit(self.return_image,
                             (20, self.screen.get_height() - self.return_image.get_height()))

            self.return_rect = pygame.Rect(20,
                                           self.screen.get_height() - self.return_image.get_height(),
                                           self.button_width,
                                           self.button_height)

        # Category
        self.screen.blit(self.category_image, (self.screen.get_width() / 2 - 310, 50))

        # Nombre de bonnes réponses
        self.good_answer_text = self.font.render("Points : {}".format(self.current_player.total_point)
                                                 , True,
                                                 (255, 255, 255))
        self.screen.blit(self.good_answer_text,
                         ((self.screen.get_width() - self.good_answer_text.get_width()) / 2,
                          self.screen.get_height() - 60))

        # Background barre grise
        self.screen.blit(self.password_pins.background_image,
                         (self.screen.get_width() / 2 - self.password_pins.background_width / 2, 500))

        # Pins
        for index, pins in enumerate(self.password_pins.all_pins):
            self.screen.blit(pins.pin, (self.pin_default_pos + (250 * index), 498))

        if self.game_over:
            if self.defeat:
                self.screen.blit(self.loose_image, (self.screen.get_width() / 2 - self.loose_image.get_width() / 2,
                                                    self.screen.get_height() - self.loose_image.get_height()))
            else:
                self.screen.blit(self.win_image,  (self.screen.get_width() / 2 - self.win_image.get_width() / 2,
                                                    self.screen.get_height() - self.win_image.get_height()))
