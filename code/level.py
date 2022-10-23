from random import choice

import pygame
from player import Player
from settings import TILESIZE
from support import import_csv_file, import_folder
from tile import Tile


class Level:
    def __init__(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_file('../map/map_FloorBlocks.csv'),
            'grass': import_csv_file('../map/map_Grass.csv'),
            'objects': import_csv_file('../map/map_Objects.csv')
        }
        graphics = {
            'grass': import_folder('../graphics/grass/'),
            'objects': import_folder('../graphics/objects/')
        }
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for column_index, column in enumerate(row):
                    if column != '-1':
                        x = column_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites], 'invisible')
                        elif style == 'grass':
                            grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites],
                                 'grass', grass_image)
                        elif style == 'objects':
                            object_image = graphics['objects'][int(column)]
                            Tile((x, y), [self.visible_sprites,
                                 self.obstacle_sprites], 'object', object_image)
        self.player = Player(
            (2000, 1430), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.floor_surface = pygame.image.load(
            '../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        offset = (player.rect.centerx - self.half_width,
                  player.rect.centery - self.half_height)
        floor_position = self.floor_rect.move(-offset[0], -offset[1])
        self.display_surface.blit(self.floor_surface, floor_position)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery if sprite.rect is not None else 0):
            if sprite.image is not None and sprite.rect is not None:
                offset_position = sprite.rect.move(-offset[0], -offset[1])
                self.display_surface.blit(sprite.image, offset_position)
