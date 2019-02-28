import sys, pygame
import random

pygame.init()

SIZE = WIDTH, HEIGHT = 1200, 1000
speed = [1, 1]
BLACK = 0, 0, 0
PINK = 200, 111, 150

screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x=None, y=None):
        super().__init__()
        self._image = pygame.Surface([width, height])
        self._image.fill(color)
        self.x = x or int(random.randint(0, 5) * (WIDTH / 5))
        self.y = y or random.randint(0, HEIGHT)
        self.set_position()

    def set_position(self):
        factor = self.y / HEIGHT
        self.image = pygame.transform.scale(
            self._image,
            (
                int(self._image.get_width() * factor),
                int(self._image.get_height() * factor),
            ),
        )

        translate_x = self.x * factor + WIDTH * (1 - factor) / 2
        translate_y = self.y

        self.rect = self.image.get_rect()
        self.rect.center = (translate_x, translate_y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("src/ball_noun_001_01090.jpg")
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - self.image.get_height() // 2 - 50)


def init_obstacles(n):
    obstacles = pygame.sprite.Group()
    for i in range(n):
        obstacles.add(Obstacle((52, 220, 60), 40, 40))
    return obstacles


def tick_obstacles(delta_time, obstacles, obstacle_count, bottom_border):
    collisions = pygame.sprite.spritecollide(bottom_border, obstacles, True)
    for col in collisions:
        obstacles.remove(col)
    for obstacle in obstacles:
        obstacle.y += 1
        obstacle.set_position()
    while len(obstacles) < obstacle_count:
        obstacles.add(Obstacle((52, 220, 60), 40, 40, None, 1))
    return obstacles


bottom_border = Obstacle(PINK, WIDTH, 2, 0, HEIGHT - 2)

all_sprites = pygame.sprite.Group()

obstacles = init_obstacles(10)
all_sprites.add(*obstacles)

player = Player()
all_sprites.add(player)


quit = False

while not quit:
    for event in pygame.event.get():
        quit = event.type == pygame.QUIT

    screen.fill(BLACK)

    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    delta_time = clock.tick(60)
    obstacles = tick_obstacles(delta_time, obstacles, 11, bottom_border)
    all_sprites.empty()
    all_sprites.add(player)
    all_sprites.add(*obstacles)
    pygame.display.flip()
