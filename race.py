import pygame
import random
from constants import *
from ui import draw_text, draw_finish_line

def race_animation(surface, teams, horse_image):
    positions = {team: 150 for team in teams}
    speeds = {team: random.randint(2, RACE_SPEED) for team in teams}
    running = True
    winners = []

    while running:
        surface.fill(DARK_BG)
        draw_finish_line(surface)

        for i, team in enumerate(teams):
            y = TRACK_Y_START + i * TRACK_Y_GAP
            pygame.draw.line(surface, LIGHT_TEXT, (150, y + 40), (SCREEN_WIDTH - 100, y + 40), 3)
            surface.blit(horse_image, (positions[team], y))
            positions[team] += speeds[team]

            if positions[team] >= FINISH_LINE_X and team not in winners:
                winners.append(team)

        draw_text("Trka je u toku...", FONT_LARGE, ACCENT, surface, SCREEN_WIDTH // 2, 50)
        pygame.display.update()

        if len(winners) == len(teams):
            running = False

        pygame.time.delay(40)

    return winners[0]  # Prvi konj koji je stigao
