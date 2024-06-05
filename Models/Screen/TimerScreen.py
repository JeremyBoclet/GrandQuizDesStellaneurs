import pygame

from Models.Buttons.Player.Players import Players


class TimerScreen:
    def __init__(self, screen):
        self.is_playing = False
        self.game_over = False
        self.screen = screen

        self.cancel_image = pygame.image.load("../Assets/Cancel.png")
        self.cancel_image = pygame.transform.scale(self.cancel_image,
                                                   (200, 65)).convert_alpha()
        self.category_image = pygame.image.load("../Assets/Round10.png")
        self.category_image = pygame.transform.scale(self.category_image,
                                                     (600, 150)).convert_alpha()

        self.cancel_rect = self.cancel_image.get_rect()
        self.current_player = Players("Player", 1)
        self.current_player_image = pygame.sprite.Group()
        self.current_player_name = ""
        self.font_timer = pygame.font.SysFont("Verdana", 100)
        self.font = pygame.font.SysFont("Futura-bold", 80)

        self.stop_timer = False

        self.stop_button_image = pygame.image.load("../Assets/Stop_Timer.png")
        self.stop_button_image = pygame.transform.scale(self.stop_button_image,
                                                     (300, 300)).convert_alpha()
        self.stop_button_rect = self.stop_button_image.get_rect()
        self.MAX_POINT = 10
        self.LIMIT = 0.5
        self.game_over = False
        self.points_won = 0

    def update(self, timer):
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
                         ((self.screen.get_width() - good_answer_text.get_width()) / 2,
                          self.screen.get_height() - 60))

        self.screen.blit(self.cancel_image,
                         (20, self.screen.get_height() - self.cancel_image.get_height()))
        self.cancel_rect = pygame.Rect(20, self.screen.get_height() - self.cancel_image.get_height(), 200, 65)

        # Category
        self.screen.blit(self.category_image, (self.screen.get_width() / 2 - 310, 50))

        # Stop Button
        self.screen.blit(self.stop_button_image, (self.screen.get_width() / 2 - 150, 530))
        self.stop_button_rect = pygame.Rect(self.screen.get_width() / 2 - 150, 530, 300, 300)

        # Affichage du timer
        if timer <= 50 or self.stop_timer:
            timer_render = self.font_timer.render((timer/10).__str__(), True, (240, 255, 255))

            self.screen.blit(timer_render, ((self.screen.get_width() - timer_render.get_width()) / 2,
                                            self.screen.get_height() / 3))

        if self.stop_timer :
            # fin du jeu, calcul des points
            if not self.game_over:
                self.game_over = True
                gap = abs(timer / 10 - self.MAX_POINT)
                point_earned = int(self.MAX_POINT - (gap / self.LIMIT * self.MAX_POINT))
                self.points_won = self.font.render("{} points".format(point_earned), True,
                                              (255, 255, 255))

                self.current_player.add_point(point_earned)

            self.screen.blit(self.points_won, (1580, 120))


