import sys, pygame

pygame.init()

size = width, height = 1200, 1000
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("src/ball_noun_001_01090.jpg")
        self.rect = self.image.get_rect()


def init_obstacles(n):
    obstacle_group = pygame.sprite.Group()
    for i in range(n):
        obstacle_group.add(Obstacle((0, 0, 0), 20, 20))
    return obstacle_group


all_sprites = pygame.sprite.Group()

obstacles = init_obstacles(10)
all_sprites.add(*obstacles)

player = Player()
all_sprites.add(player)


quit = False

while not quit:
    for event in pygame.event.get():
        quit = event.type == pygame.QUIT

    screen.fill(black)
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)
    pygame.display.flip()
