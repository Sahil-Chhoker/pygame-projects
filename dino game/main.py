import pygame
import math

from pygame.sprite import Group
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
        self.is_animating = False
        self.sprites = [
            pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/dino_2.png'),
            pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/dino_3.png')
        ]
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.vel_y = 0  
        
    def animate(self):
        self.is_animating = True

    def update(self, speed):
        if self.is_animating:
            self.current_sprite += speed
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = self.sprites[int(self.current_sprite)]

        # Apply gravity
        self.vel_y += 0.5
        self.rect.y += self.vel_y

        if self.rect.bottom >= HEIGHT - 36:
            self.rect.bottom = HEIGHT - 36
            self.vel_y = 0
            
class DrawWorld(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.ground = pygame.Surface((WIDTH, 50))
        self.ground.fill(DARK_GREY)
        self.rect = self.ground.get_rect()
        self.rect.bottom = HEIGHT
        
    def draw(self, surface):
        surface.blit(self.ground, self.rect)
        
def main():
    run = True
    clock = pygame.time.Clock()

    moving_sprites = pygame.sprite.Group()
    dino = Dino(100, 100)
    world = DrawWorld()

    moving_sprites.add(dino)

    while run:
        clock.tick(60)
        WIN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        moving_sprites.update(0.2)
        dino.animate()
        moving_sprites.draw(WIN)
        world.draw(WIN)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
	main()