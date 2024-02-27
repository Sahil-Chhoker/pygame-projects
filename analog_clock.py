import pygame
from math import cos, sin, pi
import datetime

# screen stats
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

# logic to draw numbers
def numbers(number, size, position):
    font = pygame.font.SysFont("Arial", size, True, False)
    text = font.render(number, True, WHITE)
    text_rect = text.get_rect(center=(position))
    screen.blit(text, text_rect)

# logic for converting polar coordinates to cartesian coordinates
def polar_to_cartesian(r, theta):
    x = r * sin(pi * theta / 180)
    y = r * cos(pi * theta / 180)
    return x + WIDTH / 2, -(y - HEIGHT / 2)

# main loop
def main():
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # for time in clock
        current_time = datetime.datetime.now()
        second = current_time.second
        minute = current_time.minute
        hour = current_time.hour

        # for styling the clock
        day = current_time.day
        month = current_time.month
        year = current_time.year
        weekday = current_time.today().isoweekday()
        calander = current_time.today().isocalendar()

        # converting week numbers to string
        weekdays_abbr = {1: "Mo", 2: "Tu", 3: "Wed", 4: "Th", 5: "Fri", 6: "Sat", 7: "Sun"}
        weekday_abbr = weekdays_abbr.get(weekday)

        # converting month numbers to string
        months_abbr = {1: "JAN", 2: "FEB", 3: "MAR", 4: "APR", 5: "MAY", 6: "JUN", 7: "JUL", 8: "AUG", 9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"}
        month_abbr = months_abbr.get(month)

        screen.fill(BLACK)
        pygame.draw.circle(screen, WHITE, center, clock_radius - 15, 8)
        pygame.draw.circle(screen, WHITE, center, 15)

        # drawing rectangles to make the clock more attractive
        pygame.draw.rect(screen, WHITE, [WIDTH / 2 - 260, HEIGHT / 2 - 30, 80, 60], 1)
        pygame.draw.rect(screen, WHITE, [WIDTH / 2 - 180, HEIGHT / 2 - 30, 80, 60], 1)
        pygame.draw.rect(screen, WHITE, [WIDTH / 2 + 100, HEIGHT / 2 - 30, 80, 60], 1)
        pygame.draw.rect(screen, WHITE, [WIDTH / 2 + 180, HEIGHT / 2 - 30, 80, 60], 1)
        pygame.draw.rect(screen, WHITE, [WIDTH / 2 - 50, HEIGHT / 2 - 30 + 160, 100, 60], 1)

        numbers(str(weekday_abbr), 40, (WIDTH/2 - 220, HEIGHT / 2))
        numbers(str(calander[1]), 40, (WIDTH/2 - 140, HEIGHT / 2))
        numbers(str(month_abbr), 40, (WIDTH/2 + 140, HEIGHT / 2))
        numbers(str(day), 40, (WIDTH/2 + 220, HEIGHT / 2))
        numbers(str(year), 40, (WIDTH/2 , HEIGHT / 2 + 160))

        # drawing numbers
        for number in range(1, 13):
            numbers(str(number), 80, polar_to_cartesian(clock_radius - 80, number * 30))

        # drawing clock ticks
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

        # control the fps
        clock.tick(FPS)

    pygame.quit()

# calling the main function
main()