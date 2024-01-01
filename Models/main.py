import pygame

from Models.Screen.Selection_Player_Screen import Selection_Player_Screen
from Models.Screen.Game import Game
from Models.Screen.Selection_Round import Selection_Round
from Models.Screen.Screen_Round import Round
from Models.Buttons.Player.Players import Players

pygame.init()

# générer la fenêtre du jeu
pygame.display.set_caption("GRAND QUIZZ")
# Changement de la taille (position)
screen_width = 1500
screen_height = 1000
# screen = pygame.display.set_mode((screen_width, screen_height))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
background = pygame.transform.scale(pygame.image.load("../assets/background.jpg").convert_alpha(),
                                    (screen.get_width(), screen.get_height()))
# Temps d'affichage des tuiles finales en seconde
round_timer = 40000

# écran
game = Game(screen)
screen_round = Round(screen)
selection_player_screen = Selection_Player_Screen(screen)
selection_round = Selection_Round(screen)

running = True

# Event
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)
GET_TIME = pygame.USEREVENT + 1
pygame.time.set_timer(GET_TIME, 1000)
time_in_sec = round_timer
timer_for_sound = 0
current_round = 1
last_question_id = ""
point = 0
classement_round = 6
show_answer = False

while running:
    screen.blit(background, (0, 0))

    if game.is_playing:
        # Question
        game.update(time_in_sec, current_round == 0, show_answer, timer_for_sound)
    elif selection_player_screen.is_selecting_player:
        # Sélection du joueur
        selection_player_screen.update(screen)
    elif selection_round.is_selecting_round:
        # Selection de la manche
        if not selection_player_screen.has_Reorganized:
            selection_player_screen.reorganize_player_finale()
            selection_player_screen = Selection_Player_Screen(screen)
            game.current_player = Players("Player", 1)
            selection_player_screen.has_Reorganized = True

        selection_round.update()
    elif screen_round.is_round1_active:
        # Round 1
        selection_player_screen.has_Reorganized = False
        screen_round.update_round1(game.current_player)
        current_round = 1
    elif screen_round.is_round2_active:
        # Round 2
        selection_player_screen.has_Reorganized = False
        screen_round.update_round2(game.current_player)
        current_round = 2
    elif screen_round.is_round3_active:
        # Round 3
        selection_player_screen.has_Reorganized = False
        screen_round.update_round3(game.current_player)
        current_round = 3
    elif screen_round.is_round4_active:
        selection_player_screen.has_Reorganized = False
        screen_round.update_round4(game.current_player)
        current_round = 4
    elif screen_round.is_finale_active:
        # Finale
        selection_player_screen.has_Reorganized = False
       # if not selection_player_screen.has_Reorganized:
       #     selection_player_screen.reorganize_player_finale()
       #     selection_player_screen = Selection_Player_Screen(screen)
       #     selection_player_screen.has_Reorganized = True

        screen_round.update_finale(game.current_player, time_in_sec)
        current_round = 5
    elif screen_round.is_ranking_active:
        # Classement
        screen_round.update_Ranking(game.get_all_players_points())
        current_round = 6

    # Met à jour l'écran
    pygame.display.flip()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        else:
            if event.type == GET_TIME:
                time_in_sec -= 1
                timer_for_sound += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Click de souris
                if game.is_playing:
                    # Affichage des réponses
                    for button in game.group_button:
                        if button.rect.collidepoint(pygame.mouse.get_pos()):
                            game.show_answer = not game.show_answer
                        else:
                            game.show_answer = show_answer
                    if game.is_image_question:
                        if game.image_question_rect.collidepoint(event.pos):
                            game.zoom()
                        else:
                            game.is_zoomed = False
                    elif game.is_sound_question:
                        if game.image_question_rect.collidepoint(event.pos):
                            timer_for_sound = 0
                            game.display_sound()
                    if game.good_answer_rect.collidepoint(event.pos):
                        # Bonne réponse
                        game.stop_sound()
                        game.current_ID += 1
                        match current_round:
                            case 1:
                                point = 2
                            case 2:
                                point = 1
                            case 3:
                                point = 2
                            case 4:
                                point = 1
                            case 5:
                                if game.current_question_category == "Culture_G":
                                    # Culture G = 1 Pt
                                    point = 1
                                elif game.current_question_category == game.current_player.main_category_id:
                                    # Catégorie du joueur = 2 Pts
                                    point = 2
                                else:
                                    # Catégorie d'un autre joueur = 3 pts
                                    point = 3

                        game.current_player.add_point(point)
                        # selection_player_screen.set_points(game.current_player, point)

                    if game.bad_answer_rect.collidepoint(event.pos):
                        # Mauvaise réponse
                        game.current_ID += 1
                        game.stop_sound()
                    if game.cancel_rect.collidepoint(event.pos):
                        # Annuler
                        game.stop_sound()
                        game.current_ID = 0
                        game.is_playing = False
                        for button in screen_round.group_buttons_round1:
                            if button.name == last_question_id:
                                button.had_been_chosen = False
                        for button in screen_round.group_buttons_round2:
                            if button.name == last_question_id:
                                button.had_been_chosen = False
                        for button in screen_round.group_buttons_round3:
                            if button.name == last_question_id:
                                button.had_been_chosen = False
                        for button in screen_round.group_buttons_round4:
                            if button.name == last_question_id:
                                button.had_been_chosen = False
                        for button in screen_round.group_buttons_finale:
                            if button.question_id == last_question_id:
                                button.had_been_chosen = False
                elif selection_player_screen.is_selecting_player:
                    # Sélection du joueur
                    for button in selection_player_screen.group_buttons:
                        if button.rect.collidepoint(event.pos):
                            game.current_player = button.player
                            selection_player_screen.is_selecting_player = False
                    # Sélection du round
                elif selection_round.is_selecting_round:
                    for button in selection_round.group_buttons:
                        if button.rect.collidepoint(event.pos):
                            screen_round.is_round1_active = (button.round_id == 1)
                            screen_round.is_round2_active = (button.round_id == 2)
                            screen_round.is_round3_active = (button.round_id == 3)
                            screen_round.is_round4_active = (button.round_id == 4)
                            screen_round.is_finale_active = (button.round_id == 5)
                            screen_round.is_ranking_active = (button.round_id == 6)
                            running = (button.round_id != "Quit")
                            selection_player_screen.save_points()

                            time_in_sec = round_timer
                            selection_round.is_selecting_round = False
                else:
                    # sélection du joueur / Manche
                    if not selection_player_screen.is_selecting_player and current_round != classement_round:
                        for button in screen_round.group_buttons:
                            if button.rect.collidepoint(event.pos):
                                if button.category_id == 0:
                                    selection_player_screen.is_selecting_player = True
                                    selection_player_screen.save_points()

                    for button in screen_round.group_buttons_return_round:
                        if button.rect.collidepoint(event.pos):
                            if button.category_id == -10:
                                selection_round.is_selecting_round = True

                    # ROUND 1 (Récupération des questions par rapport à la catégorie sélectionnée)
                    if screen_round.is_round1_active:
                        if not selection_player_screen.is_selecting_player and not selection_round.is_selecting_round and not game.is_playing:
                            for button in screen_round.group_buttons_round1:
                                if button.rect.collidepoint(event.pos):
                                    time_in_sec = round_timer
                                    game.get_question(button.name)
                                    last_question_id = button.name
                                    button.had_been_chosen = True
                                    game.is_playing = True

                    # Round 2 (Récupération des questions par rapport à la catégorie sélectionnée)
                    if screen_round.is_round2_active:
                        if not selection_player_screen.is_selecting_player and not selection_round.is_selecting_round and not game.is_playing:
                            for button in screen_round.group_buttons_round2:
                                if button.rect.collidepoint(event.pos):
                                    time_in_sec = round_timer
                                    game.get_question(button.name)
                                    game.is_playing = True
                                    button.had_been_chosen = True
                                    last_question_id = button.name

                    # Round 3 (Récupération des questions par rapport à la catégorie sélectionnée)
                    if screen_round.is_round3_active:
                        if not selection_player_screen.is_selecting_player and not selection_round.is_selecting_round and not game.is_playing:
                            for button in screen_round.group_buttons_round3:
                                if button.rect.collidepoint(event.pos):
                                    time_in_sec = round_timer
                                    game.get_question(button.name)
                                    game.is_playing = True
                                    button.had_been_chosen = True
                                    last_question_id = button.name

                    # Round 4
                    if screen_round.is_round4_active:
                        if not selection_player_screen.is_selecting_player and not selection_round.is_selecting_round and not game.is_playing:
                            for button in screen_round.group_buttons_round4:
                                if button.rect.collidepoint(event.pos):
                                    time_in_sec = round_timer
                                    game.get_question(button.name)
                                    game.is_playing = True
                                    button.had_been_chosen = True
                                    last_question_id = button.name

                    # Finale (Récupération des questions par rapport à la question sélectionnée)
                    if screen_round.is_finale_active:
                        if not selection_player_screen.is_selecting_player and not selection_round.is_selecting_round:
                            for button in screen_round.group_buttons_finale:
                                if button.rect.collidepoint(event.pos):
                                    time_in_sec = round_timer
                                    game.get_final_question(button.question_id)
                                    game.is_playing = True
                                    button.had_been_chosen = True
                                    last_question_id = button.question_id


pygame.quit()
