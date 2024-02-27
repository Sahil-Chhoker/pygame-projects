import pygame

HEIGHT, WIDTH = 800, 800

pygame.init()

# screen stats
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Analog Clock")
clock = pygame.time.Clock()
FPS = 60

