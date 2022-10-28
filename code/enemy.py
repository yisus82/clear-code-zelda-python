from os import path

from entity import Entity
from support import import_folder


class Enemy(Entity):
    def __init__(self, position, groups, enemy_type, obstacle_sprites):
        super().__init__(position, groups, obstacle_sprites)
        self.enemy_type = enemy_type
        self.sprite_type = 'enemy'
        self.import_enemy_assets()
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-1, -25)

    def import_enemy_assets(self):
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

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        self.image = animation[int(self.frame_index % len(animation))]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.animate()
        self.move()
