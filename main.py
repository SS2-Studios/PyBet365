import pygame
import random
import sys

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyBet365")

DARK_BG = (24, 26, 27)
ACCENT = (30, 144, 255)
LIGHT_TEXT = (200, 200, 200)
GREEN = (50, 205, 50)
RED = (255, 69, 58)
FINISH_COLOR = (255, 255, 255)
GRAY = (75, 75, 75)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("Verdana", 36)
small_font = pygame.font.SysFont("Verdana", 28)

teams = ["Konj Rale", "Konj Makedonac", "Konj Vrhovni", "Konj Ivica", "Konj Boja"]
selected_team = None
bet_amount = 0
balance = 1000

horse_image = pygame.image.load("horse.png")
horse_image = pygame.transform.scale(horse_image, (60, 60))
track_background = pygame.image.load("track_background.jpg")
track_background = pygame.transform.scale(track_background, (SCREEN_WIDTH, SCREEN_HEIGHT))

horse_running_sound = pygame.mixer.Sound("horse_running.wav")
lose_sound = pygame.mixer.Sound("lose_sound.wav")
win_sound = pygame.mixer.Sound("win_sound.wav")
start_race_sound = pygame.mixer.Sound("start_race.wav")

def draw_text(text, font, color, surface, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def draw_button_with_text(text, x, y, font, text_color, bg_color, surface):
    text_surface = font.render(text, True, text_color)
    text_width = text_surface.get_width()
    text_height = text_surface.get_height()
    button_width = text_width + 20
    button_height = text_height + 10
    pygame.draw.rect(surface, bg_color, (x - button_width // 2, y - button_height // 2, button_width, button_height), border_radius=10)
    surface.blit(text_surface, (x - text_width // 2, y - text_height // 2))
    return pygame.Rect(x - button_width // 2, y - button_height // 2, button_width, button_height)

def race_animation():
    track_length = SCREEN_WIDTH - 150
    team_positions = {team: 50 for team in teams}
    speeds = {team: random.randint(3, 5) for team in teams}
    winner = None

    running = True
    start_race_sound.play()
    start_time = pygame.mixer.Sound.get_length(start_race_sound)
    time_started = pygame.time.get_ticks()

    while pygame.time.get_ticks() - time_started < start_time * 1000:
        screen.fill(DARK_BG)
        screen.blit(track_background, (0, 0))
        draw_text("Trka konja!", font, ACCENT, screen, SCREEN_WIDTH // 2, 50, center=True)
        pygame.draw.rect(screen, FINISH_COLOR, (track_length, 0, 10, SCREEN_HEIGHT), 0)
        for y in range(100, SCREEN_HEIGHT, 150):
            pygame.draw.line(screen, LIGHT_TEXT, (0, y), (SCREEN_WIDTH, y), 2)
        for team in teams:
            horse_rect = horse_image.get_rect(center=(team_positions[team], 100 + teams.index(team) * 150 + 50))
            screen.blit(horse_image, horse_rect.topleft)
            draw_text(team, small_font, LIGHT_TEXT, screen, team_positions[team] + 30, 100 + teams.index(team) * 150 + 70, center=True)
        pygame.display.flip()
        pygame.time.delay(100)

    horse_running_sound.play(loops=-1, maxtime=0)

    while running:
        screen.fill(DARK_BG)
        screen.blit(track_background, (0, 0))
        draw_text("Trka konja!", font, ACCENT, screen, SCREEN_WIDTH // 2, 50, center=True)
        pygame.draw.rect(screen, FINISH_COLOR, (track_length, 0, 10, SCREEN_HEIGHT), 0)
        for y in range(100, SCREEN_HEIGHT, 150):
            pygame.draw.line(screen, LIGHT_TEXT, (0, y), (SCREEN_WIDTH, y), 2)
        for team in teams:
            horse_rect = horse_image.get_rect(center=(team_positions[team], 100 + teams.index(team) * 150 + 50))
            screen.blit(horse_image, horse_rect.topleft)
            draw_text(team, small_font, LIGHT_TEXT, screen, team_positions[team] + 30, 100 + teams.index(team) * 150 + 70, center=True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for team in teams:
            speeds[team] += random.choice([-1, 0, 1])
            speeds[team] = max(2, speeds[team])
            team_positions[team] += speeds[team]
            if team_positions[team] >= track_length and winner is None:
                winner = team
                running = False
                break
        pygame.display.flip()
        pygame.time.delay(100)

    horse_running_sound.stop()
    return winner

def main():
    global selected_team, bet_amount, balance

    clock = pygame.time.Clock()
    user_input = ""
    result = ""
    stage = "team_selection"
    last_update = pygame.time.get_ticks()
    team_odds = {team: round(random.uniform(2, 5), 2) for team in teams}

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
                if user_input and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if bet_amount <= balance:
                        balance -= bet_amount
                        result = race_animation()
                        if result == selected_team:
                            winnings = bet_amount * team_odds[selected_team]
                            balance += winnings
                            win_sound.play()
                            stage = "result"
                            draw_text(f"Čestitamo! Pobedili ste i osvojili {winnings:.2f} €!", font, GREEN, screen, SCREEN_WIDTH // 2, 300, center=True)
                        else:
                            lose_sound.play()
                            stage = "result"
                            draw_text(f"Nažalost, izgubili ste {bet_amount:.2f} €.", font, RED, screen, SCREEN_WIDTH // 2, 300, center=True)
        elif stage == "result":
            if result == selected_team:
                winnings = bet_amount * team_odds[selected_team]
                balance += winnings
                win_message = f"Čestitamo! Pobedili ste sa konjem {selected_team} i osvojili {winnings:.2f} €!"
                draw_text(win_message, font, GREEN, screen, SCREEN_WIDTH // 2, 300, center=True)
                win_sound.play()
            else:
                lose_message = f"Nažalost, vaš konj {selected_team} je izgubio. Pobednik je {result}."
                draw_text(lose_message, font, RED, screen, SCREEN_WIDTH // 2, 300, center=True)
                lose_sound.play()
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
