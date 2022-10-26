import pygame
from settings import (BAR_BORDER_WIDTH, BAR_HEIGHT, BAR_MARGIN,
                      EXP_BORDER_WIDTH, EXP_MARGIN, EXP_PADDING,
                      HEALTH_BAR_WIDTH, HEALTH_COLOR, MANA_BAR_WIDTH,
                      MANA_COLOR, TEXT_COLOR, UI_BG_COLOR, UI_BORDER_COLOR,
                      UI_FONT, UI_FONT_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH)


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

    def draw(self):
        self.draw_bar(
            self.player.current_stats['health'], self.player.initial_stats['health'], HEALTH_COLOR, self.health_bg_rect)
        self.draw_bar(
            self.player.current_stats['mana'], self.player.initial_stats['mana'], MANA_COLOR, self.mana_bg_rect)
        self.draw_exp(self.player.current_stats['exp'])
