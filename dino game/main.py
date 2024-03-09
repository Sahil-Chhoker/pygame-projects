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
game_over_sprite = pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/game_over.png')
dead_dino_sprite = pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/hurt_dino.png')
bird_sprites = [
    pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/bird_0.png'),
    pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/bird_1.png')
]


class Dino(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.is_animating = False
        self.current_sprite = 0
        self.image = dino_sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.vel_y = 0
        self.collided = False
        self.collided_with_obstacle = False

        self.rect.width -= 10
        self.rect.height -= 10

    def jump(self, jump_force):
        if self.rect.bottom == HEIGHT - 36:
            self.vel_y = -jump_force

    def die(self, obstacles, cloud_list):
        if not self.collided_with_obstacle:
            for obstacle in obstacles:
                collide = self.rect.colliderect(obstacle.rect)
                if collide:
                    self.collided_with_obstacle = True
                    obstacle.is_updating = False
                    for cloud in cloud_list:
                        cloud.is_updating = False
                    break

    def animate(self):
        self.is_animating = True

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
        self.is_updating = True
        self.image = random.choice(cacti_sprites)
        self.rect = self.image.get_rect(bottomleft=(pos_x, pos_y))
        self.speed = speed

        self.rect.width -= 15

    def update(self):
        if self.is_updating:
            self.rect.x -= self.speed


class Clouds(pygame.sprite.Sprite):
    def __init__(self, posx, posy, speed):
        super().__init__()
        self.is_updating = True
        self.image = cloud_sprite
        self.rect = self.image.get_rect(bottomleft=(posx, posy))
        self.speed = speed

    def update(self):
        if self.is_updating:
            self.rect.x -= self.speed


class GameManager:
    def __init__(self, dino, obstacles, cloud_list, moving_sprites, obstacle_spawned):
        self.dino = dino
        self.obstacles = obstacles
        self.cloud_list = cloud_list
        self.moving_sprites = moving_sprites
        self.obstacle_spawned = obstacle_spawned

        self.game_over_sprite = pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/game_over.png')
        self.restart_button_sprite = pygame.image.load('C:/MASTER FOLDER/pygame-projects/dino game/assets/dino/restart.png')
        self.restart_button_rect = self.restart_button_sprite.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    def show_game_over(self, window):
        window.blit(self.game_over_sprite, (WIDTH // 2 - self.game_over_sprite.get_width() // 2, HEIGHT // 2 - self.game_over_sprite.get_height() // 2))
        window.blit(self.restart_button_sprite, self.restart_button_rect)

    def restart_button_clicked(self, mouse_pos):
        return self.restart_button_rect.collidepoint(mouse_pos)
    
    def reset_game_state(self):
        self.game_over = False
        self.obstacle_spawned = False
        self.dino.rect.topleft = (100, 100)
        self.dino.collided_with_obstacle = False
        self.obstacles.empty()
        self.cloud_list.empty()
    

class Bird(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.is_moving = True
        self.is_animating = False
        self.current_sprite = 0
        self.image = bird_sprites[self.current_sprite]
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

    def animate(self):
        self.is_animating = True

    def update(self, dx):
        if self.is_animating:
            self.current_sprite += dx
            if self.current_sprite >= len(bird_sprites):
                self.current_sprite = 0
            self.image = bird_sprites[int(self.current_sprite)]

    def move(self, speed):
        self.speed = speed
        if self.is_moving:
            self.rect.x -= self.speed


def main():
    run = True
    clock = pygame.time.Clock()

    moving_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    cloud_list = pygame.sprite.Group()
    dino = Dino(100, 100)
    birds = pygame.sprite.Group()
    ground = Ground()

    # variables
    jump_force = 15
    dx = 0.2
    game_speed = 10

    moving_sprites.add(dino)

    obstacle_spawned = False

    game_manager = GameManager(dino, obstacles, cloud_list, moving_sprites, obstacle_spawned)

    BIRD_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRD_EVENT, 15000)

    while run:
        clock.tick(60)
        WIN.fill(WHITE)

        new_bird = Bird(WIDTH, 460)
        new_bird.update(dx)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump(jump_force)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game_manager.restart_button_clicked(mouse_pos):
                    game_manager.reset_game_state()
            elif event.type == BIRD_EVENT: 
                new_bird.animate()
                birds.add(new_bird)

        # Draw ground
        ground.draw(WIN)

        # Update and draw sprites and gameover logic
        if dino.collided_with_obstacle:
            WIN.blit(dead_dino_sprite, dino.rect)
            game_manager.show_game_over(WIN)
        else:
            moving_sprites.update(dx)
            dino.animate()
            moving_sprites.draw(WIN)

        # Obstacle logic
        if not game_manager.obstacle_spawned:
            obstacle = Obstacle(WIDTH, HEIGHT - ground.height + 20, game_speed)
            obstacles.add(obstacle)
            game_manager.obstacle_spawned = True
        obstacles.update()
        obstacles.draw(WIN)
        if obstacle.rect.x + 50 < 0:
            obstacles.remove(obstacle)
            game_manager.obstacle_spawned = False

        # Debug
        # for obstacle in obstacles:
        #     pygame.draw.rect(WIN, "red", obstacle.rect, 2)
        # pygame.draw.rect(WIN, "green", dino.rect, 2)

        # Cloud logic
        if not dino.collided_with_obstacle:
            cloud = Clouds(WIDTH, random.randint(40, 100), game_speed)
            if random.randint(0, 100) < 3:
                cloud_list.add(cloud)
        cloud_list.update()
        cloud_list.draw(WIN)

        # Bird logic
        for bird in birds:
            bird.move(game_speed * 1.5)
            bird.update(dx)
        birds.draw(WIN)

        # Die logic
        dino.die(obstacles, cloud_list)

        # Update the screen
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
