import pygame
from constants import LIGHT_TEXT, WHITE, BLACK, SCREEN_WIDTH

def draw_track(surface, teams):
    """Funkcija za crtanje trkalista."""
    for i in range(len(teams)):
        y = 150 + i * 100
        pygame.draw.line(surface, LIGHT_TEXT, (100, y), (SCREEN_WIDTH - 100, y), 3)
    pygame.draw.line(surface, BLACK, (SCREEN_WIDTH - 100, 150), (SCREEN_WIDTH - 100, 550), 5)
    pygame.draw.rect(surface, WHITE, (SCREEN_WIDTH - 105, 150, 5, 400))
