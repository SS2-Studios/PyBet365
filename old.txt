import pygame
import random
import sys
import time

# Inicijalizacija pygame-a
pygame.init()

# Postavljanje ekrana i boja
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trka konja")

# Boje za dark mode
DARK_BG = (24, 26, 27)  # Tamno siva
ACCENT = (30, 144, 255)  # Plavi naglasak
LIGHT_TEXT = (200, 200, 200)
GREEN = (50, 205, 50)
RED = (255, 69, 58)
FINISH_COLOR = (255, 255, 255)
GRAY = (75, 75, 75)
WHITE = (255, 255, 255)

# Fontovi
font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)

# Timovi za klađenje
teams = ["Konj Rale", "Konj Makedonac", "Konj Vrhovni", "Konj Ivica"]
selected_team = None
bet_amount = 0
balance = 1000  # Početni novac korisnika

# Učitavanje slike konja
horse_image = pygame.image.load("horse.png")  # Postavi sliku u isti folder
horse_image = pygame.transform.scale(horse_image, (80, 80))  # Smanji sliku konja

# Funkcija za crtanje teksta
def draw_text(text, font, color, surface, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Funkcija za crtanje dugmeta
def draw_button(text, x, y, w, h, color, hover_color, mouse_pos, surface, active):
    rect_color = hover_color if active else color
    pygame.draw.rect(surface, rect_color, (x, y, w, h), border_radius=8)
    draw_text(text, small_font, WHITE, surface, x + 10, y + 10)
    return pygame.Rect(x, y, w, h)

# Funkcija za trku konja
def race_animation():
    track_length = SCREEN_WIDTH - 150
    team_positions = {team: 100 for team in teams}
    speeds = {team: random.randint(3, 6) for team in teams}
    winner = None

    running = True
    while running:
        screen.fill(DARK_BG)
        draw_text("Trka konja!", font, ACCENT, screen, SCREEN_WIDTH // 2, 50, center=True)

        # Crtanje finish linije
        pygame.draw.rect(screen, FINISH_COLOR, (track_length, 0, 10, SCREEN_HEIGHT), 0)

        # Crtanje trkalista
        for y in range(100, SCREEN_HEIGHT, 150):
            pygame.draw.line(screen, LIGHT_TEXT, (0, y), (SCREEN_WIDTH, y), 2)

        # Crtanje konja
        for team in teams:
            screen.blit(horse_image, (team_positions[team], 100 + teams.index(team) * 150))
            draw_text(team, small_font, LIGHT_TEXT, screen, team_positions[team] + 25, 100 + teams.index(team) * 150 + 90)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Ažuriranje pozicija
        for team in teams:
            team_positions[team] += speeds[team]
            if team_positions[team] >= track_length and winner is None:
                winner = team
                running = False
                break

        pygame.display.flip()
        pygame.time.delay(50)

    return winner

# Glavna petlja igre
def main():
    global selected_team, bet_amount, balance

    clock = pygame.time.Clock()
    user_input = ""
    result = ""
    stage = "team_selection"

    while True:
        screen.fill(DARK_BG)
        mouse_pos = pygame.mouse.get_pos()

        # Faza 1: Odabir tima
        if stage == "team_selection":
            draw_text("Dobrodošli u Trku konja", font, ACCENT, screen, SCREEN_WIDTH // 2, 50, center=True)
            draw_text(f"Vaš balans: {balance} €", small_font, LIGHT_TEXT, screen, 20, 100)
            draw_text("Odaberite konja:", font, LIGHT_TEXT, screen, 20, 180)
            y_offset = 240
            buttons = []
            for i, team in enumerate(teams):
                button = draw_button(f"{team} - Kvote: {round(random.uniform(2, 5), 2)}", 300, y_offset + i * 60, 400, 40, GRAY, ACCENT, mouse_pos, screen, selected_team == team)
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

        # Faza 2: Unos uloga
        elif stage == "bet_input":
            draw_text("Unesite iznos uloga:", font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 150, center=True)
            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 100, 200, 200, 40), border_radius=5)
            draw_text(user_input, font, DARK_BG, screen, SCREEN_WIDTH // 2, 210, center=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and user_input.isdigit():
                        bet_amount = int(user_input)
                        if bet_amount <= balance:
                            winner = race_animation()
                            if winner == selected_team:
                                balance += bet_amount * 2
                                result = f"Čestitamo! {winner} je pobijedio. Dobitak: {bet_amount * 2} €."
                            else:
                                balance -= bet_amount
                                result = f"Žao nam je, {winner} je pobijedio. Izgubili ste {bet_amount} €."
                            stage = "result"
                        else:
                            result = "Nemate dovoljno novca!"
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit():
                        user_input += event.unicode

        # Faza 3: Rezultat trke
        elif stage == "result":
            draw_text(result, font, GREEN if "Čestitamo" in result else RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
            draw_text("Pritisnite R za novu igru ili ESC za izlaz.", small_font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        stage = "team_selection"
                        selected_team = None
                        user_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
