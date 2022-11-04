
import pygame


class Spell(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'spell'
