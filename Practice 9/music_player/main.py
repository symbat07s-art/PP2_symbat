
import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 20)

player = MusicPlayer()

running = True

while running:
    screen.fill((230, 220, 250))

    title = font.render("MY MUSIC PLAYER", True, (60, 30, 90))
    screen.blit(title, (150, 60))

    song_text = small_font.render(
        "Song: " + str(player.current_song + 1),
        True,
        (60, 30, 90)
    )
    screen.blit(song_text, (230, 130))

    controls = small_font.render(
        "P - Play | S - Stop | N - Next | B - Previous | Q - Quit",
        True,
        (60, 30, 90)
    )
    screen.blit(controls, (35, 220))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()

            if event.key == pygame.K_s:
                player.stop()

            if event.key == pygame.K_n:
                player.next_song()

            if event.key == pygame.K_b:
                player.previous_song()

            if event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()
