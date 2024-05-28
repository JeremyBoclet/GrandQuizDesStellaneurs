import math

import pygame
import random

from Models import Business
from Models.Bdd import Bdd
from Models.Buttons.Player.Players import Players
from Models.InputBox import InputBox
from Models.MoneyDropQuestion import MoneyDropQuestion


class DropScreen:
    def __init__(self, screen):
        self.is_playing = False
        self.game_over = False
        self.screen = screen

        self.current_player = Players("Player", 1)
        self.current_player_image = pygame.sprite.Group()
        self.current_player_name = ""

        self.button_width = 400
        self.button_height = 130

        self.font = pygame.font.SysFont("Futura-bold", 80)

        self.point_earned = 0
        self.point_earned_text = ""

        self.category_image = pygame.image.load("../Assets/Round8.png")
        self.category_image = pygame.transform.scale(self.category_image,
                                                     (600, 150)).convert_alpha()

        self.valid_image = pygame.image.load("../Assets/Valid.png")
        self.valid_image = pygame.transform.scale(self.valid_image,
                                                  (600, 150)).convert_alpha()
        self.valid_rect = self.valid_image.get_rect()

        self.loose_image = pygame.image.load("../Assets/Loose.png")
        self.loose_image = pygame.transform.scale(self.loose_image,
                                                  (800, 350)).convert_alpha()

        self.win_image = pygame.image.load("../Assets/Win.png")
        self.win_image = pygame.transform.scale(self.win_image,
                                                (800, 350)).convert_alpha()

        self.return_image = pygame.image.load("../Assets/Return.png")
        self.return_image = pygame.transform.scale(self.return_image,
                                                   (self.button_width, self.button_height)).convert_alpha()
        self.return_rect = self.return_image.get_rect()

        self.Next_image = pygame.image.load("../Assets/NextQuestion.png")
        self.Next_image = pygame.transform.scale(self.Next_image,
                                                 (600, 150)).convert_alpha()
        self.Next_rect = self.Next_image.get_rect()

        self.input_box_a = InputBox(450, 510, 200, 60, True, 70)
        self.input_box_b = InputBox(1150, 510, 200, 60, True, 70)
        self.input_box_c = InputBox(450, 720, 200, 60, True, 70)
        self.input_box_d = InputBox(1150, 720, 200, 60, True, 70)

        self.cancel_image = pygame.image.load("../Assets/Cancel.png")
        self.cancel_image = pygame.transform.scale(self.cancel_image,
                                                   (200, 65)).convert_alpha()
        self.cancel_rect = self.cancel_image.get_rect()

        self.current_question_l1 = ""
        self.current_question_l2 = ""

        self.answer_a = None
        self.answer_b = None
        self.answer_c = None
        self.answer_d = None
        self.right_answer = None

        self.wait_for_next_step = False
        self.defeat = False
        self.error_text = ""

        self.current_number_question = 0
        self.MAX_QUESTION = 8
        self.is_finale = False

        self.question = ""
        self.bdd = Bdd()
        self.all_questions = []
        df = self.bdd.read_excel("MoneyDrop")

        df.reset_index()
        for index, row in df.iterrows():
            question = MoneyDropQuestion(row["Question"],
                                         row["Answer"],
                                         row["Guess_A"],
                                         row["Guess_B"],
                                         row["Guess_C"],
                                         row["Guess_D"])

            self.all_questions.append(question)

        self.finale_answer = []
        self.final_input = []

    def raz_zone(self):
        self.input_box_a.text = "0"
        self.input_box_b.text = "0"
        self.input_box_c.text = "0"
        self.input_box_d.text = "0"

        self.input_box_a.change_color("")
        self.input_box_b.change_color("")
        self.input_box_c.change_color("")
        self.input_box_d.change_color("")

    def set_question(self):
        if len(self.all_questions) == 0:
            self.is_playing = False
            return

        self.current_number_question += 1
        self.is_finale = self.current_number_question == self.MAX_QUESTION

        r = list(range(0, len(self.all_questions)))
        random.shuffle(r)

        self.question = self.all_questions[r[0]]
        self.all_questions.pop(r[0])

        self.answer_a = self.font.render('A - ' + str(self.question.guess_A), True, (240, 255, 255))
        self.answer_b = self.font.render('B - ' + str(self.question.guess_B), True, (240, 255, 255))
        self.answer_c = self.font.render('C - ' + str(self.question.guess_C), True, (240, 255, 255))
        self.answer_d = self.font.render('D - ' + str(self.question.guess_D), True, (240, 255, 255))

        if str(self.question.answer).lower() == str(self.question.guess_A).lower():
            self.right_answer = self.input_box_a
        elif str(self.question.answer).lower() == str(self.question.guess_B).lower():
            self.right_answer = self.input_box_b
        elif str(self.question.answer).lower() == str(self.question.guess_C).lower():
            self.right_answer = self.input_box_c
        elif str(self.question.answer).lower() == str(self.question.guess_D).lower():
            self.right_answer = self.input_box_d
        else:
            self.error_text = Business.get_error_message(-1)

        # self.current_question = self.font.render(self.question.question, True, (240, 255, 255))

        # Question
        question_l1 = self.question.question.split('#')[0]
        question_l2 = self.question.question[len(question_l1) + 1:200]

        self.current_question_l1 = self.font.render(question_l1, True, (240, 255, 255))
        self.current_question_l2 = self.font.render(question_l2, True, (240, 255, 255))

        if self.is_finale:
            self.set_final_answers()

    def check_input(self):
        error_code = 0

        # check de 3 choix max
        if ((self.input_box_a.text != "" and int(self.input_box_a.text) != 0) and not self.is_finale
                and (self.input_box_b.text != "" and int(self.input_box_b.text) != 0)
                and (self.input_box_c.text != "" and int(self.input_box_c.text) != 0)
                and (self.input_box_d.text != "" and int(self.input_box_d.text) != 0)):
            error_code = 1
        else:
            # Check du montant saisie < montant restant
            input_amount = ((int(self.input_box_a.text) if self.input_box_a.text != "" else 0)
                            + (int(self.input_box_b.text) if self.input_box_b.text != "" else 0)
                            + (int(self.input_box_c.text) if self.input_box_c.text != "" else 0)
                            + (int(self.input_box_d.text) if self.input_box_d.text != "" else 0))

            if input_amount > self.current_player.remaining_md_point:
                error_code = 2
            elif input_amount != self.current_player.remaining_md_point:
                # check que le montant restant = montant max
                error_code = 3

        if self.is_finale:
            count_input = 0
            for i in self.final_input:
                if i.text != "" and int(i.text) != 0:
                    count_input += 1

            if count_input > 1:
                error_code = 4

        self.error_text = Business.get_error_message(error_code)

    def set_final_answers(self):
        answer_list = [self.input_box_a, self.input_box_b, self.input_box_c, self.input_box_d]
        self.final_input.clear()
        self.finale_answer.clear()

        self.final_input.append(self.right_answer)

        good_answer_index = 0
        # Affichage de la bonne reponse
        for index, answer in enumerate(answer_list):
            if self.right_answer == answer:
                good_answer_index = index
                match index:
                    case 0:
                        self.finale_answer.append([self.answer_a, (450, 450)])
                    case 1:
                        self.finale_answer.append([self.answer_b, (1150, 450)])
                    case 2:
                        self.finale_answer.append([self.answer_c, (450, 650)])
                    case 3:
                        self.finale_answer.append([self.answer_d, (1150, 650)])

        # Affichage d'une mauvaise réponse de manière aléatoire
        r = list(range(0, len(answer_list)))
        random.shuffle(r)

        index_to_show = r[0] if good_answer_index != r[0] else r[1]
        for index, answer in enumerate(answer_list):
            if index == index_to_show:
                match index:
                    case 0:
                        self.finale_answer.append([self.answer_a, (450, 450)])
                        self.final_input.append(self.input_box_a)
                    case 1:
                        self.finale_answer.append([self.answer_b, (1150, 450)])
                        self.final_input.append(self.input_box_b)
                    case 2:
                        self.finale_answer.append([self.answer_c, (450, 650)])
                        self.final_input.append(self.input_box_c)
                    case 3:
                        self.finale_answer.append([self.answer_d, (1150, 650)])
                        self.final_input.append(self.input_box_d)

    def valid_input(self):
        if not self.wait_for_next_step:
            # Première validation
            self.wait_for_next_step = True
            self.input_box_a.change_color(
                "green") if self.input_box_a == self.right_answer else self.input_box_a.change_color("red")
            self.input_box_b.change_color(
                "green") if self.input_box_b == self.right_answer else self.input_box_b.change_color("red")
            self.input_box_c.change_color(
                "green") if self.input_box_c == self.right_answer else self.input_box_c.change_color("red")
            self.input_box_d.change_color(
                "green") if self.input_box_d == self.right_answer else self.input_box_d.change_color("red")

            self.defeat = self.right_answer.text == "0" or self.right_answer.text == ""
        else:
            # Question suivante
            self.wait_for_next_step = False

            remaining_point = Business.int_try_parse(self.right_answer.text)
            if remaining_point is None:
                remaining_point = 0

            self.current_player.set_md_point(remaining_point)

            self.set_question()
            self.raz_zone()

    def blit_answer(self):
        if self.is_finale:
            for i in self.finale_answer:
                self.screen.blit(i[0], i[1])

            for i in self.final_input:
                i.draw(self.screen)
        else:
            # Réponses
            self.screen.blit(self.answer_a, (450, 450))
            self.screen.blit(self.answer_b, (1150, 450))
            self.screen.blit(self.answer_c, (450, 650))
            self.screen.blit(self.answer_d, (1150, 650))

            # Saisie des réponses
            self.input_box_a.draw(self.screen)
            self.input_box_b.draw(self.screen)
            self.input_box_c.draw(self.screen)
            self.input_box_d.draw(self.screen)

    def update(self):
        self.limit_text()

        self.input_box_a.update()
        self.input_box_b.update()
        self.input_box_c.update()
        self.input_box_d.update()

        if self.current_player_name != self.current_player.name:
            self.current_player_image = pygame.image.load(
                "../Assets/Player/{}.png".format(self.current_player.name)).convert_alpha()
            self.current_player_image = pygame.transform.scale(self.current_player_image, (400, 100))
            self.current_player_name = self.current_player.name

        self.screen.blit(self.current_player_image, (1500, 5))

        # Nombre de bonnes réponses
        good_answer_text = self.font.render("Points : {}".format(self.current_player.total_point)
                                            , True,
                                            (255, 255, 255))

        self.screen.blit(good_answer_text,
                         (1580,110))

        if not self.wait_for_next_step:
            self.check_input()

        # Bouton annuler
        self.screen.blit(self.cancel_image,
                         (20, self.screen.get_height() - self.cancel_image.get_height()))
        self.cancel_rect = pygame.Rect(20, self.screen.get_height() - self.cancel_image.get_height(), 200, 65)

        self.screen.blit(self.category_image, (self.screen.get_width() / 2 - 310, 50))

        # question
        self.screen.blit(self.current_question_l1,
                         ((self.screen.get_width() - self.current_question_l1.get_width()) / 2,
                          self.screen.get_height() / 4))
        self.screen.blit(self.current_question_l2,
                         ((self.screen.get_width() - self.current_question_l2.get_width()) / 2,
                          self.screen.get_height() / 3))

        # Montant max et restant
        maximum_money = self.font.render('Maximum : ' + str(self.current_player.maximum_md_point) + '€', True,
                                         (240, 255, 255))
        self.screen.blit(maximum_money, (10, 60))

        remaining_money = (self.current_player.remaining_md_point
                           - int(self.input_box_a.text if self.input_box_a.text != "" else 0)
                           - int(self.input_box_b.text if self.input_box_b.text != "" else 0)
                           - int(self.input_box_c.text if self.input_box_c.text != "" else 0)
                           - int(self.input_box_d.text if self.input_box_d.text != "" else 0))

        remaining_money_font = self.font.render('Restant : ' + str(remaining_money) + '€', True,
                                                (0, 255, 0) if remaining_money >= 0 else (255, 0, 0))
        self.screen.blit(remaining_money_font, (10, 140))

        self.blit_answer()

        # Message d'erreur
        if self.error_text != "":
            error_font = self.font.render(self.error_text, False, (255, 0, 0))
            self.screen.blit(error_font, (self.screen.get_width() / 2 - error_font.get_width() / 2,
                                          self.screen.get_height() - self.valid_image.get_height() - 75))
        else:
            if self.wait_for_next_step:
                if self.defeat:
                    self.screen.blit(self.loose_image, (self.screen.get_width() / 2 - self.loose_image.get_width() / 2,
                                                        self.screen.get_height() - self.loose_image.get_height()))
                    self.show_return_button()
                    self.game_over = True
                elif self.current_number_question == self.MAX_QUESTION:
                    self.screen.blit(self.win_image, (self.screen.get_width() / 2 - self.win_image.get_width() / 2,
                                                      self.screen.get_height() - self.win_image.get_height()))
                    self.show_return_button()

                    point = math.ceil(self.current_player.remaining_md_point / 1000)
                    self.point_earned_text = self.font.render(
                        "+ {} points".format(point), True,
                        (255, 255, 255))

                    self.screen.blit(self.point_earned_text,
                                     (self.screen.get_width() / 2 - self.point_earned_text.get_width() / 2,
                                      self.screen.get_height() - self.point_earned_text.get_height()))

                    if not self.game_over:
                        self.game_over = True
                        self.current_player.add_point(point)
                else:
                    # Next step
                    self.screen.blit(self.Next_image, (
                        self.screen.get_width() / 2 - 310, self.screen.get_height() - self.Next_image.get_height()))

                    self.Next_rect = pygame.Rect(self.screen.get_width() / 2 - 310,
                                                 self.screen.get_height() - self.Next_image.get_height(), 600, 150)

            else:
                # Valider
                self.screen.blit(self.valid_image,
                                 (self.screen.get_width() / 2 - 310,
                                  self.screen.get_height() - self.valid_image.get_height()))

                self.valid_rect = pygame.Rect(self.screen.get_width() / 2 - 310,
                                              self.screen.get_height() - self.valid_image.get_height(), 600, 150)

    def limit_text(self):
        self.input_box_a.text = self.input_box_a.text[:len(str(self.current_player.maximum_md_point))]
        self.input_box_b.text = self.input_box_b.text[:len(str(self.current_player.maximum_md_point))]
        self.input_box_c.text = self.input_box_c.text[:len(str(self.current_player.maximum_md_point))]
        self.input_box_d.text = self.input_box_d.text[:len(str(self.current_player.maximum_md_point))]

    def reset_game(self):
        self.raz_zone()
        self.current_number_question = 0
        self.current_player.set_md_point(250000)
        self.set_question()
        self.defeat = False
        self.game_over = False
        self.is_finale = False
        self.wait_for_next_step = False

    def show_return_button(self):
        self.screen.blit(self.return_image,
                         (20, self.screen.get_height() - self.return_image.get_height()))

        self.return_rect = pygame.Rect(20,
                                       self.screen.get_height() - self.return_image.get_height(),
                                       self.button_width,
                                       self.button_height)



