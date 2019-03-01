import sys, pygame
import random

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()

MAX_NUMBER_OF_OBSTACLES = 20

OBSTACLE_INIT_WITDTH = 100
OBSTACLE_INIT_HEIGHT = 100

NUMBER_OF_LANES = 4

MOVE_SPEED_PLAYER = 8


SIZE = WIDTH, HEIGHT = 1000, 500
speed = [1, 1]
BLACK = 0, 0, 0
GREEN = 0, 255, 0
RED = 255, 0, 0
BG_COLOR = 10, 20, 50
PINK = 200, 111, 150


SCORE = 0

ZERO_POINT = [WIDTH // 2, HEIGHT // 3]

screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()


class Border(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x=None, y=None):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x=None, y=None):
        super().__init__()
        self._image = pygame.Surface([width, height], pygame.SRCALPHA, 32)
        self._image.convert_alpha()
        pygame.draw.circle(self._image, PINK, (width // 2, height // 2), height // 2)

        lane_width = (WIDTH) / (NUMBER_OF_LANES)
        self.x = (
            x
            or int((random.randint(0, NUMBER_OF_LANES - 1) * lane_width))
            + lane_width / 2
        )
        self.y = y or random.randint(0, HEIGHT)
        self.set_position()

    def set_position(self):

        ff = self.y ** 2 / HEIGHT ** 2
        translate_y = self.y

        zp = ZERO_POINT[1]
        if self.y < zp:
            factor = 0
        else:
            factor = (self.y - zp) * (1 / (HEIGHT - zp))

        translate_x = self.x * factor + WIDTH * (1 - factor) / 2
        print(
            "{:>3}   {:>5}   {:>5}    {:>5} ".format(
                self.y, factor, self.x, translate_x
            )
        )

        self.image = pygame.transform.scale(
            self._image,
            (
                int(self._image.get_width() * factor),
                int(self._image.get_height() * factor),
            ),
        )

        self.rect = self.image.get_rect()
        self.rect.center = (translate_x, translate_y)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("src/assets/images/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - self.image.get_height() // 2 - 50)

    def handle_keys(self, event):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            self.rect.x += MOVE_SPEED_PLAYER
        elif key[pygame.K_LEFT]:
            self.rect.x -= MOVE_SPEED_PLAYER
        elif event.type == pygame.JOYAXISMOTION:
            x = j.get_axis(0)
            if x >= 0.1 or x <= -0.1:
                self.rect.x += x * MOVE_SPEED_PLAYER * 1.5


def init_obstacles(n):
    obstacles = pygame.sprite.Group()
    for i in range(n):
        obstacles.add(Obstacle(RED, OBSTACLE_INIT_WITDTH, OBSTACLE_INIT_HEIGHT))
    return obstacles


def tick_obstacles(delta_time, obstacles, obstacle_count, bottom_border):
    collisions = pygame.sprite.spritecollide(bottom_border, obstacles, True)
    for col in collisions:
        obstacles.remove(col)
    for obstacle in obstacles:
        obstacle.y += 1
        obstacle.set_position()
    while len(obstacles) < obstacle_count and random.random() * 100 < obstacle_count:
        obstacles.add(
            Obstacle(
                RED, OBSTACLE_INIT_WITDTH, OBSTACLE_INIT_HEIGHT, None, ZERO_POINT[1]
            )
        )
    return (obstacles, len(collisions))


def text_to_screen(
    screen,
    text,
    x,
    y,
    size=50,
    color=(200, 000, 000),
    font_type="data/fonts/orecrusherexpand.ttf",
):
    text = str(text)
    default_font = pygame.font.get_default_font()
    font = pygame.font.Font(default_font, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


def draw_lines():
    pygame.draw.line(screen, GREEN, ZERO_POINT, [0, HEIGHT], 2)
    pygame.draw.line(screen, GREEN, ZERO_POINT, [WIDTH, HEIGHT], 2)

    for i in range(NUMBER_OF_LANES - 1):
        line_bottom_x = (WIDTH // NUMBER_OF_LANES) * (i + 1)
        pygame.draw.line(screen, RED, ZERO_POINT, [line_bottom_x, HEIGHT], 1)


def draw(all_sprites, score):

    screen.fill(BG_COLOR)
    text_to_screen(screen, "SCORE: {score}m".format(score=score), 20, 20)

    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    draw_lines()


def main():
    bottom_border = Obstacle(BLACK, WIDTH, 2, 0, HEIGHT - 2)
    bottom_border = Border(PINK, WIDTH * 10, 1000, WIDTH, HEIGHT + 498)

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    obstacle_count = 0
    all_sprites.add(bottom_border)

    player = Player()
    all_sprites.add(player)

    quit = False
    score = 0

    while not quit:
        for event in pygame.event.get():
            quit = event.type == pygame.QUIT

        player.handle_keys(event)

        draw(all_sprites, score)
        delta_time = clock.tick(60)
        score += delta_time
        obstacle_count = (score / 100) ** 0.3

        (obstacles, num_collisions) = tick_obstacles(
            delta_time, obstacles, obstacle_count, bottom_border
        )
        all_sprites.empty()
        all_sprites.add(player)
        all_sprites.add(*obstacles)
        pygame.display.flip()


if __name__ == "__main__":
    main()
