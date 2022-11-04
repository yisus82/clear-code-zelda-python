from os import path

import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]
        if direction not in ['up', 'down', 'left', 'right']:
            direction = 'full'
        weapon_file = path.normpath(
            player.weapon['graphic']).replace('full', direction)
        self.image = pygame.image.load(weapon_file).convert_alpha()
        if direction == 'right':
            image_offset = pygame.math.Vector2(0, 16)
            self.rect = self.image.get_rect(
                midleft=player.rect.midright + image_offset)
        elif direction == 'left':
            image_offset = pygame.math.Vector2(0, 16)
            self.rect = self.image.get_rect(
                midright=player.rect.midleft + image_offset)
        elif direction == 'down':
            image_offset = pygame.math.Vector2(-12, 0)
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom + image_offset)
        elif direction == 'up':
            image_offset = pygame.math.Vector2(-12, 0)
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop + image_offset)
        else:
            self.rect = self.image.get_rect(center=player.rect.center)
