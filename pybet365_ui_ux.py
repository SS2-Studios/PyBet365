# Enhancing UI/UX for PyBet365 within existing structure

import pygame
import os
from game import Game

# Initialize pygame
pygame.init()

# Constants for UI design
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (30, 30, 30)
BUTTON_COLOR = (50, 150, 250)
HOVER_COLOR = (70, 180, 255)
TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.Font(None, 36)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyBet365")

# Load assets
def load_asset(filename):
    return pygame.image.load(os.path.join("assets", filename))

track_background = load_asset("track_background.jpg")
horse_image = load_asset("horse.png")

# Create buttons with hover effect
def draw_button(screen, text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    color = BUTTON_COLOR if not (x < mouse[0] < x + width and y < mouse[1] < y + height) else HOVER_COLOR
    pygame.draw.rect(screen, color, (x, y, width, height))

    label = FONT.render(text, True, TEXT_COLOR)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

    if x < mouse[0] < x + width and y < mouse[1] < y + height and click[0] == 1 and action:
        action()

# Main menu loop
def main_menu():
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        label = FONT.render("Welcome to PyBet365", True, TEXT_COLOR)
        screen.blit(label, ((SCREEN_WIDTH - label.get_width()) // 2, 50))

        draw_button(screen, "Start Game", 300, 200, 200, 50, start_game)
        draw_button(screen, "Tutorial", 300, 300, 200, 50, show_tutorial)
        draw_button(screen, "Quit", 300, 400, 200, 50, quit_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

# Game start functionality
def start_game():
    game = EnhancedGame(screen, track_background, horse_image, FONT)
    game.run()  # Assuming the Game class has a run method for managing game flow
    main_menu()

# Quit functionality
def quit_game():
    pygame.quit()
    quit()

# Add better tutorial flow
def show_tutorial():
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        label = FONT.render("Tutorial: Place your bets and watch the race!", True, TEXT_COLOR)
        screen.blit(label, ((SCREEN_WIDTH - label.get_width()) // 2, SCREEN_HEIGHT // 2))

        draw_button(screen, "Back", 300, 400, 200, 50, main_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

# Enhance race visualization in Game class
class EnhancedGame(Game):
    def draw_horse(self, horse, x, y):
        screen.blit(horse_image, (x, y))
        # Add a progress bar under each horse
        pygame.draw.rect(screen, (255, 255, 255), (x, y + horse_image.get_height() + 5, 200, 10))
        pygame.draw.rect(screen, (50, 200, 50), (x, y + horse_image.get_height() + 5, horse.progress * 200, 10))

# Launch the main menu
if __name__ == "__main__":
    main_menu()
