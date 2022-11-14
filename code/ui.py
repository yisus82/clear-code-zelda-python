from os import path

import pygame
from settings import (BAR_BORDER_WIDTH, BAR_HEIGHT, BAR_MARGIN,
                      EXP_BORDER_WIDTH, EXP_MARGIN, EXP_PADDING,
                      GAME_OVER_BORDER_WIDTH, GAME_OVER_PADDING,
                      HEALTH_BAR_WIDTH, HEALTH_COLOR, ITEM_BOX_BORDER_WIDTH,
                      ITEM_BOX_MARGIN, ITEM_BOX_SIZE, MANA_BAR_WIDTH,
                      MANA_COLOR, TEXT_COLOR, UI_BG_COLOR, UI_BORDER_COLOR,
                      UI_BORDER_COLOR_ACTIVE, UI_FONT, UI_FONT_SIZE,
                      WINDOW_HEIGHT, WINDOW_WIDTH)


class UI:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.health_bg_rect = pygame.Rect(
            BAR_MARGIN, BAR_MARGIN, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.mana_bg_rect = pygame.Rect(
            BAR_MARGIN, 2 * BAR_MARGIN + BAR_HEIGHT, MANA_BAR_WIDTH, BAR_HEIGHT)
        self.player = player

    def draw_bar(self, current_amount, max_amount, color, bg_rect):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        current_width = int(current_amount / max_amount * bg_rect.width)
        current_rect = bg_rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         bg_rect, BAR_BORDER_WIDTH)

    def draw_exp(self, exp):
        text_surface = self.font.render(
            'EXP: ' + str(int(exp)), False, TEXT_COLOR)
        x = WINDOW_WIDTH - EXP_MARGIN
        y = WINDOW_HEIGHT - EXP_MARGIN
        text_rect = text_surface.get_rect(bottomright=(x, y))
        box_rect = text_rect.inflate(EXP_PADDING, EXP_PADDING)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, box_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         box_rect, EXP_BORDER_WIDTH)
        self.display_surface.blit(text_surface, text_rect)

    def draw_selection_box(self, x, y, active=False, image=None):
        box_rect = pygame.Rect(x, y, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, box_rect)
        if active:
            border_color = UI_BORDER_COLOR_ACTIVE
        else:
            border_color = UI_BORDER_COLOR
        pygame.draw.rect(self.display_surface, border_color,
                         box_rect, ITEM_BOX_BORDER_WIDTH)
        if image is not None:
            image_rect = image.get_rect(center=box_rect.center)
            self.display_surface.blit(image, image_rect)

    def draw_weapon_box(self):
        weapon_file = path.normpath(self.player.weapon['graphic'])
        weapon_image = pygame.image.load(weapon_file).convert_alpha()
        self.draw_selection_box(
            ITEM_BOX_MARGIN, WINDOW_HEIGHT - ITEM_BOX_MARGIN - ITEM_BOX_SIZE,
            self.player.switching_weapon, weapon_image)

    def draw_spell_box(self):
        spell_file = path.normpath(self.player.spell['graphic'])
        spell_image = pygame.image.load(spell_file).convert_alpha()
        self.draw_selection_box(
            2 * ITEM_BOX_MARGIN + ITEM_BOX_SIZE, WINDOW_HEIGHT -
            ITEM_BOX_MARGIN - ITEM_BOX_SIZE,
            self.player.switching_spell, spell_image)

    def draw_game_over_text(self):
        text_surface = self.font.render('GAME OVER', False, TEXT_COLOR)
        x = WINDOW_WIDTH / 2
        y = WINDOW_HEIGHT / 2
        text_rect = text_surface.get_rect(center=(x, y))
        box_rect = text_rect.inflate(GAME_OVER_PADDING, GAME_OVER_PADDING)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, box_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR,
                         box_rect, GAME_OVER_BORDER_WIDTH)
        self.display_surface.blit(text_surface, text_rect)

    def draw(self):
        self.draw_bar(
            self.player.current_stats['health'], self.player.base_stats['health'], HEALTH_COLOR,
            self.health_bg_rect)
        self.draw_bar(
            self.player.current_stats['mana'], self.player.base_stats['mana'], MANA_COLOR,
            self.mana_bg_rect)
        self.draw_exp(self.player.current_stats['exp'])
        self.draw_weapon_box()
        self.draw_spell_box()
        if not self.player.groups():
            self.draw_game_over_text()
