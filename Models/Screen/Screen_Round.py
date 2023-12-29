import random

import pygame

from Models.Buttons.Button import Button
from Models.Buttons.Category.Return_Round import Return_Round
from Models.Buttons.Final_Button import Final_Button
from Models.Buttons.Player.Current_Player import Current_Player
from Models.Buttons.Player.Players import Players
from Models.Screen.Timer import Timer

default_button = "Button_template2"

class Round:
    def __init__(self, screen):
        self.is_round1_active = False
        self.is_round2_active = False
        self.is_round3_active = False
        self.is_round4_active = False
        self.is_finale_active = False
        self.is_ranking_active = False

        self.screen = screen

        self.hide_final = False
        self.timer = Timer(self.screen)

        self.group_buttons = pygame.sprite.Group()

        self.group_buttons_return_round = pygame.sprite.Group()
        self.group_buttons_return_round.add(Return_Round(1))

        # Round 1 (Question theme choisi)
        self.group_buttons_round1 = pygame.sprite.Group()
        self.add_round1_button()

        # Round 2 (Question theme generale)
        self.group_buttons_round2 = pygame.sprite.Group()
        self.add_round2_button()

        # Round 3
        self.group_buttons_round3 = pygame.sprite.Group()
        self.add_round3_button()

        # Round 4
        self.group_buttons_round4 = pygame.sprite.Group()
        self.add_round4_button()

        # Round Finale
        self.group_buttons_finale = pygame.sprite.Group()
        self.final_category = []
        self.add_finale_button()

        # Round Classement
        self.group_buttons_ranking = pygame.sprite.Group()
        self.add_ranking_button()

        self.font = pygame.font.SysFont("Verdana", 30)
        self.select_player(Players("Denis", 1), 1)

    def update_round1(self, current_player):
        self.already_answered()
        self.group_buttons_round1.draw(self.screen)
        self.select_player(current_player, 1)

    def update_round2(self, current_player):
        self.already_answered()
        self.group_buttons_round2.draw(self.screen)
        self.select_player(current_player, 2)

    def update_round3(self, current_player):
        self.already_answered()
        self.group_buttons_round3.draw(self.screen)
        self.select_player(current_player, 3)

    def update_round4(self, current_player):
        self.already_answered()
        self.group_buttons_round4.draw(self.screen)
        self.select_player(current_player,4)

    def update_finale(self, current_player, time_in_sec):
        if time_in_sec == 0 and not self.hide_final:
            self.hide_final = True
            self.hide_final_button()
        elif time_in_sec >= 0 and not self.hide_final:
            self.timer.render(time_in_sec)

        self.already_answered()
        self.group_buttons_finale.draw(self.screen)

        for button in self.group_buttons_finale:
            question_num = button.get_num()
            if question_num < 10:
                x = button.rect.x + 50
            else:
                x = button.rect.x + 35

            y = button.rect.y + 30

            self.screen.blit(button.get_question_num(), (x, y))

        self.select_player(current_player, 5)

    def update_Ranking(self, all_players):
        self.group_buttons_return_round.empty()
        self.group_buttons_return_round.add(Return_Round(6))
        self.group_buttons_return_round.draw(self.screen)

        self.group_buttons_ranking.draw(self.screen)

        count = 0
        has_changed_row = False
        for player in all_players:
            count += 1
            match count:
                case 1:
                    x = 800
                    y = 180
                    self.show_ranking(x, y, player.player_name, player.player_point)

                case 2:
                    x = 340
                    y = 360
                    self.show_ranking(x, y, player.player_name, player.player_point)

                case 3:
                    x = 1300
                    y = 360
                    self.show_ranking(x, y, player.player_name, player.player_point)

                case _:
                    x = (count * 20) + (count - 4) * 450
                    y = 530
                    if count >= 8 or has_changed_row:
                        if not has_changed_row:
                            count = 4
                            x = 80

                        y = 630
                        has_changed_row = True
                    self.show_ranking(x, y, player.player_name, player.player_point)

    def show_ranking(self, x, y, player_name, player_point):
        player_point = self.font.render("{} - {} Pts".format(player_name, player_point), True,
                                        (0, 0, 0))
        self.screen.blit(player_point, [x, y])

    def select_player(self, current_player, current_round):
        self.group_buttons.draw(self.screen)
        # Supprime l'ancien joueur et ajoute le joueur courant
        for button in self.group_buttons:
            if button.category_id == 0 or button.category_id == -10:
                self.group_buttons.remove(button)
        self.group_buttons.add(Current_Player("{}.png".format(current_player.name)))

        self.group_buttons_return_round.empty()
        self.group_buttons_return_round.add(Return_Round(current_round))
        self.group_buttons_return_round.draw(self.screen)

        # Affiche le nombre de point du joueur courant
        player_point = self.font.render("Points : {}".format(current_player.total_point),
                                        True, (255, 255, 255))

        self.screen.blit(player_point, [self.screen.get_width() / 2 - 80, 10])

    def already_answered(self):
        for button in self.group_buttons_round1:
            if button.had_been_chosen:
                self.group_buttons_round1.remove(button)

        for button in self.group_buttons_round2:
            if button.had_been_chosen:
                self.group_buttons_round2.remove(button)

        for button in self.group_buttons_round3:
            if button.had_been_chosen:
                self.group_buttons_round3.remove(button)

        for button in self.group_buttons_round4:
            if button.had_been_chosen:
                self.group_buttons_round4.remove(button)

        for button in self.group_buttons_finale:
            if button.had_been_chosen:
                self.group_buttons_finale.remove(button)

    def add_round1_button(self):
        self.group_buttons_round1.add(Button("Martin", 350, 200, 600, 150))
        self.group_buttons_round1.add(Button("Ben", 350, 350, 600, 150))
        self.group_buttons_round1.add(Button("PTF", 350, 500, 600, 150))
        self.group_buttons_round1.add(Button("Zejoe", 350, 650, 600, 150))
        self.group_buttons_round1.add(Button("Mathis", 350, 800, 600, 150))

        self.group_buttons_round1.add(Button("Jeanjarjar", 1000, 200, 600, 150))
        self.group_buttons_round1.add(Button("Drakmur", 1000, 350, 600, 150))
        self.group_buttons_round1.add(Button("Plags", 1000, 500, 600, 150))
        self.group_buttons_round1.add(Button("GrosLombaire", 1000, 650, 600, 150))
        self.group_buttons_round1.add(Button(default_button, 1000, 800, 600, 150))

    def add_round2_button(self):
        self.group_buttons_round2.add(Button("Gaming", 40, 250, 550, 110))
        self.group_buttons_round2.add(Button("Stellan", 40, 360, 550, 110))
        self.group_buttons_round2.add(Button("Religion", 40, 470, 550, 110))
        self.group_buttons_round2.add(Button("LoL", 40, 580, 550, 110))
        self.group_buttons_round2.add(Button("Automobile", 40, 690, 550, 110))
        self.group_buttons_round2.add(Button("Mystery", 40, 800, 550, 110))

        self.group_buttons_round2.add(Button("Geo", 670, 250, 550, 110))
        self.group_buttons_round2.add(Button("History", 670, 360, 550, 110))
        self.group_buttons_round2.add(Button("Animals", 670, 470, 550, 110))
        self.group_buttons_round2.add(Button("Formula1", 670, 580, 550, 110))
        self.group_buttons_round2.add(Button("Sport", 670, 690, 550, 110))
        self.group_buttons_round2.add(Button("CodeRoute", 670, 800, 550, 110))

        self.group_buttons_round2.add(Button("Pixar", 1300, 250, 550, 110))
        self.group_buttons_round2.add(Button(default_button, 1300, 360, 550, 110))
        self.group_buttons_round2.add(Button(default_button, 1300, 470, 550, 110))
        self.group_buttons_round2.add(Button(default_button, 1300, 580, 550, 110))
        self.group_buttons_round2.add(Button("Dreamworks", 1300, 690, 550, 110))
        self.group_buttons_round2.add(Button(default_button, 1300, 800, 550, 110))


        self.group_buttons_round2.add(Button("TranslatedMusique", 350, 910, 550, 110))
        self.group_buttons_round2.add(Button("Gastronomy", 1000, 910, 550, 110))

    def add_round3_button(self):
        self.group_buttons_round3.add(Button("RE_Martin", 350, 200, 600, 150))
        self.group_buttons_round3.add(Button("RE_Ben", 350, 350, 600, 150))
        self.group_buttons_round3.add(Button("RE_PTF", 350, 500, 600, 150))
        self.group_buttons_round3.add(Button("RE_Zejoe", 350, 650, 600, 150))
        self.group_buttons_round3.add(Button("RE_Mathis", 350, 800, 600, 150))

        self.group_buttons_round3.add(Button("RE_Jeanjarjar", 1000, 200, 600, 150))
        self.group_buttons_round3.add(Button("RE_Drakmur", 1000, 350, 600, 150))
        self.group_buttons_round3.add(Button("RE_Plags", 1000, 500, 600, 150))
        self.group_buttons_round3.add(Button("RE_GrosLombaire", 1000, 650, 600, 150))
        self.group_buttons_round3.add(Button(default_button, 1000, 800, 600, 150))

    def add_round4_button(self):
        self.group_buttons_round4.add(Button("LoL_Ban", 40, 250, 550, 110))
        self.group_buttons_round4.add(Button("LoL_Pick", 40, 360, 550, 110))
        self.group_buttons_round4.add(Button("Audio_Jeux", 40, 470, 550, 110))
        self.group_buttons_round4.add(Button("Audio_Serie", 40, 580, 550, 110))
        self.group_buttons_round4.add(Button("Pub", 40, 690, 550, 110))
        self.group_buttons_round4.add(Button("Disney", 40, 800, 550, 110))

        self.group_buttons_round4.add(Button("Dessin_Anime", 670, 250, 550, 110))
        self.group_buttons_round4.add(Button("Hymne", 670, 360, 550, 110))
        self.group_buttons_round4.add(Button("Audio_Film", 670, 470, 550, 110))
        self.group_buttons_round4.add(Button("Emission", 670, 580, 550, 110))
        self.group_buttons_round4.add(Button("Musique1980", 670, 690, 550, 110))
        self.group_buttons_round4.add(Button("Musique2000", 670, 800, 550, 110))

        self.group_buttons_round4.add(Button("Anime", 1300, 250, 550, 110))
        self.group_buttons_round4.add(Button("Button_template2", 1300, 360, 550, 110))
        self.group_buttons_round4.add(Button("Button_template2", 1300, 470, 550, 110))
        self.group_buttons_round4.add(Button("Button_template2", 1300, 580, 550, 110))
        self.group_buttons_round4.add(Button("Button_template2", 1300, 690, 550, 110))
        self.group_buttons_round4.add(Button("Button_template2", 1300, 800, 550, 110))

        self.group_buttons_round4.add(Button("Rap", 1000, 910, 550, 110))
        self.group_buttons_round4.add(Button("Button_template2", 350, 910, 550, 110))

    def add_finale_button(self):
        button_id = 0
        question_id = 0
        category_id = 1

        # Doit suivre l'ordre dans la feuille "Finale"
        colors = ["Shit_Green", "Red", "Black", "Purple", "Brown", "Dark_Blue", "Light_Blue", "Green", "Orange", "White"]

        for color in colors:
            # Boucle changement de theme
            category_id += 1
            for i in range(0, 6):
                # Boucle des questions
                question_id += 1
                button_id += 1
                self.final_category.append({'id': button_id,
                                            'color': color,
                                            'id_question': question_id,
                                            'id_category': category_id,
                                            'x': 0,
                                            'y': 0})

        # 2 questions CG, car 8x6 = 48 et on veut 50 questions (8 = joueurs (+CG) / 7 = nombre de questions par joueur)
        # for i in range(0, 2):
        #     question_id += 1
        #     button_id += 1
        #     self.final_category.append({'id': button_id,
        #                                 'color': "White",
        #                                 'id_question': question_id,
        #                                 'id_category': 0,
        #                                 'x': 0,
        #                                 'y': 0})

        r = list(range(1, 61))
        random.shuffle(r)
        count = 0
        x = -1
        y = 0
        for i in r:
            count += 1
            x += 1
            if x == 12:
                x = 0
                y += 1

            for final_cat in self.final_category:
                if final_cat['id'] == i:
                    final_cat['x'] = 70 + x * 150
                    final_cat['y'] = 215 + y * 170
                    final_cat['count'] = count
                    self.group_buttons_finale.add(Final_Button(final_cat["color"],
                                                               final_cat["id_question"],
                                                               final_cat['x'],
                                                               final_cat['y'],
                                                               count,
                                                               final_cat["id_category"]))

    def hide_final_button(self):
        self.group_buttons_finale.empty()
        for final_cat in self.final_category:
            self.group_buttons_finale.add(Final_Button("Hide_Final",
                                                       final_cat["id_question"],
                                                       final_cat['x'],
                                                       final_cat['y'],
                                                       final_cat['count'],
                                                       final_cat["id_category"]))

    def add_ranking_button(self):
        self.group_buttons_ranking.add(Button("First", self.screen.get_width() / 2 - 325, 0, 600, 275))
        self.group_buttons_ranking.add(Button("Second", self.screen.get_width() / 2 - 825, 300, 600, 150))
        self.group_buttons_ranking.add(Button("Third", self.screen.get_width() / 2 + 180, 300, 600, 150))

        self.group_buttons_ranking.add(Button("ForthOrMore", 30, 500, 450, 100))
        self.group_buttons_ranking.add(Button("ForthOrMore", 490, 500, 450, 100))
        self.group_buttons_ranking.add(Button("ForthOrMore", 950, 500, 450, 100))
        self.group_buttons_ranking.add(Button("ForthOrMore", 1410, 500, 450, 100))

        self.group_buttons_ranking.add(Button("ForthOrMore", 30, 600, 450, 100))
        self.group_buttons_ranking.add(Button("ForthOrMore", 490, 600, 450, 100))
        self.group_buttons_ranking.add(Button("ForthOrMore", 950, 600, 450, 100))
        # self.group_buttons_ranking.add(Button("ForthOrMore", 1410, 600, 450, 100))
