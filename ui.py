import pygame
from constants import *

def fade_in(surface, color, duration=1000):
    """Efekat fade-in tranzicije na ekranu."""
    fade_surface = pygame.Surface(surface.get_size())
    fade_surface.fill(color)
    for alpha in range(0, 255, 5):  # Povećava transparentnost
        fade_surface.set_alpha(alpha)
        surface.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(duration // 50)  # Kontroliše brzinu fade-in efekta

def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def draw_button(surface, text, x, y, w, h, mouse_pos):
    color = ACCENT if pygame.Rect(x, y, w, h).collidepoint(mouse_pos) else GRAY
    pygame.draw.rect(surface, color, (x, y, w, h), border_radius=10)
    draw_text(text, FONT_MEDIUM, WHITE, surface, x + w // 2, y + h // 2)
    return pygame.Rect(x, y, w, h)

def draw_input_field(surface, x, y, w, h, text, active):
    border_color = ACCENT if active else WHITE
    pygame.draw.rect(surface, border_color, (x, y, w, h), 3, border_radius=5)
    draw_text(text, FONT_SMALL, WHITE, surface, x + w // 2, y + h // 2)

def draw_finish_line(surface):
    block_size = 20
    for y in range(TRACK_Y_START, TRACK_Y_START + TRACK_Y_GAP * 4, block_size):
        for x in range(FINISH_LINE_X, FINISH_LINE_X + 20, block_size):
            color = WHITE if (x // block_size + y // block_size) % 2 == 0 else BLACK
            pygame.draw.rect(surface, color, (x, y, block_size, block_size))
