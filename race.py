
import pygame, random, sys
from constants import DARK_BG, ACCENT, SCREEN_WIDTH, GREEN
from graphics import draw_track
from utils import draw_text

def race_animation(surface, teams, horse_image):
    """Funkcija za animaciju trke."""
    track_length = SCREEN_WIDTH - 200
    horse_positions = {team: 100 for team in teams}
    speeds = {team: random.randint(1, 5) for team in teams}

    running = True
    winner_found = None

    while running:
        surface.fill(DARK_BG)
        draw_text("Trka konja", FONT_LARGE, ACCENT, surface, SCREEN_WIDTH // 2, 50)
        draw_track(surface, teams)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for i, team in enumerate(teams):
            y_position = 170 + i * 100
            x_position = horse_positions[team]
            surface.blit(horse_image, (x_position, y_position))

            if not winner_found:
                horse_positions[team] += speeds[team]
                if horse_positions[team] >= track_length:
                    winner_found = team
                    running = False
                    break

        pygame.display.flip()
        pygame.time.delay(50)

    return winner_found
