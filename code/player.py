import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, position, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load(
            '../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.obstacle_sprites = obstacle_sprites

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self):
        if self.rect is not None:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
            self.rect.move_ip(self.direction.x * self.speed, 0)
            self.collide('horizontal')
            self.rect.move_ip(0, self.direction.y * self.speed)
            self.collide('vertical')

    def collide(self, direction):
        if self.rect is not None:
            if direction == 'horizontal':
                for sprite in self.obstacle_sprites:
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.x > 0:  # moving right
                            self.rect.right = sprite.rect.left
                        elif self.direction.x < 0:  # moving left
                            self.rect.left = sprite.rect.right
            elif direction == 'vertical':
                for sprite in self.obstacle_sprites:
                    if sprite.rect.colliderect(self.rect):
                        if self.direction.y > 0:  # moving down
                            self.rect.bottom = sprite.rect.top
                        elif self.direction.y < 0:  # moving up
                            self.rect.top = sprite.rect.bottom

    def update(self):
        self.input()
        self.move()
