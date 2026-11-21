
import pygame
from clock import Clock

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

clock = Clock(screen)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.draw()

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
