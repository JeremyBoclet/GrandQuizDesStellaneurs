import pygame

from Models.Business import convert_difficulty_to_number_password
from Models.Business import convert_difficulty_to_number_wordle
from Models.ProjectG.ProjectGGame import ProjectGGame
from Models.Screen.DropScreen import DropScreen
from Models.Screen.Selection_Player_Screen import Selection_Player_Screen
from Models.Screen.Game import Game
from Models.Screen.PasswordScreen import PasswordScreen
from Models.Screen.TimerScreen import TimerScreen
from Models.Screen.WordleScreen import WordleScreen
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
round_timer = 30

# écran
QUIZ = True
game = Game(screen)
PasswordScreen = PasswordScreen(screen)
MoneyDropScreen = DropScreen(screen)
WordleScreen = WordleScreen(screen)
TimerScreen = TimerScreen(screen)
screen_round = Round(screen, QUIZ)
selection_player_screen = Selection_Player_Screen(screen)
selection_round = Selection_Round(screen, QUIZ)
ProjectG = ProjectGGame(screen)
running = True

# Event
GET_TIME = pygame.USEREVENT + 1
GET_TIME_ROUND = pygame.USEREVENT + 2
pygame.time.set_timer(GET_TIME, 1000)
pygame.time.set_timer(GET_TIME_ROUND, 100)

GET_TIME_PROJECTG = pygame.USEREVENT + 3
pygame.time.set_timer(GET_TIME_PROJECTG, 1000)

time_in_sec = round_timer
timer_for_sound = 0
timer_for_round = 0
timer_for_projectg = 0
current_round = 1
last_question_id = ""
point = 0
classement_round = 6
show_answer = False
current_game_mode = 0

current_game_mode = ProjectG.game_mode_id

