import pygame
from random import randint

WINDOW_SIZE = WINDOW_HIDTH, WINDOW_HEIGHT = 500, 500
FPS = 30
#pygame.time.set_timer(pygame.USEREVENT, 3000)
def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    screen.fill((10, 200, 50))
    screen2 = pygame.Surface(screen.get_size())
    x1, y1, w, h = 0, 0, 0, 0
    drawing = False
    running  = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                x1, y1 = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                screen2.blit(screen, (0, 0))
                drawing = False
                x1, y1, w, h = 0, 0, 0, 0
            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    w, h = event.pos[0] - x1, event.pos[1] - y1
        screen.fill((0, 0, 0))
        screen.blit(screen2, (0, 0))
        if drawing:
            if w > 0 and h > 0:
                pygame.draw.rect(screen
                                 , (0, 0, 255), (x1, y1, w, h), 5)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
