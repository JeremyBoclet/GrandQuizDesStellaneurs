import pygame

from Models.Bdd import Bdd
from Models.Buttons.Player.Player_button import Player_button


class Selection_Player_Screen(pygame.sprite.Sprite):
    def __init__(self, screen):
        self.screen = screen
        self.is_selecting_player = False
        self.bdd = Bdd()
        self.group_buttons = pygame.sprite.Group()
        self.add_players()

        self.font = pygame.font.SysFont("Verdana", 30)

    def update(self, screen):
        self.group_buttons.draw(screen)
        for player in self.group_buttons:
            # Affiche le nombre de point du joueur courant
            player_point = self.font.render("Points : {}".format(player.player.total_point),
                                            True, (255, 255, 255))
            self.screen.blit(player_point, [player.rect.x + 230, player.rect.y + 100])

    def save_points(self):
        for player in self.group_buttons:
            # print("{} {}".format(player.player.name,player.player.total_point))
            self.bdd.execute_query("UPDATE GrandQuiz.dbo.Players SET PlayerPoint = {} WHERE PlayerName = '{}'".format(
                player.player.total_point, player.player.name))

    def set_points(self, current_player, point):
        for player in self.group_buttons:
            if player.player.name == current_player.name:
                player.player.total_point += point

    def add_players(self):
        y = 50
        x = 50
        df = self.bdd.read_excel("Players")
        # df = self.bdd.request_query("SELECT PlayerName, Main_Category FROM GrandQuiz.dbo.Players")
        df.reset_index()

        for index, row in df.iterrows():
            self.group_buttons.add(Player_button(row["PlayerName"], x, y, row["Main_Category"]))
            y += 150
            if y >= 801:
                y = 50
                x = 650

    def get_all_players(self):
        return self.group_buttons
