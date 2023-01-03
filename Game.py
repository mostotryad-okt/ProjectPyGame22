import pygame
import random
import sys
import os
WINDOW_RATIO = 0.9
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 720 * WINDOW_RATIO, 1080 * WINDOW_RATIO
TITLE_SIZE = 50
FPS = 60


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Hero:

    def __init__(self, position):
        self.x, self.y = position

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position

    def render(self, screen):
        center = self.x * TITLE_SIZE + TITLE_SIZE // 2, self.y * TITLE_SIZE + TITLE_SIZE // 2
        pygame.draw.circle(screen, (255, 255, 255), center, TITLE_SIZE // 2)


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        radius = radius * WINDOW_RATIO
        self.radius = radius
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


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.image.fill(pygame.Color('yellow'))

class Game:

    def __init__(self, hero):
        self.hero = hero

    def render(self, screen):
        self.hero.render(screen)

    def update_hero(self):
        next_x, next_y = self.hero.get_position()
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            next_x -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            next_x += 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            next_y -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += 1
        '''if self.labyrinth.is_free((next_x, next_y)):
            self.hero.set_position((next_x, next_y))'''


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    Border(5, 5, WINDOW_WIDTH - 5, 5)
    Border(5, WINDOW_HEIGHT - 5, WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
    Border(5, 5, 5, WINDOW_HEIGHT - 5)
    Border(WINDOW_WIDTH - 5, 5, WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
    image = load_image("фон.png")
    image1 = pygame.transform.scale(image, WINDOW_SIZE)
    for i in range(10):
        Ball(20, 100, 100)
    hero = Hero((100, 100))
    game = Game(hero)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        screen.fill(pygame.Color('black'))
        screen.blit(image1, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        game.render(screen)
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()