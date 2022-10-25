from csv import reader
from os import path, walk

import pygame


def import_csv_file(pathname):
    pathname = path.normpath(pathname)
    terrain_map = []
    with open(pathname, 'r') as level_map:
        layout = reader(level_map, delimiter=',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map


def import_folder(pathname):
    pathname = path.normpath(pathname)
    image_surfaces = []
    for _, _, filenames in walk(pathname):
        for filename in sorted(filenames):
            full_path = path.join(pathname, filename)
            try:
                image_surface = pygame.image.load(full_path).convert_alpha()
                image_surfaces.append(image_surface)
            except pygame.error:
                pass
    return image_surfaces
