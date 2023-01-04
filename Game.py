import pygame
import random
import sys
import os
WINDOW_RATIO = 0.9
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 720 * WINDOW_RATIO, 1080 * WINDOW_RATIO
TITLE_SIZE = 50
SPEED = 5 * WINDOW_RATIO
ENEMY_EVENT_TYPE = 30
FPS = 120


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.image.fill((120, 200, 100))


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):

        super().__init__(all_sprites)
        radius = radius * WINDOW_RATIO
        self.radius = radius

        # image = load_image("pine2.png")
        # self.image_cones = pygame.transform.scale(image, (radius * 5 * WINDOW_RATIO, radius * 5 * WINDOW_RATIO))
        # screen.blit(self.image_cones, (x, y))
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)

        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)

        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy

        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, surf, group):
        super(Car, self).__init__()
        self.image = surf
        self.rect = self.image.get_rect(center=(x, y))
        self.add(group)

    def update(self):
        if self.rect.y < WINDOW_HEIGHT:
            self.rect.y += SPEED * 0.6
        else:
            self.kill()


pins = pygame.sprite.Group()


class Hero:

    def __init__(self):
        image = load_image("bear.png")
        self.image_bear = pygame.transform.scale(image, (125 * WINDOW_RATIO, 125 * WINDOW_RATIO))
        self.image_bear_right = self.image_bear
        self.image_bear_left = pygame.transform.flip(self.image_bear, 1, 0)
        self.width = self.image_bear.get_width()
        self.x, self.y = WINDOW_WIDTH // 2, WINDOW_HEIGHT - self.image_bear.get_height()\
                         - self.image_bear.get_height() * 0.2


    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen, flag):
        if flag == 'left':
            self.image_bear = self.image_bear_left
        else:
            self.image_bear = self.image_bear_right
        screen.blit(self.image_bear, (self.x, self.y))


class Game:

    def __init__(self, hero):
        self.hero = hero
        self.flag = True

    def render(self, screen):
        self.hero.render(screen, self.flag)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= SPEED
            self.flag = 'left'

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += SPEED
            self.flag = 'right'

        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= SPEED

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += SPEED

        if 0 < next_x < WINDOW_WIDTH - self.hero.width:
            self.hero.set_position((next_x, next_y))

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def main():

    pygame.init()
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, 500)
    screen = pygame.display.set_mode(WINDOW_SIZE)

    Border(5, 5, WINDOW_WIDTH - 5, 5)
    Border(5, WINDOW_HEIGHT - 5, WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
    Border(5, 5, 5, WINDOW_HEIGHT - 5)
    Border(WINDOW_WIDTH - 5, 5, WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
    for i in range(0):
        Ball(20, 100, 100)

    image = load_image("фон.png")
    image_background = pygame.transform.scale(image, WINDOW_SIZE)
    image_pine = load_image("shishka2.png")
    image_pine = pygame.transform.scale(image_pine, (70 * WINDOW_RATIO, 70 * WINDOW_RATIO))
    image_pine = pygame.transform.flip(image_pine, 0, 1)

    hero = Hero()
    game = Game(hero)
    Car(random.randint(1, WINDOW_HEIGHT), random.randint(1, WINDOW_WIDTH // 2), image_pine, pins)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.USEREVENT:
                Car(random.randint(1, WINDOW_HEIGHT), random.randint(1, WINDOW_WIDTH // 2), image_pine, pins)

        screen.fill(pygame.Color('black'))
        screen.blit(image_background, (0, 0))

        all_sprites.draw(screen)
        all_sprites.update()

        pins.draw(screen)
        pins.update()

        game.update_hero()
        game.render(screen)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()