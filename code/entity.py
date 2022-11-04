from math import sin

import pygame
from settings import TILESIZE


class Entity(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = 'entity'
        self.status = 'idle'
        self.import_animations()
        self.frame_index = 0
        self.animation_speed = 0.15
        if self.status in self.animations:
            self.image = self.animations[self.status][self.frame_index]
        else:
            self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=position)
        if self.rect is not None:
            self.hitbox = self.rect.inflate(-1, -10)
        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2()
        self.current_stats = {
            'speed': 1,
        }

    def flicker_alpha_value(self):
        if sin(pygame.time.get_ticks()) > 0:
            return 255
        else:
            return 0

    def import_animations(self):
        self.animations = {}

    def animate(self):
        if self.status in self.animations:
            animation = self.animations[self.status]
            self.frame_index += self.animation_speed
            if self.frame_index >= len(animation):
                self.frame_index = 0
            self.image = animation[int(self.frame_index)]
            self.rect = self.image.get_rect(center=self.hitbox.center)

    def move(self):
        if self.rect is not None:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            self.hitbox.move_ip(self.direction.x *
                                self.current_stats['speed'], 0)
            self.collide('horizontal')
            self.hitbox.move_ip(0, self.direction.y *
                                self.current_stats['speed'])
            self.collide('vertical')
            self.rect.center = self.hitbox.center

    def collide(self, direction):
        if self.rect is not None:
            if direction == 'horizontal':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        elif self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
            elif direction == 'vertical':
                for sprite in self.obstacle_sprites:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        elif self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom
