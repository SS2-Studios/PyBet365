
import pygame, sys, time, random
from constants import *
from utils import draw_text, draw_button
from graphics import draw_track
from race import race_animation

# Inicijalizacija pygame-a
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Trka konja")

# Učitavanje slike konja
horse_image = pygame.image.load("horse.png")
horse_image = pygame.transform.scale(horse_image, (40, 40))

# Glavne promenljive
teams = ["Tim A", "Tim B", "Tim C", "Tim D"]
kotes = {team: round(random.uniform(1.5, 3.5), 2) for team in teams}
balance = 1000
selected_team = None
bet_amount = 0

def main():
    global selected_team, bet_amount, balance, kotes
    clock = pygame.time.Clock()
    user_input = ""
    stage = "team_selection"
    result = ""
    kotes_timer = time.time()

    while True:
        screen.fill(DARK_BG)
        mouse_pos = pygame.mouse.get_pos()

        # Promena kvota na svakih pola sekunde
        if time.time() - kotes_timer >= 0.5:
            kotes = {team: round(random.uniform(1.5, 3.5), 2) for team in teams}
            kotes_timer = time.time()

        # Ekrani igre
        if stage == "team_selection":
            draw_text("Dobrodošli u Trku konja", FONT_LARGE, ACCENT, screen, SCREEN_WIDTH // 2, 50)
            draw_text(f"Balans: {balance} €", FONT_MEDIUM, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 100)

            # Dugmići za selekciju tima
            y_offset = 200
            buttons = []
            for i, team in enumerate(teams):
                active = selected_team == team
                button = draw_button(f"{team} - {kotes[team]}x", SCREEN_WIDTH // 2 - 100, y_offset + i * 60, 200, 40, GRAY, ACCENT, mouse_pos, screen, active)
                buttons.append((button, team))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button, team in buttons:
                        if button.collidepoint(mouse_pos):
                            selected_team = team
                            stage = "bet_input"

        elif stage == "bet_input":
            draw_text("Unesite ulog:", FONT_MEDIUM, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 200)
            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 75, 250, 150, 40))
            draw_text(user_input, FONT_MEDIUM, DARK_BG, screen, SCREEN_WIDTH // 2, 270)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and user_input.isdigit():
                        bet_amount = int(user_input)
                        winner = race_animation(screen, teams, horse_image)
                        if winner == selected_team:
                            winnings = int(bet_amount * kotes[selected_team])
                            balance += winnings
                            result = f"Pobeda! Dobitak: {winnings}€"
                        else:
                            balance -= bet_amount
                            result = f"Izgubili ste {bet_amount}€. Pobednik: {winner}"
                        stage = "result"
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit():
                        user_input += event.unicode

        elif stage == "result":
            draw_text(result, FONT_MEDIUM, GREEN if "Pobeda" in result else RED, screen, SCREEN_WIDTH // 2, 300)
            draw_text("Pritisnite bilo koji taster za povratak", FONT_SMALL, WHITE, screen, SCREEN_WIDTH // 2, 400)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    stage = "team_selection"

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
