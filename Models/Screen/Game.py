import pygame

from Models.Bdd import Bdd
from Models.Buttons.Button import Button
from Models.Buttons.Player.Players import Players
from Models.Buttons.Player.PlayersRanking import PlayersRanking
from Models.Questions import Questions
from Models.Screen.Timer import Timer


class Game:
    def __init__(self, screen):
        self.is_playing = False
        self.screen = screen
        self.bdd = Bdd()
        self.questions = []
        self.players = []
        self.font = pygame.font.SysFont("Futura-bold", 80)
        self.question_font_color = (240, 255, 255)
        self.current_question = ""
        self.external_name = ""
        self.is_zoomed = False
        self.current_answer = ""
        self.current_question_category = 0
        self.current_answer_rect = pygame.Rect(0, 0, 0, 0)
        self.group_button = pygame.sprite.Group()
        self.group_button.add(Button("Hide_Answer", -2, (self.screen.get_width() / 2 - 750),
                                     self.screen.get_height() / 1.6, 1500, 150))
        self.view_cat_group = pygame.sprite.Group()

        self.show_answer = False

        self.current_ID = 0
        self.good_answer_text = ""
        self.current_player = Players("Denis", 1)
        self.button_width = 400
        self.button_height = 130

        self.image_question = ""
        self.image_question_rect = ""
        self.is_image_question = False
        self.is_sound_question = False
        self.is_displaying_sound = False

        self.cancel_image = pygame.image.load("../Assets/Cancel.png")
        self.cancel_image = pygame.transform.scale(self.cancel_image,
                                                   (200, 65)).convert_alpha()
        self.cancel_rect = self.cancel_image.get_rect()
        self.good_answer_image = pygame.image.load("../Assets/Good_Answer.png")
        self.good_answer_image = pygame.transform.scale(self.good_answer_image,
                                                        (self.button_width, self.button_height)).convert_alpha()
        self.good_answer_rect = self.good_answer_image.get_rect()

        self.bad_answer_image = pygame.image.load("../Assets/Bad_Answer.png")
        self.bad_answer_image = pygame.transform.scale(self.bad_answer_image,
                                                       (self.button_width, self.button_height)).convert_alpha()
        self.bad_answer_rect = self.bad_answer_image.get_rect()
        self.timer = Timer(self.screen)


    def get_all_players_points(self):
        # df = self.bdd.request_query("SELECT PlayerName, PlayerPoint FROM GrandQuiz.dbo.Players ORDER BY PlayerPoint DESC")
        df = self.bdd.get_players()
        df.reset_index()
        df = df.sort_values("Player_Points",ascending=False)
        self.players.clear()
        for index, row in df.iterrows():
            players = PlayersRanking(row["PlayerName"], row["Player_Points"])
            self.players.append(players)

        return self.players

    def get_category(self, current_category):
        self.view_cat_group.draw(self.screen)

        self.view_cat_group.empty()
        self.view_cat_group.add(Button(current_category, 1, self.screen.get_width() / 2 - 310, 50, 600, 150))

    def get_question(self, category_id):
        self.questions = []
        df = self.bdd.read_excel(category_id)
        print(category_id)
        # df = self.bdd.get_question(category_id)
        df.reset_index()
        for index, row in df.iterrows():
            question = Questions(row["Question"],
                                 row["Answer"],
                                 category_id,
                                 row["Category_Name"],
                                 row["TypeQuestion"],
                                 row["ExternalName"])

            self.questions.append(question)

    def get_question_round3(self, category_id):
        self.questions = []
        df = self.bdd.get_question_round3(category_id)
        df.reset_index()

        for index, row in df.iterrows():
            question = Questions(row["Question"], row["Answer"], row["Category_ID"], row["Category_Name"],
                                 row["TypeQuestion"], row["PathExternalQuestion"], row["ExternalName"])
            self.questions.append(question)

    def get_final_question(self, question_id):
        self.questions = []
        df = self.bdd.get_final_question(question_id)
        df.reset_index()
        for index, row in df.iterrows():
            question = Questions(row["Question"], row["Answer"], row["Category_ID"], row["Category_Name"],
                                 row["TypeQuestion"], row["PathExternalQuestion"], row["ExternalName"])
            self.questions.append(question)

    def get_question_excel(self):
        df = self.bdd.read_excel("Question")

    def zoom(self):
        self.is_zoomed = not self.is_zoomed

    def stop_sound(self):
        self.is_displaying_sound = False
        pygame.mixer.stop()

    def display_sound(self):
        self.is_displaying_sound = not self.is_displaying_sound

        if self.is_displaying_sound:
            sound = pygame.mixer.Sound("../Assets/Sounds/" + self.external_name)
            pygame.mixer.Sound.play(sound)
        else:
            pygame.mixer.stop()

    def update(self, time_in_sec, use_timer, always_show_answer):
        if self.current_ID == len(self.questions) or (time_in_sec <= 0 and use_timer):
            self.is_playing = False
            self.current_ID = 0

        else:
            # Question
            question_l1 = self.questions[self.current_ID].question.split('#')[0]
            question_l2 = self.questions[self.current_ID].question[len(question_l1) + 1:200]
            self.current_question_category = self.questions[self.current_ID].category_id

            self.current_question = self.font.render(question_l1, True, self.question_font_color)
            self.screen.blit(self.current_question, ((self.screen.get_width() - self.current_question.get_width()) / 2,
                                                     self.screen.get_height() / 4))

            self.current_question = self.font.render(question_l2, True, self.question_font_color)
            self.screen.blit(self.current_question, ((self.screen.get_width() - self.current_question.get_width()) / 2,
                                                     self.screen.get_height() / 3))

            good_answer_pos_x = (self.screen.get_width() - self.good_answer_image.get_width()) / 1.3
            good_answer_pos_y = self.screen.get_height() - self.good_answer_image.get_height()
            bad_answer_pos_x = (self.screen.get_width() - self.bad_answer_image.get_width()) / 4
            bad_answer_pos_y = self.screen.get_height() - self.bad_answer_image.get_height()

            # Réponse
            self.current_answer = self.font.render(self.questions[self.current_ID].answer, True, (255, 170, 0))
            self.current_answer_rect = pygame.Rect((self.screen.get_width() - self.current_answer.get_width()) / 2,
                                                   self.screen.get_height() / 1.6,
                                                   350,
                                                   100)

            self.screen.blit(self.current_answer,
                             ((self.screen.get_width() - self.current_answer.get_width()) / 2,
                              self.screen.get_height() / 1.5))

            if not self.show_answer and not always_show_answer:
                self.group_button.draw(self.screen)

            # Bonne réponse
            self.screen.blit(self.good_answer_image,
                             (good_answer_pos_x,
                              good_answer_pos_y))

            self.good_answer_rect = pygame.Rect(good_answer_pos_x,
                                                good_answer_pos_y, self.button_width, self.button_height)

            # Mauvaise Réponse
            self.screen.blit(self.bad_answer_image,
                             (bad_answer_pos_x,
                              bad_answer_pos_y))

            self.bad_answer_rect = pygame.Rect(bad_answer_pos_x,
                                               bad_answer_pos_y, self.button_width, self.button_height)

            # Nombre de bonnes réponses
            self.good_answer_text = self.font.render("Points : {}".format(self.current_player.total_point)
                                                     , True,
                                                     (255, 255, 255))
            self.screen.blit(self.good_answer_text,
                             ((self.screen.get_width() - self.good_answer_text.get_width()) / 2,
                              self.screen.get_height() - 60))

            # Bouton annuler
            self.screen.blit(self.cancel_image,
                             (20, self.screen.get_height() - self.cancel_image.get_height()))

            self.cancel_rect = pygame.Rect(20, self.screen.get_height() - self.cancel_image.get_height(), 200, 65)

            # affichage de la catégorie
            self.get_category(self.questions[self.current_ID].category_name)

            if self.questions[self.current_ID].type_question == "img":
                # Si image on la montre + zoomable sur clic
                self.external_name = self.questions[self.current_ID].external_name
                self.is_image_question = True
                self.is_sound_question = False

                # La question est une image
                self.image_question = pygame.image.load(
                    "../Assets/Annexe/" + self.questions[self.current_ID].external_name)

                if self.is_zoomed:
                    width = self.screen.get_width()
                    height = self.screen.get_height()
                else:
                    width = 300
                    height = 300

                self.image_question = pygame.transform.scale(self.image_question,
                                                             (width, height)).convert_alpha()

                if self.is_zoomed:
                    pos_x = 1
                    pos_y = 1
                else:
                    pos_x = ((self.screen.get_width() / 2) - self.image_question.get_width() / 2)
                    pos_y = self.screen.get_height() / 2 - self.image_question.get_height() + 110

                self.screen.blit(self.image_question,
                                 (pos_x, pos_y))

                self.image_question_rect = pygame.Rect(
                    pos_x,
                    pos_y, width, height)

            elif self.questions[self.current_ID].type_question == "audio":
                self.is_image_question = False
                self.is_sound_question = True
                # Si son, image de son + audio sur clic
                self.external_name = self.questions[self.current_ID].external_name

                self.is_displaying_sound = pygame.mixer.get_busy()

                if self.is_displaying_sound:
                    self.image_question = pygame.image.load("../Assets/stop_sound.png")
                else:
                    self.image_question = pygame.image.load("../Assets/sound.png")
                self.image_question = pygame.transform.scale(self.image_question,
                                                             (300, 300)).convert_alpha()

                pos_x = ((self.screen.get_width() / 2) - self.image_question.get_width() / 2)
                pos_y = self.screen.get_height() / 2 - self.image_question.get_height() + 110

                self.image_question_rect = pygame.Rect(
                    pos_x,
                    pos_y, 300, 300)

                self.screen.blit(self.image_question,
                                 (pos_x, pos_y))

            else:
                self.is_image_question = False
                self.is_sound_question = False

            if use_timer:
                self.timer.render(time_in_sec)



