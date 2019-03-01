import sys, pygame, pygameMenu
from pygameMenu.locals import *
import random
import time

pygame.init()

MAX_NUMBER_OF_OBSTACLES = 20

OBSTACLE_INIT_WITDTH = 170
OBSTACLE_INIT_HEIGHT = 40

NUMBER_OF_LANES = 4

MOVE_SPEED_PLAYER = 8


SIZE = WIDTH, HEIGHT = 1000, 500
speed = [1, 1]
BLACK = 0, 0, 0
GREEN = 0, 255, 0
RED = 255, 0, 0
BG_COLOR = 20, 30, 70
PINK = 200, 111, 150

ZERO_POINT = [WIDTH // 2, HEIGHT // 3]

screen = pygame.display.set_mode(SIZE)


class Scoring:
    def __init__(self):
        self.score = 0
        self.high_score = 0

    def get_score(self):
        return self.score

    def get_high_score(self):
        return self.high_score

    def update_high_score(self):
        self.high_score = self.score

    def update_score(self, add_value):
        self.score += add_value

    def reset_score(self):
        self.score = 0


scoring = Scoring()


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
    def __init__(self, width, height, x=None, y=None):
        super().__init__()
        if random.random() < 0.01:
            self._image = pygame.image.load("src/assets/images/dash.png")
        else:
            self._image = pygame.Surface([width, height], pygame.SRCALPHA, 32)
            self._image.convert_alpha()
            pygame.draw.ellipse(self._image, BLACK, self._image.get_rect())

        lane_width = (WIDTH) / (NUMBER_OF_LANES)
        self.x = (
            x
            or int((random.randint(0, NUMBER_OF_LANES - 1) * lane_width))
            + lane_width / 2
        )
        self.y = y or random.randint(0, HEIGHT)
        self.set_position()

    def set_position(self):

        translate_y = self.y

        zp = ZERO_POINT[1]
        if self.y <= zp:
            factor = 0
        else:
            factor_y = self.y ** 2 / HEIGHT ** 2
            translate_y = zp + self.y * factor_y

            factor = (translate_y - zp) * (1 / (HEIGHT - zp))

        translate_x = self.x * factor + WIDTH * (1 - factor) / 2

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
    def __init__(self, joystick):
        super().__init__()
        self.crashed = False
        self.joystick = joystick
        self.image = pygame.image.load("src/assets/images/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - self.image.get_height() // 2)

    def handle_keys(self, event):
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            return
        elif key[pygame.K_RIGHT]:
            self.rect.x += MOVE_SPEED_PLAYER
        elif key[pygame.K_LEFT]:
            self.rect.x -= MOVE_SPEED_PLAYER
        elif key[pygame.K_x]:
            play_overlap("src/assets/sounds/car+horn+x.wav", max_time=250)

    def handle_joystick(self, event):
        if self.joystick and event.type == pygame.JOYAXISMOTION:
            x = self.joystick.get_axis(0)
            if x >= 0.05 or x <= -0.05:
                self.rect.x += x * MOVE_SPEED_PLAYER
        if event.type == pygame.JOYBUTTONDOWN:
            if self.joystick.get_button(1):
                play_overlap("src/assets/sounds/car+horn+x.wav", max_time=250)


def init_obstacles(n):
    obstacles = pygame.sprite.Group()
    for i in range(n):
        obstacles.add(Obstacle(OBSTACLE_INIT_WITDTH, OBSTACLE_INIT_HEIGHT))
    return obstacles


def tick_obstacles(delta_time, player, obstacles, obstacle_count, bottom_border):
    car_collision = pygame.sprite.spritecollide(player, obstacles, True)
    player.crashed = len(car_collision) > 0
    collisions = pygame.sprite.spritecollide(bottom_border, obstacles, True)
    for col in collisions:
        obstacles.remove(col)
    for obstacle in obstacles:
        obstacle.y += 1
        obstacle.set_position()
    while len(obstacles) < obstacle_count and random.random() * 100 < obstacle_count:
        obstacles.add(
            Obstacle(OBSTACLE_INIT_WITDTH, OBSTACLE_INIT_HEIGHT, None, ZERO_POINT[1])
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


def draw(all_sprites):

    screen.fill(BG_COLOR)
    text_to_screen(
        screen,
        "BEST SCORE: {score}m".format(score=scoring.get_high_score()),
        20,
        20,
        30,
        GREEN,
    )
    text_to_screen(
        screen, "SCORE: {score}m".format(score=scoring.get_score()), 20, 60, 20, RED
    )

    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    draw_lines()


def init_joystick(pygame):
    if not pygame.joystick.get_count():
        return None

    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    return joystick


def mainmenu_background():
    screen.fill((40, 0, 40))


def play_the_game():
    main()


def play_sound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(0)


def play_overlap(sound, max_time=500):
    pygame.mixer.Channel(0).play(pygame.mixer.Sound(sound), maxtime=max_time)


def show_menu():
    menu_text = "Your score: {0}".format(scoring.get_score())
    if scoring.get_score() > scoring.get_high_score():
        scoring.update_high_score()

    menu = pygameMenu.Menu(
        screen,
        WIDTH,
        HEIGHT,
        pygameMenu.fonts.FONT_NEVIS,
        "Crash! Score: {0}".format(scoring.get_score()),
        bgfun=mainmenu_background,
    )

    menu.add_option("Try Again", play_the_game)
    menu.add_option("Exit", PYGAME_MENU_EXIT)
    menu.mainloop(pygame.event.get())


def main():

    play_sound("src/assets/sounds/background.mp3")

    clock = pygame.time.Clock()
    bottom_border = Border(PINK, WIDTH * 10, 1000, WIDTH, HEIGHT + 498)

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    obstacle_count = 0
    all_sprites.add(bottom_border)

    joystick = init_joystick(pygame)

    player = Player(joystick)
    all_sprites.add(player)
    quit = False
    scoring.reset_score()

    while not quit:
        for event in pygame.event.get():
            quit = event.type == pygame.QUIT
            player.handle_joystick(event)

        player.handle_keys(event)

        draw(all_sprites)
        delta_time = clock.tick(60)
        scoring.update_score(delta_time)
        obstacle_count = (scoring.get_score() / 100) ** 0.3

        (obstacles, num_collisions) = tick_obstacles(
            delta_time, player, obstacles, obstacle_count, bottom_border
        )
        all_sprites.empty()
        all_sprites.add(player)
        all_sprites.add(*obstacles)
        pygame.display.flip()

        # TODO: Show menu after car accident
        if player.crashed:
            pygame.mixer.music.stop()
            play_sound("src/assets/sounds/Explosion+5.mp3")
            time.sleep(1)
            show_menu()


if __name__ == "__main__":
    main()
