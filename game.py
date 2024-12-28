import random
import pygame
from config import *
from utils import *
from assets import *

def race_animation(horse_image, track_background, team_odds, screen, font, small_font, team_positions, speeds, selected_team):
    track_length = SCREEN_WIDTH - 150
    winner = None
    horse_running_sound, lose_sound, win_sound, start_race_sound = load_sounds()

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
