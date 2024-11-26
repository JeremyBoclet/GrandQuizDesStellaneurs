import pygame

from Models.Buttons.Player.Player_Button_Logique import Player_Button_Logique


class LogiqueScreen:
    def __init__(self, screen):
        self.game_over = False
        self.screen = screen
        self.game_mode_id = 1500
        self.cancel_image = pygame.image.load("../Assets/Cancel.png")
        self.cancel_image = pygame.transform.scale(self.cancel_image,
                                                   (200, 65)).convert_alpha()
        self.category_image = pygame.image.load("../Assets/Round12.png")
        self.category_image = pygame.transform.scale(self.category_image,
                                                     (600, 150)).convert_alpha()

        self.cancel_rect = self.cancel_image.get_rect()
        self.font = pygame.font.SysFont("Futura-bold", 80)

        self.all_player = None
        self.all_player_group = pygame.sprite.Group()

    def set_all_player(self,all_player):
        self.all_player = all_player

        i = 0
        x = 0
        y = 0
        for player in self.all_player:
            i+= 1
            match i:
                case 1:
                    x = 100
                    y = 400
                case 2:
                    x = 200
                    y = 500
                case 3:
                    x = 300
                    y = 600
                case 4:
                    x = 400
                    y = 700
                case 5:
                    x = 500
                    y = 800
                case 6:
                    x = 1000
                    y = 800
                case 7:
                    x = 1100
                    y = 700
                case 8:
                    x = 1200
                    y = 600
                case 9:
                    x = 1300
                    y = 500
                case 10:
                    x = 1400
                    y = 400

            self.all_player_group.add(Player_Button_Logique(player.player_name,x,y,400,90))

    def get_players(self):
        return self.all_player_group

    def update(self):
        self.screen.blit(self.cancel_image,
                         (20, self.screen.get_height() - self.cancel_image.get_height()))
        self.cancel_rect = pygame.Rect(20, self.screen.get_height() - self.cancel_image.get_height(), 200, 65)

        # Category
        self.screen.blit(self.category_image, (self.screen.get_width() / 2 - 310, 50))
        self.all_player_group.draw(self.screen)