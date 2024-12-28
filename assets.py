import pygame

def load_images():
    horse_image = pygame.image.load("horse.png")
    horse_image = pygame.transform.scale(horse_image, (60, 60))
    track_background = pygame.image.load("track_background.jpg")
    track_background = pygame.transform.scale(track_background, (1200, 800))
    return horse_image, track_background

def load_sounds():
    horse_running_sound = pygame.mixer.Sound("horse_running.wav")
    lose_sound = pygame.mixer.Sound("lose_sound.wav")
    win_sound = pygame.mixer.Sound("win_sound.wav")
    start_race_sound = pygame.mixer.Sound("start_race.wav")
    return horse_running_sound, lose_sound, win_sound, start_race_sound
