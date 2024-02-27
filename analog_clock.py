import pygame
from math import cos, sin, pi
import datetime

HEIGHT, WIDTH = 800, 800
center = (WIDTH/2, HEIGHT/2)
clock_radius = 400

pygame.init()

# screen stats
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Analog Clock")
clock = pygame.time.Clock()
FPS = 60

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


def main():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        screen.fill(BLACK)
        pygame.draw.circle(screen, WHITE, center, clock_radius - 15, 8)

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()



main()