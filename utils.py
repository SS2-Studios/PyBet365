import pygame
from constants import WHITE, FONT_SMALL

def draw_text(text, font, color, surface, x, y):
    """Funkcija za crtanje centriranog teksta."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(text, x, y, w, h, color, hover_color, mouse_pos, surface, active):
    """Funkcija za crtanje dugmeta."""
    rect_color = hover_color if active else color
    pygame.draw.rect(surface, rect_color, (x, y, w, h), border_radius=8)
    draw_text(text, FONT_SMALL, WHITE, surface, x + w // 2, y + h // 2)
    return pygame.Rect(x, y, w, h)
