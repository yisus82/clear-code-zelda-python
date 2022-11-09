from random import choice

import pygame
from support import import_folder


class AnimationPlayer():
    def __init__(self):
        self.animation_frames = {
            'aura': import_folder('../graphics/particles/spells/aura'),
            'flame': import_folder('../graphics/particles/spells/flame'),
            'heal': import_folder('../graphics/particles/spells/heal'),
            'claw': import_folder('../graphics/particles/attacks/claw'),
            'leaf': import_folder('../graphics/particles/attacks/leaf'),
            'slash': import_folder('../graphics/particles/attacks/slash'),
            'sparkle': import_folder('../graphics/particles/attacks/sparkle'),
            'thunder': import_folder('../graphics/particles/attacks/thunder'),
            'bamboo': import_folder('../graphics/particles/deaths/bamboo'),
            'raccoon': import_folder('../graphics/particles/deaths/raccoon'),
            'spirit': import_folder('../graphics/particles/deaths/spirit'),
            'squid': import_folder('../graphics/particles/deaths/squid'),
            'grass': [
                import_folder('../graphics/particles/grass/leaf1'),
                import_folder('../graphics/particles/grass/leaf2'),
                import_folder('../graphics/particles/grass/leaf3'),
                import_folder('../graphics/particles/grass/leaf4'),
                import_folder('../graphics/particles/grass/leaf5'),
                import_folder('../graphics/particles/grass/leaf6'),
                self.reflect_images(import_folder(
                    '../graphics/particles/grass/leaf1')),
                self.reflect_images(import_folder(
                    '../graphics/particles/grass/leaf2')),
                self.reflect_images(import_folder(
                    '../graphics/particles/grass/leaf3')),
                self.reflect_images(import_folder(
                    '../graphics/particles/grass/leaf4')),
                self.reflect_images(import_folder(
                    '../graphics/particles/grass/leaf5')),
                self.reflect_images(import_folder(
                    '../graphics/particles/grass/leaf6'))
            ],
        }

    def reflect_images(self, images):
        reflected_images = []
        for image in images:
            reflected_images.append(pygame.transform.flip(image, True, False))
        return reflected_images

    def create_particles(self, position, groups, particle_type, random=False):
        if random:
            particles = choice(self.animation_frames[particle_type])
        else:
            particles = self.animation_frames[particle_type]
        ParticleEffect(position, groups, particles)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, position, groups, animation_frames):
        super().__init__(groups)
        self.sprite_type = 'particle'
        self.animation_frames = animation_frames
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animation_frames[self.frame_index]
        self.rect = self.image.get_rect(center=position)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animation_frames):
            self.kill()
        else:
            self.image = self.animation_frames[int(self.frame_index)]

    def update(self):
        self.animate()
