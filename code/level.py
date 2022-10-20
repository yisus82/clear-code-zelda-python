import pygame
from player import Player
from settings import *
from tile import Tile


class Level:
    def __init__(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for column_index, column in enumerate(row):
                x = column_index * TILESIZE
                y = row_index * TILESIZE
                if column == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif column == 'p':
                    self.player = Player(
                        (x, y), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

    def custom_draw(self, player):
        offset = (player.rect.centerx - self.half_width,
                  player.rect.centery - self.half_height)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery if sprite.rect is not None else 0):
            if sprite.image is not None and sprite.rect is not None:
                offset_position = sprite.rect.move(-offset[0], -offset[1])
                self.display_surface.blit(sprite.image, offset_position)
