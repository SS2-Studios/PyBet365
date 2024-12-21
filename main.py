import pygame
import random
import sys

# Inicijalizacija pygame-a
pygame.init()
pygame.mixer.init()  # Inicijalizacija zvučnog sistema

# Postavljanje ekrana i boja
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PyBet365")

# Boje za dark mode
DARK_BG = (24, 26, 27)
ACCENT = (30, 144, 255)
LIGHT_TEXT = (200, 200, 200)
GREEN = (50, 205, 50)
RED = (255, 69, 58)
FINISH_COLOR = (255, 255, 255)
GRAY = (75, 75, 75)
WHITE = (255, 255, 255)

# Fontovi
font = pygame.font.SysFont("Verdana", 36)
small_font = pygame.font.SysFont("Verdana", 28)

# Timovi za klađenje
teams = ["Konj Rale", "Konj Makedonac", "Konj Vrhovni", "Konj Ivica", "Konj Boja"]
selected_team = None
bet_amount = 0
balance = 1000

# Učitavanje slika konja i pozadine trkališta
horse_image = pygame.image.load("horse.png")
horse_image = pygame.transform.scale(horse_image, (60, 60))
track_background = pygame.image.load("track_background.jpg")  # Slika trkališta, zemlja/pesak
track_background = pygame.transform.scale(track_background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Prilagodimo pozadinu

# Učitajte zvukove
horse_running_sound = pygame.mixer.Sound("horse_running.wav")  # Zvuk trčanja konja
lose_sound = pygame.mixer.Sound("lose_sound.wav")  # Zvuk kada izgubite
win_sound = pygame.mixer.Sound("win_sound.wav")  # Zvuk kada pobedite
start_race_sound = pygame.mixer.Sound("start_race.wav")  # Zvuk kada trka počne

# Funkcija za crtanje teksta
def draw_text(text, font, color, surface, x, y, center=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Funkcija za crtanje dugmeta
def draw_button(text, x, y, min_width, height, color, hover_color, mouse_pos, surface, active):
    # Računanje dužine teksta i širine dugmadi
    text_width = font.size(text)[0] + 40  # Dodajemo 40 piksela za padding
    button_width = max(min_width, text_width)  # Širina dugmeta zavisi od dužine teksta
    
    rect_color = hover_color if active else color
    pygame.draw.rect(surface, rect_color, (x, y, button_width, height), border_radius=8)
    
    draw_text(text, small_font, WHITE, surface, x + button_width // 2, y + height // 2, center=True)
    
    return pygame.Rect(x, y, button_width, height)

# Funkcija za trku konja
def race_animation():
    track_length = SCREEN_WIDTH - 150
    team_positions = {team: 50 for team in teams}
    speeds = {team: random.randint(3, 5) for team in teams}
    winner = None

    running = True
    start_race_sound.play()  # Zvuk trke počinje
    start_time = pygame.mixer.Sound.get_length(start_race_sound)  # Trajanje start_race zvuka
    time_started = pygame.time.get_ticks()

    # Dok traje start_race zvuk, konji ne pomeraju
    while pygame.time.get_ticks() - time_started < start_time * 1000:
        screen.fill(DARK_BG)
        screen.blit(track_background, (0, 0))  # Postavljanje pozadine trkališta
        draw_text("Trka konja!", font, ACCENT, screen, SCREEN_WIDTH // 2, 50, center=True)

        # Crtanje finish linije
        pygame.draw.rect(screen, FINISH_COLOR, (track_length, 0, 10, SCREEN_HEIGHT), 0)

        # Crtanje trkalista
        for y in range(100, SCREEN_HEIGHT, 150):
            pygame.draw.line(screen, LIGHT_TEXT, (0, y), (SCREEN_WIDTH, y), 2)

        # Crtanje konja (na početnoj poziciji dok zvuk traje)
        for team in teams:
            horse_rect = horse_image.get_rect(center=(team_positions[team], 100 + teams.index(team) * 150 + 50))
            screen.blit(horse_image, horse_rect.topleft)
            draw_text(team, small_font, LIGHT_TEXT, screen, team_positions[team] + 30, 100 + teams.index(team) * 150 + 70, center=True)

        pygame.display.flip()
        pygame.time.delay(100)

    # Kada zvuk završi, počinju da trče konji
    horse_running_sound.play(loops=-1, maxtime=0)  # Zvuk trčanja konja se reprodukuje tokom trke

    while running:
        screen.fill(DARK_BG)
        screen.blit(track_background, (0, 0))  # Postavljanje pozadine trkališta
        draw_text("Trka konja!", font, ACCENT, screen, SCREEN_WIDTH // 2, 50, center=True)

        # Crtanje finish linije
        pygame.draw.rect(screen, FINISH_COLOR, (track_length, 0, 10, SCREEN_HEIGHT), 0)

        # Crtanje trkalista
        for y in range(100, SCREEN_HEIGHT, 150):
            pygame.draw.line(screen, LIGHT_TEXT, (0, y), (SCREEN_WIDTH, y), 2)

        # Crtanje konja
        for team in teams:
            horse_rect = horse_image.get_rect(center=(team_positions[team], 100 + teams.index(team) * 150 + 50))
            screen.blit(horse_image, horse_rect.topleft)
            draw_text(team, small_font, LIGHT_TEXT, screen, team_positions[team] + 30, 100 + teams.index(team) * 150 + 70, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Ažuriranje pozicija i brzina
        for team in teams:
            speeds[team] += random.choice([-1, 0, 1])
            speeds[team] = max(2, speeds[team])  # Minimalna brzina
            team_positions[team] += speeds[team]
            if team_positions[team] >= track_length and winner is None:
                winner = team
                running = False
                break

        pygame.display.flip()
        pygame.time.delay(100)

    horse_running_sound.stop()  # Zaustavite zvuk trčanja konja
    return winner

# Glavna petlja igre
def main():
    global selected_team, bet_amount, balance

    clock = pygame.time.Clock()
    user_input = ""
    result = ""
    stage = "team_selection"
    last_update = pygame.time.get_ticks()
    team_odds = {team: round(random.uniform(2, 5), 2) for team in teams}

    while True:
        screen.fill(DARK_BG)
        mouse_pos = pygame.mouse.get_pos()

        # Faza 1: Odabir tima
        if stage == "team_selection":
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= 500:
                team_odds = {team: round(random.uniform(2, 5), 2) for team in teams}
                last_update = current_time

            draw_text("Dobrodošli u Trku konja", font, ACCENT, screen, SCREEN_WIDTH // 2, 50, center=True)
            draw_text(f"Vaš balans: {balance} €", small_font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 100, center=True)
            draw_text("Odaberite konja:", font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 180, center=True)

            y_offset = 240
            buttons = []
            for i, team in enumerate(teams):
                border_color = ACCENT if selected_team == team else GRAY
                button = draw_button(f"{team} - Kvote: {team_odds[team]}", (SCREEN_WIDTH - 400) // 2, y_offset + i * 80, 400, 60, GRAY, border_color, mouse_pos, screen, selected_team == team)
                buttons.append((button, team))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button, team in buttons:
                        if button.collidepoint(mouse_pos):
                            selected_team = team
                            stage = "bet_input"

        # Faza 2: Unos uloga
        elif stage == "bet_input":
            draw_text(f"Vaš balans: {balance} €", small_font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 100, center=True)
            draw_text("Unesite iznos uloga ili odaberite opciju:", font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, 150, center=True)
            
            # Prikazivanje dugmadi za procente
            button_25 = draw_button(f"25% Balansa", (SCREEN_WIDTH - 400) // 2, 230, 400, 60, GRAY, ACCENT, mouse_pos, screen, False)
            button_50 = draw_button(f"50% Balansa", (SCREEN_WIDTH - 400) // 2, 310, 400, 60, GRAY, ACCENT, mouse_pos, screen, False)
            button_75 = draw_button(f"75% Balansa", (SCREEN_WIDTH - 400) // 2, 390, 400, 60, GRAY, ACCENT, mouse_pos, screen, False)
            button_100 = draw_button(f"100% Balansa", (SCREEN_WIDTH - 400) // 2, 470, 400, 60, GRAY, ACCENT, mouse_pos, screen, False)
            
            pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH // 2 - 100, 550, 200, 50), border_radius=10)
            draw_text(user_input, font, DARK_BG, screen, SCREEN_WIDTH // 2, 575, center=True)

            # Prikazivanje greške ako se unese 0 ili previše novca
            if user_input == "0":
                draw_text("Molimo unesite ulog veći od 0!", small_font, RED, screen, SCREEN_WIDTH // 2, 625, center=True)
            elif user_input.isdigit() and int(user_input) > balance:
                draw_text("Nemate dovoljno novca!", small_font, RED, screen, SCREEN_WIDTH // 2, 625, center=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and user_input.isdigit():
                        bet_amount = int(user_input)
                        if bet_amount <= balance and bet_amount > 0:
                            winner = race_animation()
                            if winner == selected_team:
                                # Koristi kvotu odabranog tima za izračunavanje dobitka
                                odds = team_odds[selected_team]
                                winnings = int(bet_amount * odds)
                                balance += winnings
                                result = f"Čestitamo! {winner} je pobijedio. Dobitak: {winnings} €."
                                win_sound.play()  # Zvuk pobede kada pobedite
                            else:
                                balance -= bet_amount
                                result = f"Žao nam je, {winner} je pobijedio. Izgubili ste {bet_amount} €."
                                lose_sound.play()  # Zvuk gubitka kada izgubite
                            stage = "result"
                        elif bet_amount <= 0:
                            result = "Ulog mora biti veći od 0!"
                        elif bet_amount > balance:
                            result = "Nemate dovoljno novca!"
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.unicode.isdigit():
                        user_input += event.unicode
                        
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Prikazivanje procenta uloga kada korisnik klikne na dugme
                    if button_25.collidepoint(mouse_pos):
                        bet_amount = int(balance * 0.25)
                        user_input = str(bet_amount)
                    elif button_50.collidepoint(mouse_pos):
                        bet_amount = int(balance * 0.50)
                        user_input = str(bet_amount)
                    elif button_75.collidepoint(mouse_pos):
                        bet_amount = int(balance * 0.75)
                        user_input = str(bet_amount)
                    elif button_100.collidepoint(mouse_pos):
                        bet_amount = balance
                        user_input = str(bet_amount)

        # Faza 3: Rezultat trke
        elif stage == "result":
            draw_text(result, font, GREEN if "Čestitamo" in result else RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, center=True)
            draw_text("Pritisnite R za novu igru ili ESC za izlaz.", small_font, LIGHT_TEXT, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        stage = "team_selection"
                        selected_team = None
                        user_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
