import sys

import pygame
from settings import *


class Game:
    def __init__(self):
        pygame.init()
        pygame_icon = pygame.image.load('../graphics/weapons/sword/full.png')
        pygame.display.set_icon(pygame_icon)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()