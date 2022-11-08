from os import path

import pygame
from entity import Entity
from settings import ENEMIES
from support import import_folder


class Enemy(Entity):
    def __init__(self, position, groups, enemy_type, obstacle_sprites, damage_player, trigger_death_particles):
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
        self.damage_player = damage_player
        self.invulnerable = False
        self.invulnerability_time = 0
        self.invulnerability_cooldown = 300
        self.trigger_death_particles = trigger_death_particles
        self.current_stats = ENEMIES[self.enemy_type].copy()

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

    def take_damage(self, player, attack_type):
        if not self.invulnerable:
            self.direction = self.get_player_direction(player)
            self.invulnerable = True
            self.invulnerability_time = pygame.time.get_ticks()
            if attack_type == 'weapon':
                self.current_stats['health'] -= player.get_full_weapon_damage()
            elif attack_type == 'spell':
                self.current_stats['health'] -= player.get_full_spell_damage()
            if self.current_stats['health'] <= 0:
                if self.rect is not None:
                    self.trigger_death_particles(
                        self.rect.center, self.enemy_type)
                self.kill()

    def hit_reaction(self):
        if self.invulnerable:
            self.direction *= -self.current_stats['resistance']
            if self.image is not None:
                self.image.set_alpha(self.flicker_alpha_value())
        elif self.image is not None:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking and current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False
        if self.invulnerable and current_time - self.invulnerability_time >= self.invulnerability_cooldown:
            self.invulnerable = False

    def update_status(self, player):
        distance = self.get_player_distance(player)
        if self.attacking and self.frame_index >= len(self.animations['attack']) - self.animation_speed:
            self.status = 'idle'
            self.direction = pygame.math.Vector2()
        elif distance <= self.current_stats['attack_radius']:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.status = 'attack'
            self.damage_player(
                self.current_stats['damage'], self.current_stats['attack_type'])
            self.direction = pygame.math.Vector2()
        elif distance <= self.current_stats['notice_radius']:
            self.status = 'move'
            self.direction = self.get_player_direction(player)
        else:
            self.status = 'idle'
            self.direction = pygame.math.Vector2()

    def update(self):
        self.cooldowns()
        self.hit_reaction()
        self.move()
        self.animate()

    def enemy_update(self, player):
        self.update_status(player)
