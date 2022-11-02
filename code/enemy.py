from os import path

import pygame
from entity import Entity
from settings import ENEMIES
from support import import_folder


class Enemy(Entity):
    def __init__(self, position, groups, enemy_type, obstacle_sprites):
        self.enemy_type = enemy_type
        super().__init__(position, groups, obstacle_sprites)
        self.sprite_type = 'enemy'
        self.import_animations()
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-1, -10)
        self.attacking = False
        self.attack_time = 0
        self.attack_cooldown = 400
        self.current_stats = ENEMIES[self.enemy_type]

    def import_animations(self):
        enemy_folder = path.join('..', 'graphics', 'enemies')
        self.animations = {
            'attack': [],
            'idle': [],
            'move': [],
        }
        for animation_name in self.animations.keys():
            animation_folder = path.join(
                enemy_folder, self.enemy_type, animation_name)
            self.animations[animation_name] = import_folder(animation_folder)

    def get_player_distance(self, player):
        if self.rect is not None and player.rect is not None:
            enemy_vector = pygame.math.Vector2(self.rect.center)
            player_vector = pygame.math.Vector2(player.rect.center)
            distance = (player_vector - enemy_vector).magnitude()
            return distance
        else:
            return 0

    def get_player_direction(self, player):
        if self.rect is not None and player.rect is not None:
            enemy_vector = pygame.math.Vector2(self.rect.center)
            player_vector = pygame.math.Vector2(player.rect.center)
            distance = (player_vector - enemy_vector).magnitude()
            if distance > 0:
                direction = (player_vector - enemy_vector).normalize()
            else:
                direction = pygame.math.Vector2()
            return direction
        else:
            return pygame.math.Vector2()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False

    def update_status(self, player):
        distance = self.get_player_distance(player)
        if self.attacking and self.frame_index >= len(self.animations['attack']) - self.animation_speed:
            self.status = 'idle'
            self.direction = pygame.math.Vector2()
        elif distance <= self.current_stats['attack_radius']:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.status = 'attack'
            self.direction = pygame.math.Vector2()
        elif distance <= self.current_stats['notice_radius']:
            self.status = 'move'
            self.direction = self.get_player_direction(player)
        else:
            self.status = 'idle'
            self.direction = pygame.math.Vector2()

    def update(self):
        self.cooldowns()
        self.move()
        self.animate()

    def enemy_update(self, player):
        self.update_status(player)
