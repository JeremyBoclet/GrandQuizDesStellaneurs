import random

import pygame

from Models.Bdd import Bdd
from Models.Buttons.Player.Players import Players
from Models.InputBox import InputBox
from Models.WordleLetters import WordleLetters


class WordleScreen:
    def __init__(self, screen):
        self.is_playing = False
        self.screen = screen

        self.font = pygame.font.SysFont("Futura-bold", 80)

        self.button_width = 400
        self.button_height = 130

        self.cancel_image = pygame.image.load("../Assets/Return.png")
        self.cancel_image = pygame.transform.scale(self.cancel_image,
                                                   (self.button_width , self.button_height)).convert_alpha()
        self.cancel_rect = self.cancel_image.get_rect()

        self.category_image = pygame.image.load("../Assets/Round9.png")
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

        self.good_answer_pos_x = (self.screen.get_width() - self.good_answer_image.get_width()) / 1.3
        self.good_answer_pos_y = self.screen.get_height() - self.good_answer_image.get_height()
        self.bad_answer_pos_x = (self.screen.get_width() - self.bad_answer_image.get_width()) / 4
        self.bad_answer_pos_y = self.screen.get_height() - self.bad_answer_image.get_height()

        self.current_player = Players("Player", 1)
        self.current_player_image = pygame.sprite.Group()
        self.current_player_name = ""

        self.letter_default_pos = self.screen.get_width() / 2 - (5 * 120 / 2)

        self.wordle_letters = WordleLetters(5)

        self.input_box = InputBox(50, 50, 50, 50, False, 50, need_focus=False)
        self.answered = []
        self.current_answer = ""

        self.is_game_over = False
        self.defeat = False
        self.point_earned = 0

        self.list_already_answered = []

        self.all_answer_easy = []
        self.all_answer_medium = []
        self.all_answer_hard = []

        self.bdd = Bdd()

        df = self.bdd.read_excel("Wordle")
        df.reset_index()
        for index, row in df.iterrows():
            match len(row["Wordle"]):
                case 5:
                    self.all_answer_easy.append(row["Wordle"])
                case 6:
                    self.all_answer_medium.append(row["Wordle"])
                case 7:
                    self.all_answer_hard.append(row["Wordle"])

        self.all_answers = {
            5: self.all_answer_easy,
            6: self.all_answer_medium,
            7: self.all_answer_hard}

    def set_max_attempt(self, max_attempt):
        self.wordle_letters = WordleLetters(max_attempt)
        self.letter_default_pos = (self.screen.get_width() / 2 - (max_attempt * 120) / 2)

    def add_answer(self):
        if len(self.input_box.text) == self.wordle_letters.letter_length:
            self.valid_input()
            self.wordle_letters.set_answer()
            self.answered.append(self.input_box.text)
            self.input_box.text = ""
            self.wordle_letters.set_letters()

    def valid_input(self):
        # Affichage des couleurs en fonction de la place de la lettre
        print("validation {0}".format(self.current_answer))
        letters_found = []

        letter_good_pos = {index for index, (ct, ch) in
                           enumerate(zip(self.input_box.text.upper(), self.current_answer.upper()))
                           if ct.upper() == ch.upper()}

        remaining = [char for index, char in enumerate(self.current_answer.upper())
                     if index not in letter_good_pos
                     ]
        letter_bad_pos = set()
        for index, c in enumerate(self.input_box.text.upper()):
            if index in letter_good_pos:
                continue
            try:
                remaining.remove(c)
                letter_bad_pos.add(index)
            except ValueError:
                pass

        for i in range(self.wordle_letters.letter_length):
            if i in letter_good_pos:
                self.wordle_letters.add_answer("valid")
            elif i in letter_bad_pos:
                self.wordle_letters.add_answer("wrong")
            else:
                self.wordle_letters.add_answer("nok")

    def limit_text(self):
        self.input_box.text = self.input_box.text[:self.wordle_letters.letter_length]

    def set_answer(self):
        current_length = self.wordle_letters.letter_length
        current_answer = self.all_answers.get(current_length, [])

        if current_answer:
            r = list(range(1, len(current_answer)))
            random.shuffle(r)

            self.current_answer = current_answer[r[0]]
            self.all_answers.get(current_length, []).pop(r[0])

    def update(self):
        if self.current_player_name != self.current_player.name:
            self.current_player_image = pygame.image.load(
                "../Assets/Player/{}.png".format(self.current_player.name)).convert_alpha()
            self.current_player_image = pygame.transform.scale(self.current_player_image, (400, 100))
            self.current_player_name = self.current_player.name

        self.screen.blit(self.current_player_image,
                         (1500, 5))

        # Nombre de bonnes réponses
        good_answer_text = self.font.render("Points : {}".format(self.current_player.total_point)
                                            , True,
                                            (255, 255, 255))

        self.screen.blit(good_answer_text,
                         (1580,110))

        if not self.is_game_over:
            if self.wordle_letters.last_valid.count('valid') == self.wordle_letters.letter_length:
                # Victoire
                # self.is_playing = False
                self.defeat = False
                self.is_game_over = True
                max_pts = 0
                match self.wordle_letters.letter_length:
                    case 7:
                        print("difficile")
                        max_pts = 12
                    case 6:
                        print("moyen")
                        max_pts = 9
                    case _:
                        print("facile")
                        max_pts = 7

                self.point_earned = max_pts - len(self.answered)
                self.current_player.add_point(self.point_earned)
            elif len(self.answered) == 6:
                # nombre d'essai atteint (Defaite)
                # self.is_playing = False
                self.point_earned = 0
                self.defeat = True
                self.is_game_over = True
                print("defaite")

        # Bouton annuler
        self.screen.blit(self.cancel_image,
                         (20, self.screen.get_height() - self.cancel_image.get_height()))
        self.cancel_rect = pygame.Rect(20, self.screen.get_height() - self.cancel_image.get_height(), self.button_width, self.button_height)

        # Category
        self.screen.blit(self.category_image, (self.screen.get_width() / 2 - 310, 50))

        # Lettre
        for i in range(0, 6):
            for index, lettres in enumerate(self.wordle_letters.all_letters):
                self.screen.blit(lettres.pin, (self.letter_default_pos + (120 * index), 220 + (i * 140)))

        for i in range(0, len(self.answered)):
            for index, lettres in enumerate(self.wordle_letters.all_answer[i]):
                self.screen.blit(lettres.pin, (self.letter_default_pos + (120 * index), 220 + (i * 140)))

        # affichage de la réponse en cours
        index = 0
        for element in self.input_box.text:
            letter = self.font.render(element.upper(), True, (240, 255, 255))
            self.screen.blit(letter,
                             (self.letter_default_pos + (120 * index) + 30, 255 + (140 * len(self.answered))))
            index += 1
        row = 0

        # affichage des anciennes réponses
        for answer in self.answered:
            index = 0
            for element in answer:
                letter = self.font.render(element.upper(), True, (240, 255, 255))
                self.screen.blit(letter,
                                 (self.letter_default_pos + (120 * index) + 30, 255 + (140 * row)))
                index += 1
            row += 1

        if self.defeat:
            # On affiche le mot à deviner en cas d'echec
            word_to_find = self.font.render("{}".format(self.current_answer), True,
                                                (255, 255, 255))

            self.screen.blit(word_to_find, (1580, 200))

        if self.point_earned > 0:
            points_won = self.font.render("+{} points".format(self.point_earned), True,
                                                (255, 255, 255))
            self.screen.blit(points_won, (1580, 200))

