import pygame

# Boje
DARK_BG = (15, 20, 45)  # Lepša tamno plava pozadina
ACCENT = (255, 140, 0)  # Narančasta za hover i naglaske
LIGHT_TEXT = (240, 240, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
FINISH_LINE = (255, 255, 255)

# Rezolucija
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

# Fontovi
pygame.font.init()
FONT_TITLE = pygame.font.SysFont("Arial", 72, bold=True)
FONT_LARGE = pygame.font.SysFont("Arial", 48, bold=True)
FONT_MEDIUM = pygame.font.SysFont("Arial", 36)
FONT_SMALL = pygame.font.SysFont("Arial", 28)

# Trkalište
TRACK_Y_START = 300
TRACK_Y_GAP = 150
FINISH_LINE_X = SCREEN_WIDTH - 200

# Brzina i FPS
FPS = 60
RACE_SPEED = 6
