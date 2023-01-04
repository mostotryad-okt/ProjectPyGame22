import pygame
from random import randint

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
FPS = 90

CARS = ('data/creature.png', 'data/car2.png', 'data/boom.png')
CARS_SURF = []
class Car(pygame.sprite.Sprite):
    def __init__(self, y, surf, group):
        super(Car, self).__init__()
        self.image = surf
        self.rect = self.image.get_rect(center=(0, y))
        self.add(group)
        self.speed = randint(1, 3)


    def update(self):
        if self.rect.x < WINDOW_WIDTH:
            self.rect.x += self.speed
        else:
            self.kill()


cars = pygame.sprite.Group()
def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.time.set_timer(pygame.USEREVENT, 3000)
    clock = pygame.time.Clock()
    for i in range(len(CARS)):
        CARS_SURF.append(pygame.image.load(CARS[i]).convert_alpha())
    Car(randint(1, WINDOW_HEIGHT), CARS_SURF[randint(0, 2)], cars)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                Car(randint(1, WINDOW_HEIGHT), CARS_SURF[randint(0, 2)], cars)

        clock.tick(FPS)
        screen.fill((0, 200, 123))
        cars.draw(screen)
        pygame.display.update()
        cars.update()

    pygame.quit()

if __name__ == '__main__':
    main()