while running:
    screen.blit(background, (0, 0))

    if game.is_playing:
        # Question
        game.update(time_in_sec, current_round == 0, show_answer, timer_for_sound)
    elif current_game_mode == PasswordScreen.game_mode_ID:
        PasswordScreen.current_player = game.current_player
        PasswordScreen.update()
    elif current_game_mode == MoneyDropScreen.game_mode_id:
        MoneyDropScreen.current_player = game.current_player
        MoneyDropScreen.update()
    elif current_game_mode == WordleScreen.game_mode_id:
        WordleScreen.current_player = game.current_player
        WordleScreen.update()
    elif current_game_mode == TimerScreen.game_mode_id:
        TimerScreen.current_player = game.current_player
        TimerScreen.update(timer_for_round)
    elif current_game_mode == ProjectG.game_mode_id:
        ProjectG.update()
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
    elif screen_round.is_round7_active:
        # Mot de passe
        selection_player_screen.has_Reorganized = False
        screen_round.update_round7(game.current_player)
        current_round = 7
    elif screen_round.is_round_drop_active:
        # Money Drop
        selection_player_screen.has_Reorganized = False
        screen_round.update_round_drop(game.current_player)
        current_round = 8
    elif screen_round.is_round_wordle_active:
        # Wordle
        selection_player_screen.has_Reorganized = False
        screen_round.update_round_wordle(game.current_player)
        current_round = 9
    elif screen_round.is_round_timer_active:
        # Timer ROUND
        selection_player_screen.has_Reorganized = False
        screen_round.update_round_timer(game.current_player)
        current_round = 10
    elif screen_round.is_round_projectG_active:
        # Project G ROUND
        selection_player_screen.has_Reorganized = False
        screen_round.update_round_projectg(game.current_player)
        current_round = 11
    # Met à jour l'écran
    pygame.display.flip()
    pygame.display.update()

    if not current_game_mode == ProjectG.game_mode_id:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            else:
                if event.type == GET_TIME:
                    time_in_sec -= 1
                    timer_for_sound += 1
                if event.type == GET_TIME_ROUND and not TimerScreen.stop_timer:
                    timer_for_round += 1
                if event.type == GET_TIME_PROJECTG:
                    timer_for_projectg += 1
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
                    elif current_game_mode == PasswordScreen.game_mode_ID:
                        # PASSWORD *******************************************
                        if PasswordScreen.cancel_rect.collidepoint(event.pos) or (
                                PasswordScreen.game_over and PasswordScreen.return_rect.collidepoint(event.pos)):
                            # Annuler
                            current_game_mode = 0
                            PasswordScreen.game_over = False
                        if not PasswordScreen.game_over:
                            if PasswordScreen.good_answer_rect.collidepoint(event.pos):
                                PasswordScreen.set_answer("valid")
                                PasswordScreen.set_password()
                            elif PasswordScreen.bad_answer_rect.collidepoint(event.pos):
                                PasswordScreen.set_answer("error")
                                PasswordScreen.set_password()
                    elif current_game_mode == MoneyDropScreen.game_mode_id:
                        # MONEY DROP *******************************************
                        if MoneyDropScreen.wait_for_next_step:
                            if MoneyDropScreen.Next_rect.collidepoint(
                                    event.pos) and not MoneyDropScreen.is_finale and not MoneyDropScreen.game_over:
                                MoneyDropScreen.valid_input()
                        else:
                            MoneyDropScreen.input_box_a.handle_event(event)
                            MoneyDropScreen.input_box_b.handle_event(event)
                            MoneyDropScreen.input_box_c.handle_event(event)
                            MoneyDropScreen.input_box_d.handle_event(event)

                            if MoneyDropScreen.error_text == "" and MoneyDropScreen.valid_rect.collidepoint(event.pos):
                                # Valider
                                MoneyDropScreen.valid_input()
                        if MoneyDropScreen.cancel_rect.collidepoint(event.pos) or (
                                MoneyDropScreen.return_rect.collidepoint(event.pos) and MoneyDropScreen.game_over):
                            # Annuler
                            current_game_mode = 0

                    elif current_game_mode == WordleScreen.game_mode_id:
                        # WORDLE *******************************************
                        if WordleScreen.cancel_rect.collidepoint(event.pos):
                            # Annuler
                            current_game_mode = 0
                            WordleScreen.is_game_over = False
                            WordleScreen.defeat = False
                            WordleScreen.point_earned = 0
                        WordleScreen.input_box.handle_event(event)

                    elif current_game_mode == TimerScreen.game_mode_id:
                        if TimerScreen.cancel_rect.collidepoint(event.pos):
                            # Annuler
                            current_game_mode = 0
                        if TimerScreen.stop_button_rect.collidepoint(event.pos):
                            TimerScreen.stop_timer = True
                    elif current_game_mode == ProjectG.game_mode_id:
                        if ProjectG.cancel_rect.collidepoint(event.pos):
                            current_game_mode = 0
                            running = False
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
                                screen_round.is_round7_active = (button.round_id == "password")
                                screen_round.is_round_drop_active = (button.round_id == "drop")
                                screen_round.is_round_wordle_active = (button.round_id == "wordle")
                                screen_round.is_round_timer_active = (button.round_id == "timer")
                                screen_round.is_round_projectG_active = (button.round_id == "projectG")

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
                                    selection_player_screen.save_points()

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
                        # Round Mot de Passe
                        if screen_round.is_round7_active:
                            if not selection_player_screen.is_selecting_player and not selection_round.is_selecting_round:
                                for button in screen_round.group_buttons_round7:
                                    if button.rect.collidepoint(event.pos):
                                        PasswordScreen.set_max_attempt(convert_difficulty_to_number_password(button.name))
                                        PasswordScreen.password_pins.answered_password.clear()
                                        PasswordScreen.password_pins.set_pins()
                                        PasswordScreen.set_password()
                                        current_game_mode = PasswordScreen.game_mode_ID
                        # Round Money Drop
                        if screen_round.is_round_drop_active:
                            if not selection_player_screen.is_selecting_player and not selection_round.is_selecting_round:
                                for button in screen_round.group_buttons_round_drop:
                                    if button.rect.collidepoint(event.pos):
                                        MoneyDropScreen.reset_game()
                                        current_game_mode = MoneyDropScreen.game_mode_id
                        # Round Wordle
                        if screen_round.is_round_wordle_active:
                            if not selection_player_screen.is_selecting_player and not selection_round.is_selecting_round:
                                for button in screen_round.group_buttons_round_wordle:
                                    if button.rect.collidepoint(event.pos):
                                        WordleScreen.set_max_attempt(convert_difficulty_to_number_wordle(button.name))
                                        WordleScreen.answered.clear()
                                        WordleScreen.input_box.text = ""
                                        WordleScreen.set_answer()
                                        current_game_mode = WordleScreen.game_mode_id

                        # Round Timer
                        if screen_round.is_round_timer_active:
                            if not selection_player_screen.is_selecting_player and not selection_round.is_selecting_round:
                                for button in screen_round.group_buttons_round_timer:
                                    if button.rect.collidepoint(event.pos):
                                        game.is_playing = False
                                        current_game_mode = TimerScreen.game_mode_id
                                        TimerScreen.stop_timer = False
                                        timer_for_round = 0
                                        TimerScreen.game_over = False
                        # Project G
                        if screen_round.is_round_projectG_active:
                            if not selection_player_screen.is_selecting_player and not selection_round.is_selecting_round:
                                for button in screen_round.group_buttons_round_projectg:
                                    if button.rect.collidepoint(event.pos):
                                        current_game_mode = ProjectG.game_mode_id

                elif event.type == pygame.KEYDOWN:
                    if current_game_mode == MoneyDropScreen.game_mode_id and not MoneyDropScreen.wait_for_next_step:
                        MoneyDropScreen.input_box_a.handle_event(event)
                        MoneyDropScreen.input_box_b.handle_event(event)
                        MoneyDropScreen.input_box_c.handle_event(event)
                        MoneyDropScreen.input_box_d.handle_event(event)
                    if current_game_mode == WordleScreen.game_mode_id and not WordleScreen.is_game_over:
                        if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                            WordleScreen.add_answer()
                        WordleScreen.input_box.handle_event(event)
                        WordleScreen.limit_text()

pygame.quit()
