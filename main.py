import pygame
import sys
import time
import random
from constants import *
from ui import draw_text, draw_button, draw_input_field, fade_in
from race import race_animation

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyBet365 Trka Konja")

horse_image = pygame.image.load("horse.png")
horse_image = pygame.transform.scale(horse_image, (80, 80))

teams = ["Tim A", "Tim B", "Tim C", "Tim D"]
kotes = {team: round(random.uniform(1.5, 3.5), 2) for team in teams}
balance = 1000

def main():
    global balance
    stage = "team_selection"
    selected_team = None
    user_input = ""
    bet_amount = 0
    clock = pygame.time.Clock()

    while True:
        screen.fill(DARK_BG)
        mouse_pos = pygame.mouse.get_pos()
        draw_text("PyBet365 Trka Konja", FONT_TITLE, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 100)

        if stage == "team_selection":
            draw_text(f"Balans: {balance} €", FONT_MEDIUM, WHITE, screen, SCREEN_WIDTH // 2, 200)
            buttons = []
            for i, team in enumerate(teams):
                rect = draw_button(screen, f"{team} - {kotes[team]}x", SCREEN_WIDTH // 2 - 150, 300 + i * 100, 300, 60, mouse_pos)
                buttons.append((rect, team))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, team in buttons:
                        if rect.collidepoint(mouse_pos):
                            selected_team = team
                            stage = "bet_input"

        elif stage == "bet_input":
            draw_text("Unesite iznos uloga:", FONT_MEDIUM, WHITE, screen, SCREEN_WIDTH // 2, 400)
            draw_input_field(screen, SCREEN_WIDTH // 2 - 150, 500, 300, 60, user_input, True)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and user_input.isdigit():
                        bet_amount = int(user_input)
                        stage = "race"
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit():
                        user_input += event.unicode

        elif stage == "race":
            fade_in(screen, DARK_BG)
            winner = race_animation(screen, teams, horse_image)
            stage = "result"
            race_winner = winner

        elif stage == "result":
            draw_text(f"Pobednik: {race_winner}", FONT_LARGE, ACCENT, screen, SCREEN_WIDTH // 2, 400)
            draw_text("ESC - izlaz | SPACE - nova igra", FONT_SMALL, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 500)
            for event in pygame.event.get():
                if event.key == pygame.K_SPACE:
                    stage = "team_selection"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
