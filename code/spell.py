
import pygame
from settings import TILESIZE


class Spell():
    def __init__(self, player, groups, animation_player):
        self.player = player
        self.groups = groups
        self.animation_player = animation_player
        self.cast_spell()

    def cast_spell(self):
        spell = self.player.spell
        if spell['type'] == 'attack':
            self.player.current_stats['mana'] -= spell['cost']
            position = self.player.rect.center
            direction = self.player.status.split('_')[0]
            if direction == 'right':
                initial_offset = pygame.math.Vector2(1, 0)
            elif direction == 'left':
                initial_offset = pygame.math.Vector2(-1, 0)
            elif direction == 'down':
                initial_offset = pygame.math.Vector2(0, 1)
            elif direction == 'up':
                initial_offset = pygame.math.Vector2(0, -1)
            else:
                initial_offset = pygame.math.Vector2(0, 1)
            for i in range(int(self.player.current_stats['magic'])):
                offset = initial_offset * (i + 1) * TILESIZE
                self.animation_player.create_particles(
                    (position[0] + offset.x, position[1] + offset.y), self.groups, spell['name'].lower())
        else:
            if self.player.current_stats[spell['type']] < self.player.base_stats[spell['type']]:
                self.player.current_stats['mana'] -= spell['cost']
                self.player.current_stats[spell['type']] += spell['strength']
                if self.player.current_stats[spell['type']] > self.player.base_stats[spell['type']]:
                    self.player.current_stats[spell['type']
                                              ] = self.player.base_stats[spell['type']]
                position = self.player.rect.center
                offset = pygame.math.Vector2(0, -60)
                self.animation_player.create_particles(
                    position, self.groups, 'aura')
                self.animation_player.create_particles(
                    position + offset, self.groups, spell['name'].lower())
            else:
                return
