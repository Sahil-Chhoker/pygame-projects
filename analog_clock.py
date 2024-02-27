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

def numbers(number, size, position):
    font = pygame.font.SysFont("Arial", size, True, False)
    text = font.render(number, True, WHITE)
    text_rect = text.get_rect(center=(position))
    screen.blit(text, text_rect)

def polar_to_cartesian(r, theta):
    x = r * sin(pi * theta / 180)
    y = r * cos(pi * theta / 180)
    return x + WIDTH / 2, -(y - HEIGHT / 2)

def main():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        current_time = datetime.datetime.now()
        second = current_time.second
        minute = current_time.minute
        hour = current_time.hour

        screen.fill(BLACK)
        pygame.draw.circle(screen, WHITE, center, clock_radius - 15, 8)
        pygame.draw.circle(screen, WHITE, center, 15)

        for number in range(1, 13):
            numbers(str(number), 80, polar_to_cartesian(clock_radius - 80, number * 30))

        for number in range(0, 360, 6):
            if number % 5:
                pygame.draw.line(screen, WHITE, polar_to_cartesian(clock_radius - 15, number), polar_to_cartesian(clock_radius - 30, number), 2)
            else:
                pygame.draw.line(screen, WHITE, polar_to_cartesian(clock_radius - 15, number), polar_to_cartesian(clock_radius - 30, number), 6)


        # hours arrow
        r = 250
        theta = (hour + minute / 60 + second / 3600) * (360 / 12)
        pygame.draw.line(screen, WHITE, center, polar_to_cartesian(r, theta), 14)


        # minutes arrow
        r = 280
        theta = (minute + second / 60) * (360 / 60)
        pygame.draw.line(screen, WHITE, center, polar_to_cartesian(r, theta), 10)

        # seconds arrow
        r = 340
        theta = second * (360/60)
        pygame.draw.line(screen, RED, center, polar_to_cartesian(r, theta), 4)

        pygame.display.update()

        clock.tick(FPS)

    pygame.quit()



main()