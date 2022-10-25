import sys
from os import path

import pygame
from level import Level
from settings import FPS, HEIGHT, WIDTH


class Game:
    def __init__(self):
        pygame.init()
        icon_path = path.join('..', 'graphics', 'weapons', 'sword', 'full.png')
        pygame_icon = pygame.image.load(icon_path)
        pygame.display.set_icon(pygame_icon)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
