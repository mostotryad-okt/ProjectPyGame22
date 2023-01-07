import pygame
import random
import sys
import os
WINDOW_RATIO = 0.8
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 720 * WINDOW_RATIO, 1080 * WINDOW_RATIO
TITLE_SIZE = 50
SPEED = 10 * WINDOW_RATIO
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


def terminate():
    pygame.quit()
    sys.exit()

def render_start_screen(screen, x1, x2, image_bear, image_pine):
    screen.blit(image_bear, (x1, int(WINDOW_HEIGHT * 0.8)))
    screen.blit(image_pine, (x2, int(WINDOW_HEIGHT * 0.8)))
    if x1 >= WINDOW_WIDTH:
        x1 = -SPEED * 2
    if x2 >= WINDOW_WIDTH:
        x2 = -SPEED * 2
    return x1 + SPEED * 2, x2 + SPEED * 2


def start_screen(screen):
    intro_text = ["Мишка косолапый по лесу идет,",
                  "Шишки собирает, песенки поет.",
                  "Вдруг упала шишка, прямо мишке в лоб,",
                  "Мишка оступился и об землю хлоп!"]

    fon = pygame.transform.scale(load_image('фон.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, int(35 * WINDOW_RATIO))
    text_coord = 460 * WINDOW_RATIO
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 191, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WINDOW_WIDTH // 2 - string_rendered.get_width() // 2
        text_coord += intro_rect.height
        text_w = string_rendered.get_width()
        text_h = string_rendered.get_height()
        # pygame.draw.rect(screen, (255, 255, 255), (intro_rect[0] - 5, intro_rect[1] - 5, intro_rect[2] + 10, intro_rect[3] + 10))
        screen.blit(string_rendered, intro_rect)


def show_message(screen, message, flag, message2 = '100', message3 = '100'):
    if flag:
        font = pygame.font.Font(None, int(50 * WINDOW_RATIO))
        distance = 0.04
        interval = distance

        text = font.render('SCR: ' + message, 1, (0, 75, 100))
        text_x = WINDOW_WIDTH // 40
        text_y = WINDOW_HEIGHT * interval
        interval += distance
        screen.blit(text, (text_x, text_y))

        text = font.render('HLTH: ' + str(round(float(message2), 1)) + '%', 1, (175, 0, 25))
        text_x = WINDOW_WIDTH // 40
        text_y = WINDOW_HEIGHT * interval
        interval += distance
        screen.blit(text, (text_x, text_y))

        text = font.render('LVL: ' + str(100 - float(message3)) + '%', 1, (40, 75, 25))
        text_x = WINDOW_WIDTH // 40
        text_y = WINDOW_HEIGHT * interval
        interval += distance
        screen.blit(text, (text_x, text_y))


all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
pins = pygame.sprite.Group()
heros = pygame.sprite.Group()
HLTH = 100
RSN = 100


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
        self.image.fill((40, 75, 25))


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
            next_y = max(next_y, int(WINDOW_HEIGHT - 200 * WINDOW_RATIO))


        if pygame.key.get_pressed()[pygame.K_DOWN]:
            next_y += SPEED
            next_y = min(next_y, WINDOW_HEIGHT - self.hero.height)

        if 0 < next_x < WINDOW_WIDTH - self.hero.width:
            self.hero.set_position((next_x, next_y))


class Pine(pygame.sprite.Sprite):
    def __init__(self, x, y, surf, group):
        super(Pine, self).__init__()
        self.image = surf
        self.rect = self.image.get_rect(center=(x, y))
        self.add(group)

        self.vx = 0
        self.vy = SPEED * 0.8

    def update(self):
        if pygame.sprite.spritecollideany(self, heros):
            global HLTH, RSN
            damage = 20 + (100 - RSN) / 20
            HLTH -= damage
            HLTH = max(HLTH, 0)
            self.kill()
        if self.rect.y < WINDOW_HEIGHT:
            self.rect.y += self.vy
        else:
            self.kill()


class Hero(pygame.sprite.Sprite):

    def __init__(self):
        super(Hero, self).__init__()
        self.add(heros)
        image = load_image("bear.png")
        self.image_bear = pygame.transform.scale(image, (125 * WINDOW_RATIO, 125 * WINDOW_RATIO))
        self.image_bear_right = self.image_bear
        self.image_bear_left = pygame.transform.flip(self.image_bear, 1, 0)
        self.x, self.y = WINDOW_WIDTH // 2, WINDOW_HEIGHT - self.image_bear.get_height() \
                         - self.image_bear.get_height() * 0.2
        c1 = 4 / 14 * self.image_bear.get_width()
        self.rect = self.help1()
        self.mask = pygame.mask.from_surface(self.image_bear)
        self.width = self.image_bear.get_width()
        self.height = self.image_bear.get_height()

    def help1(self):
        c1 = 4 / 14 * self.image_bear.get_width()
        return (self.x + c1, self.y, self.image_bear.get_width()
                - c1 * 2, self.image_bear.get_height() * 0.1)

    def get_position(self):
        return self.x, self.y

    def set_position(self, position):
        self.x, self.y = position
        c1 = 4 / 14 * self.image_bear.get_width()
        self.rect = self.help1()
        self.mask = pygame.mask.from_surface(self.image_bear)

    def render(self, screen, flag):
        if flag == 'left':
            self.image_bear = self.image_bear_left
        else:
            self.image_bear = self.image_bear_right
        screen.blit(self.image_bear, (self.x, self.y))


def show_game_over(screen, message, score):
    intro_text = ['Score: ' + score]

    fon = pygame.transform.scale(load_image('фон.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    # screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, int(100 * WINDOW_RATIO))
    text_coord = 300 * WINDOW_RATIO
    for line in intro_text:
        string_rendered = font.render(line, 1, (150, 0, 30))
        intro_rect = string_rendered.get_rect()
        text_w = string_rendered.get_width()
        text_h = string_rendered.get_height()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WINDOW_WIDTH // 2 - text_w // 2
        text_coord += intro_rect.height
        pygame.draw.rect(screen, (40, 50, 40),
                         (intro_rect[0] - 5, intro_rect[1] - 5, intro_rect[2] + 10, intro_rect[3] + 10), 5)
        screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(None, int(100 * WINDOW_RATIO))
    text = font.render(message, 1, (150, 0, 30))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT * 0.5 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (40, 50, 40), (text_x - 10, text_y - 10,
                                              text_w + 20, text_h + 20), 5)
    screen.blit(text, (text_x, text_y))


def show_game_victory(screen, message, score):
    intro_text = ['Score: ' + score]

    fon = pygame.transform.scale(load_image('фон.png'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    # screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, int(100 * WINDOW_RATIO))
    text_coord = 300 * WINDOW_RATIO
    for line in intro_text:
        string_rendered = font.render(line, 1, (0, 191, 255))
        intro_rect = string_rendered.get_rect()
        text_w = string_rendered.get_width()
        text_h = string_rendered.get_height()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = WINDOW_WIDTH // 2 - text_w // 2
        text_coord += intro_rect.height
        pygame.draw.rect(screen, (40, 50, 40),
                         (intro_rect[0] - 5, intro_rect[1] - 5, intro_rect[2] + 10, intro_rect[3] + 10), 5)
        screen.blit(string_rendered, intro_rect)

    font = pygame.font.Font(None, int(100 * WINDOW_RATIO))
    text = font.render(message, 1, (0, 191, 255))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT * 0.5 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (40, 50, 40), (text_x - 10, text_y - 10,
                                            text_w + 20, text_h + 20), 5)
    screen.blit(text, (text_x, text_y))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)


    speed_gen = 300
    pygame.time.set_timer(pygame.USEREVENT, speed_gen)

    score = 0

    start_screen(screen)

    Border(5, 5, WINDOW_WIDTH - 5, 5)
    Border(5, WINDOW_HEIGHT - 5, WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
    Border(5, 5, 5, WINDOW_HEIGHT - 5)
    Border(WINDOW_WIDTH - 5, 5, WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)

    image = load_image("фон.png")
    image_background = pygame.transform.scale(image, WINDOW_SIZE)
    image_pine = load_image("shishka2.png")
    image_pine = pygame.transform.scale(image_pine, (70 * WINDOW_RATIO, 70 * WINDOW_RATIO))
    image_pine = pygame.transform.flip(image_pine, 0, 1)
    image_pine_start = pygame.transform.rotate(image_pine, 90)
    image = load_image("bear.png")
    image_bear = pygame.transform.scale(image, (125 * WINDOW_RATIO, 125 * WINDOW_RATIO))
    x_start_bear = 100 * WINDOW_RATIO
    x_start_pine = 0

    hero = Hero()
    global HLTH, RSN
    flag = False
    game = Game(hero)
    Pine(random.randint(1, WINDOW_HEIGHT), random.randint(1, WINDOW_WIDTH // 2), image_pine, pins)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    HLTH = 100
                    RSN = 100
                    score = 0
                    for pine in pins:
                        pine.kill()
                    flag = True
                elif event.key == pygame.K_KP_ENTER:
                    HLTH = 100
                    RSN = 100
                    score = 0
                    for pine in pins:
                        pine.kill()
                    flag = True
            if event.type == pygame.USEREVENT and flag:
                score += 1
                Pine(random.randint(1, WINDOW_WIDTH), random.randint(1, WINDOW_HEIGHT // 2), image_pine, pins)
                if random.choice([0, 1, 0, 0]):
                    Pine(hero.get_position()[0] + hero.width // 2, random.randint(1, WINDOW_HEIGHT // 2), image_pine, pins)
                    RSN -= 1 * SPEED / 5
                    RSN = max(RSN, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flag = False
        if RSN == 0 or HLTH == 0:
            flag = False
        if flag:
            screen.fill(pygame.Color('black'))
            screen.blit(image_background, (0, 0))

            all_sprites.draw(screen)
            all_sprites.update()

            pins.draw(screen)
            pins.update()

            game.update_hero()
            game.render(screen)

            show_message(screen, str(score), flag, message2=str(HLTH), message3=str(RSN))
        else:
            if HLTH == 0:
                screen.blit(image_background, (0, 0))
                show_game_over(screen, 'Game Over', str(score))
            elif RSN == 0:
                show_game_victory(screen, 'Victory', str(score))
            else:
                start_screen(screen)
                show_message(screen, str(score), flag)
                x_start_bear, x_start_pine = render_start_screen(screen, x_start_bear, x_start_pine,
                                                                 image_bear, image_pine_start)

        pygame.display.flip()
        clock.tick(FPS)
if __name__ == '__main__':
    main()