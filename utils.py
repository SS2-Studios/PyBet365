import pygame

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
