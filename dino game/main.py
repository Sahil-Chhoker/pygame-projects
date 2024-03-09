import pygame
import random

pygame.init()

# Screen stats
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weird Dino")

# Colors
WHITE = (255, 255, 255)
DARK_GREY = (80, 78, 81)

# Load images
dino_sprites = [
    pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/dino_2.png'),
    pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/dino_3.png')
]
cacti_sprites = [
    pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/cactus_0.png'),
    pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/cactus_1.png'),
    pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/cactus_2.png'),
    pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/big_cactus_1.png'),
    pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/cacti_group_0.png'),
    pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/cacti_group_1.png')
]
cloud_sprite = pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/cloud.png')


class Dino(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.is_animating = False
        self.current_sprite = 0
        self.image = dino_sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.vel_y = 0

    def animate(self):
        self.is_animating = True

    def jump(self, jump_force):
        if self.rect.bottom == HEIGHT - 36:
            self.vel_y = -jump_force

    def update(self, speed):
        if self.is_animating:
            self.current_sprite += speed
            if self.current_sprite >= len(dino_sprites):
                self.current_sprite = 0
                self.is_animating = False
            self.image = dino_sprites[int(self.current_sprite)]

        # Apply gravity
        self.vel_y += 0.7
        self.rect.y += self.vel_y

        if self.rect.bottom >= HEIGHT - 36:
            self.rect.bottom = HEIGHT - 36
            self.vel_y = 0


class Ground:
    def __init__(self):
        self.width = 100000
        self.height = 50
        self.rect = pygame.Rect(0, HEIGHT - self.height, self.width, self.height)
        self.ground_color = DARK_GREY

    def draw(self, surface):
        pygame.draw.rect(surface, self.ground_color, self.rect, 4)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, speed):
        super().__init__()
        self.image = random.choice(cacti_sprites)
        self.rect = self.image.get_rect(bottomleft=(pos_x, pos_y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed


class Clouds(pygame.sprite.Sprite):
    def __init__(self, posx, posy, speed):
        super().__init__()
        self.image = cloud_sprite
        self.rect = self.image.get_rect(bottomleft=(posx, posy))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed


def main():
    run = True
    clock = pygame.time.Clock()

    moving_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    cloud_list = pygame.sprite.Group()
    dino = Dino(100, 100)
    ground = Ground()

    moving_sprites.add(dino)

    obstacle_spawned = False

    while run:
        clock.tick(60)
        WIN.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump(jump_force=15)

        # Draw ground
        ground.draw(WIN)

        # Update and draw sprites
        moving_sprites.update(0.2)
        moving_sprites.draw(WIN)
        dino.animate()

        # Obstacle logic
        if not obstacle_spawned:
            obstacle = Obstacle(WIDTH, HEIGHT - ground.height + 20, 6)
            obstacles.add(obstacle)
            obstacle_spawned = True
        obstacles.update()
        obstacles.draw(WIN)
        if obstacle.rect.x + 50 < 0:
            obstacles.remove(obstacle)
            obstacle_spawned = False

        # Cloud logic
        if random.randint(0, 100) < 3:
            cloud = Clouds(WIDTH, random.randint(40, 100), 6)
            cloud_list.add(cloud)
        cloud_list.update()
        cloud_list.draw(WIN)

        # Update the screen
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
