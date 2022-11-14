import sys
from os import path

import pygame
from level import Level
from settings import FPS, WATER_COLOR, WINDOW_HEIGHT, WINDOW_WIDTH


class Game:
    def __init__(self):
        pygame.init()
        icon_path = path.join('..', 'graphics', 'weapons', 'sword', 'full.png')
        pygame_icon = pygame.image.load(icon_path)
        pygame.display.set_icon(pygame_icon)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.background_sound = pygame.mixer.Sound('../audio/background.ogg')
        self.background_sound.set_volume(0.5)
        self.background_sound.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                        self.level.toggle_upgrade_menu()
            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
