from os import path

import pygame
from entity import Entity
from settings import SPELLS, WEAPONS
from support import import_folder


class Player(Entity):
    def __init__(self, position, groups, obstacle_sprites, create_attack, destroy_attack,
                 create_spell, destroy_spell):
        super().__init__(position, groups, obstacle_sprites)
        self.sprite_type = 'player'
        self.import_animations()
        self.status = 'down_idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-1, -25)
        self.attacking = False
        self.attack_time = 0
        self.attack_cooldown = 400
        self.weapon_index = 0
        self.weapon = WEAPONS[[*WEAPONS][self.weapon_index]]
        self.switching_weapon = False
        self.weapon_switch_time = 0
        self.weapon_switch_cooldown = 200
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.casting = False
        self.casting_time = 0
        self.casting_cooldown = 400
        self.spell_index = 0
        self.spell = SPELLS[[*SPELLS][self.spell_index]]
        self.switching_spell = False
        self.spell_switch_time = 0
        self.spell_switch_cooldown = 200
        self.create_spell = create_spell
        self.destroy_spell = destroy_spell
        self.invulnerable = False
        self.invulnerability_time = 0
        self.invulnerability_cooldown = 500
        self.base_stats = {
            'health': 100.0,
            'mana': 60.0,
            'attack': 10.0,
            'magic': 5.0,
            'speed': 5.0,
            'exp': 500,
        }
        self.current_stats = {
            'health': self.base_stats['health'],
            'mana': self.base_stats['mana'],
            'attack': self.base_stats['attack'],
            'magic': self.base_stats['magic'],
            'speed': self.base_stats['speed'],
            'exp': self.base_stats['exp'],
        }
        self.max_stats = {
            'health': 300,
            'mana': 140,
            'attack': 20,
            'magic': 10,
            'speed': 10,
            'exp': 99999,
        }
        self.upgrades = {
            'health': {
                'cost': 500.0,
                'amount': 10.0,
                'next': 50.0,
            },
            'mana': {
                'cost': 500.0,
                'amount': 10.0,
                'next': 50.0,
            },
            'attack': {
                'cost': 500.0,
                'amount': 1.0,
                'next': 50.0,
            },
            'magic': {
                'cost': 500.0,
                'amount': 1.0,
                'next': 50.0,
            },
            'speed': {
                'cost': 500.0,
                'amount': 1.0,
                'next': 50.0,
            },
        }

    def import_animations(self):
        player_folder = path.join('..', 'graphics', 'player')
        self.animations = {
            'up': [],
            'up_idle': [],
            'up_attack': [],
            'down': [],
            'down_idle': [],
            'down_attack': [],
            'left': [],
            'left_idle': [],
            'left_attack': [],
            'right': [],
            'right_idle': [],
            'right_attack': [],
        }
        for animation_name in self.animations.keys():
            animation_folder = path.join(player_folder, animation_name)
            self.animations[animation_name] = import_folder(animation_folder)

    def input(self):
        if not self.attacking and not self.casting:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
            else:
                self.direction.y = 0
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
            else:
                self.direction.x = 0
            if keys[pygame.K_SPACE] or keys[pygame.K_j]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0
                self.create_attack()
            elif keys[pygame.K_LCTRL] or keys[pygame.K_k]:
                self.casting = True
                self.casting_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0
                self.create_spell()
            elif not self.switching_weapon and (keys[pygame.K_LALT] or keys[pygame.K_u]):
                self.switching_weapon = True
                self.weapon_switch_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0
                self.change_weapon()
            elif not self.switching_spell and (keys[pygame.K_LSHIFT] or keys[pygame.K_i]):
                self.switching_spell = True
                self.spell_switch_time = pygame.time.get_ticks()
                self.direction.x = 0
                self.direction.y = 0
                self.change_spell()

    def change_weapon(self):
        self.weapon_index = (self.weapon_index + 1) % len(WEAPONS)
        self.weapon = WEAPONS[[*WEAPONS][self.weapon_index]]

    def change_spell(self):
        self.spell_index = (self.spell_index + 1) % len(SPELLS)
        self.spell = SPELLS[[*SPELLS][self.spell_index]]

    def get_full_weapon_damage(self):
        return self.weapon['damage'] + self.current_stats['attack']

    def get_full_spell_damage(self):
        return self.spell['strength'] + self.current_stats['magic']

    def take_damage(self, amount):
        if not self.invulnerable:
            self.invulnerable = True
            self.invulnerability_time = pygame.time.get_ticks()
            self.current_stats['health'] -= amount
            if self.current_stats['health'] <= 0:
                self.kill()

    def hit_reaction(self):
        if self.invulnerable:
            if self.image is not None:
                self.image.set_alpha(self.flicker_alpha_value())
        elif self.image is not None:
            self.image.set_alpha(255)

    def recover_mana(self):
        if self.current_stats['mana'] < self.base_stats['mana']:
            self.current_stats['mana'] += 0.01 * self.current_stats['magic']
        else:
            self.current_stats['mana'] = self.base_stats['mana']

    def receive_exp(self, amount):
        self.current_stats['exp'] += amount
        if self.current_stats['exp'] > self.max_stats['exp']:
            self.current_stats['exp'] = self.max_stats['exp']

    def upgrade_stats(self, name):
        if int(self.upgrades[name]['cost']) <= self.current_stats['exp'] and self.base_stats[name] < self.max_stats[name]:
            self.current_stats['exp'] -= self.upgrades[name]['cost']
            self.base_stats[name] += self.upgrades[name]['amount']
            self.current_stats[name] = self.base_stats[name]
            self.upgrades[name]['cost'] += self.upgrades[name]['next']
            if self.base_stats[name] > self.max_stats[name]:
                self.base_stats[name] = self.max_stats[name]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.attacking and current_time - self.attack_time >= self.attack_cooldown + self.weapon['cooldown']:
            self.attacking = False
            self.destroy_attack()
        if self.casting and current_time - self.casting_time >= self.casting_cooldown:
            self.casting = False
            self.destroy_spell()
        if self.switching_weapon and current_time - self.weapon_switch_time >= self.weapon_switch_cooldown:
            self.switching_weapon = False
        if self.switching_spell and current_time - self.spell_switch_time >= self.spell_switch_cooldown:
            self.switching_spell = False
        if self.invulnerable and current_time - self.invulnerability_time >= self.invulnerability_cooldown:
            self.invulnerable = False

    def update_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = self.status.split('_')[0] + '_idle'
        elif self.direction.x == 1 and self.direction.y == 0:
            self.status = 'right'
        elif self.direction.x == -1 and self.direction.y == 0:
            self.status = 'left'
        elif self.direction.y > 0:
            self.status = 'down'
        elif self.direction.y < 0:
            self.status = 'up'
        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def update(self):
        self.recover_mana()
        self.cooldowns()
        self.hit_reaction()
        self.input()
        self.update_status()
        self.move()
        self.animate()
