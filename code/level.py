from os import path
from random import choice

import pygame
from enemy import Enemy
from player import Player
from settings import TILESIZE
from support import import_csv_file, import_folder
from tile import Tile
from ui import UI
from weapon import Weapon


class Level:
    def __init__(self):
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.current_attack = None
        self.current_spell = None
        self.entities = {
            '390': 'bamboo',
            '391': 'spirit',
            '392': 'raccoon',
            '393': 'squid',
            '394': 'player',
        }
        self.create_map()
        self.ui = UI(self.player)

    def create_map(self):
        layouts = {
            'boundary': import_csv_file('../map/map_FloorBlocks.csv'),
            'grass': import_csv_file('../map/map_Grass.csv'),
            'objects': import_csv_file('../map/map_Objects.csv'),
            'entities': import_csv_file('../map/map_Entities.csv'),
        }
        graphics = {
            'grass': import_folder('../graphics/grass/'),
            'objects': import_folder('../graphics/objects/'),
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
                        elif style == 'entities':
                            if column == '394':
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_spell,
                                    self.destroy_spell)
                            else:
                                Enemy(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.entities[column],
                                    self.obstacle_sprites)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack is not None:
            self.current_attack.kill()
            self.current_attack = None

    def create_spell(self):
        self.current_spell = self.player.spell['name']
        print('Casting', self.current_spell, '...')
        print(
            'strength:', self.player.spell['strength'] +
            self.player.current_stats['magic'], 'cost:', self.player.spell['cost'])

    def destroy_spell(self):
        if self.current_spell is not None:
            print(self.current_spell, 'casted!')
            self.current_spell = None

    def run(self):
        self.visible_sprites.update()
        self.visible_sprites.custom_draw(self.player)
        self.ui.draw()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        floor_path = path.join('..', 'graphics', 'tilemap', 'ground.png')
        self.floor_surface = pygame.image.load(floor_path).convert()
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
