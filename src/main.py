import sys, pygame
import random

pygame.init()

MAX_NUMBER_OF_OBSTACLES = 20

OBSTACLE_INIT_WITDTH = 100
OBSTACLE_INIT_HEIGHT = 80

NUMBER_OF_LANES = 2

SIZE = WIDTH, HEIGHT = 850, 480
speed = [1, 1]
BLACK = 0, 0, 0
GREEN = 0, 255, 0
RED = 255, 0, 0

SCORE = 0

ZERO_POINT = [WIDTH//2, HEIGHT//3]

screen = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()

#class Background(pygame.sprite.Sprite):
#    def __init__(self, image_file, location):
#        self.image = pygame.image.load(image_file)
#        self.rect = self.image.get_rect()
#        self.rect.left, self.rect.top = location

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x=None, y=None):
        super().__init__()
        self._image = pygame.Surface([width, height])
        self._image.fill(color)
        self.x = x or int(random.randint(0, NUMBER_OF_LANES) * (WIDTH / NUMBER_OF_LANES))
        self.y = y or random.randint(0, HEIGHT)
        self.set_position()

    def set_position(self):
        factor = max(0, (self.y - ZERO_POINT[1]) / HEIGHT)
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
        obstacles.add(Obstacle(RED, OBSTACLE_INIT_WITDTH, OBSTACLE_INIT_HEIGHT))
    return obstacles


def tick_obstacles(delta_time, obstacles, obstacle_count, bottom_border):
    collisions = pygame.sprite.spritecollide(bottom_border, obstacles, True)
    for col in collisions:
        obstacles.remove(col)
    for obstacle in obstacles:
        obstacle.y += 1
        obstacle.set_position()
    while len(obstacles) < obstacle_count:
        obstacles.add(Obstacle(RED, OBSTACLE_INIT_WITDTH, OBSTACLE_INIT_HEIGHT, None, ZERO_POINT[1]))
    return (obstacles, len(collisions))

def text_to_screen(screen, text, x, y, size = 50, color = (200, 000, 000), font_type = 'data/fonts/orecrusherexpand.ttf'):
    text = str(text)
    default_font = pygame.font.get_default_font()
    font = pygame.font.Font(default_font, size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

#BACKGROUND = Background('src/back.jpg', [0,0])

bottom_border = Obstacle(BLACK, WIDTH, 2, 0, HEIGHT - 2)

all_sprites = pygame.sprite.Group()

obstacles = init_obstacles(10)
all_sprites.add(*obstacles)

#player = Player()
#all_sprites.add(player)

quit = False

while not quit:
    for event in pygame.event.get():
        quit = event.type == pygame.QUIT

    screen.fill([255, 255, 255])
    #screen.blit(BACKGROUND.image, BACKGROUND.rect)
    
    text_to_screen(screen, "SCORE: {score}m".format(score=SCORE), 20, 20)
    pygame.draw.line(screen, GREEN, ZERO_POINT, [0,HEIGHT], 2)
    pygame.draw.line(screen, GREEN, ZERO_POINT, [WIDTH,HEIGHT], 2)

    for i in range(NUMBER_OF_LANES - 1):
        line_bottom_x = (WIDTH // NUMBER_OF_LANES) * (i + 1)
        pygame.draw.line(screen, RED, ZERO_POINT, [line_bottom_x, HEIGHT], 1)

    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    delta_time = clock.tick(60)
    (obstacles, num_collisions) = tick_obstacles(delta_time, obstacles, MAX_NUMBER_OF_OBSTACLES, bottom_border)
    SCORE += 1
    all_sprites.empty()
    #all_sprites.add(player)
    all_sprites.add(*obstacles)
    pygame.display.flip()
