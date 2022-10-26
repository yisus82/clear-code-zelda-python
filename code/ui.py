import pygame
from settings import (BAR_BORDER_WIDTH, BAR_HEIGHT, BAR_MARGIN,
                      HEALTH_BAR_WIDTH, HEALTH_COLOR, MANA_BAR_WIDTH,
                      MANA_COLOR, UI_BG_COLOR, UI_BORDER_COLOR, UI_FONT,
                      UI_FONT_SIZE)


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

    def draw(self):
        self.draw_bar(
            self.player.current_stats['health'], self.player.initial_stats['health'], HEALTH_COLOR, self.health_bg_rect)
        self.draw_bar(
            self.player.current_stats['mana'], self.player.initial_stats['mana'], MANA_COLOR, self.mana_bg_rect)
