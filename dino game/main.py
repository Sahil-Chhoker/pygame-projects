import pygame
import math
pygame.init()

# screen stats
WIDTH, HEIGHT =  800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wierd Dino")

# colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Dino(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.sprites = []
		self.sprites.append(pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/dino_2.png'))
		self.sprites.append(pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/dino_3.png'))
		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]

		self.rect = self.image.get_rect()
		self.rect.topleft = [pos_x, pos_y]

def main():
	run = True
	clock = pygame.time.Clock()

	moving_sprites = pygame.sprite.Group()
	dino = Dino(100, 100)

	moving_sprites.add(dino)

	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		moving_sprites.draw(WIN)
		pygame.display.update()

	pygame.quit()


main()