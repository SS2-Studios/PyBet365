import pygame
import random
import sys
from config import *
from utils import *
from assets import *
from game import race_animation

def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PyBet365")

    font = pygame.font.SysFont("Verdana", 36)
    small_font = pygame.font.SysFont("Verdana", 28)

    horse_image, track_background = load_images()
    horse_running_sound, lose_sound, win_sound, start_race_sound = load_sounds()

    balance = 1000
    selected_team = None
    bet_amount = 0
    stage = "team_selection"
    user_input = ""
    team_odds = {team: round(random.uniform(2, 5), 2) for team in teams}
    last_update = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    # Multiplayer variables
    client = None  # Placeholder for socket connection

    while True:
        screen.fill(DARK_BG)
        mouse_pos = pygame.mouse.get_pos()

        if stage == "team_selection":
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= 500:
                team_odds = {team: round(random.uniform(2, 5), 2) for team in teams}
                last_update = current_time

            draw_text("Dobrodošli u Trku konja", font, ACCENT, screen, SCREEN_WIDTH // 2, 50, center=True)
            draw_text(f"Vaš balans: {balance} €", small_font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 100, center=True)
            draw_text("Odaberite konja:", font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 180, center=True)

            y_offset = 240
            buttons = []
            for i, team in enumerate(teams):
                text = f"{team} - Kvote: {team_odds[team]}"
                button = draw_button_with_text(text, SCREEN_WIDTH // 2, y_offset + i * 80, font, LIGHT_TEXT, GRAY, screen)
                buttons.append((button, team))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button, team in buttons:
                        if button.collidepoint(mouse_pos):
                            selected_team = team
                            stage = "bet_input"

        elif stage == "bet_input":
            draw_text(f"Vaš balans: {balance} €", small_font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 100, center=True)
            draw_text("Unesite iznos uloga ili odaberite opciju:", font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 150, center=True)

            button_25 = draw_button_with_text(f"25% Balansa", SCREEN_WIDTH // 2, 230, small_font, LIGHT_TEXT, ACCENT, screen)
            button_50 = draw_button_with_text(f"50% Balansa", SCREEN_WIDTH // 2, 310, small_font, LIGHT_TEXT, ACCENT, screen)
            button_75 = draw_button_with_text(f"75% Balansa", SCREEN_WIDTH // 2, 390, small_font, LIGHT_TEXT, ACCENT, screen)
            button_100 = draw_button_with_text(f"100% Balansa", SCREEN_WIDTH // 2, 470, small_font, LIGHT_TEXT, ACCENT, screen)

            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 100, 550, 200, 50), border_radius=10)
            draw_text(user_input, font, DARK_BG, screen, SCREEN_WIDTH // 2, 575, center=True)

            if user_input == "0":
                draw_text("Molimo unesite ulog veći od 0!", small_font, RED, screen, SCREEN_WIDTH // 2, 625, center=True)
            elif user_input.isdigit() and int(user_input) > balance:
                draw_text("Nemate dovoljno novca!", small_font, RED, screen, SCREEN_WIDTH // 2, 625, center=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_25.collidepoint(mouse_pos):
                        bet_amount = balance * 0.25
                        user_input = str(int(bet_amount))
                    elif button_50.collidepoint(mouse_pos):
                        bet_amount = balance * 0.50
                        user_input = str(int(bet_amount))
                    elif button_75.collidepoint(mouse_pos):
                        bet_amount = balance * 0.75
                        user_input = str(int(bet_amount))
                    elif button_100.collidepoint(mouse_pos):
                        bet_amount = balance
                        user_input = str(int(bet_amount))

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit():
                        user_input += event.unicode
                    elif event.key == pygame.K_RETURN:
                        if user_input and int(user_input) <= balance:
                            bet_amount = int(user_input)
                            balance -= bet_amount
                            # Multiplayer stage
                            try:
                                client.send(f"BET|{selected_team}|{bet_amount}".encode())
                                stage = "waiting_for_results"
                            except Exception as e:
                                print(f"Greška u komunikaciji sa serverom: {e}")
                                pygame.quit()
                                sys.exit()

        elif stage == "waiting_for_results":
            # Animacija trke
            speeds = {team: random.randint(3, 5) for team in teams}
            distances = {team: 50 for team in teams}
            race_ongoing = True

            while race_ongoing:
                screen.fill(DARK_BG)
                draw_text("Trka je u toku!", font, ACCENT, screen, SCREEN_WIDTH // 2, 50, center=True)
                draw_track(screen, teams)

                for team in teams:
                    distances[team] += speeds[team]
                    if distances[team] >= SCREEN_WIDTH - 150:  # Ciljna linija
                        race_ongoing = False
                        result = team
                        break

                draw_horses(screen, distances, horse_image, teams)

                pygame.display.flip()
                clock.tick(30)

            # Nakon završetka animacije primamo rezultat od servera
            try:
                data = client.recv(1024).decode()  # Čekanje odgovora sa servera
                if "|" in data:
                    parts = data.split('|')
                    if len(parts) == 3:
                        command, winner, updated_balance = parts
                        if command == "RESULT":
                            if winner == selected_team:
                                balance = int(updated_balance)
                                win_sound.play()
                                stage = "result"
                            else:
                                lose_sound.play()
                                stage = "result"
            except Exception as e:
                print(f"Greška u komunikaciji sa serverom: {e}")
                pygame.quit()
                sys.exit()

        elif stage == "result":
            draw_text(f"Vaš balans: {balance} €", small_font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 100, center=True)
            draw_text("Pritisnite R za povratak na klađenje ili ESC za izlazak.", small_font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 400, center=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        stage = "team_selection"
                        user_input = ""
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
