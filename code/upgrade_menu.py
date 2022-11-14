
import pygame
from settings import (BAR_COLOR, BAR_COLOR_SELECTED, BAR_VALUE_HEIGHT,
                      BAR_VALUE_WIDTH, BAR_WIDTH, ITEM_BOX_BORDER_WIDTH,
                      TEXT_COLOR, TEXT_COLOR_FORBIDDEN, TEXT_COLOR_SELECTED,
                      UI_BG_COLOR, UI_BORDER_COLOR, UI_BORDER_COLOR_ACTIVE,
                      UI_FONT, UI_FONT_SIZE, UPGRADE_BG_COLOR_SELECTED)


class UpgradeMenu:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.selected_index = 0
        self.selecting = False
        self.selection_time = 0
        self.selection_cooldown = 300
        self.create_items()

    def create_items(self):
        item_height = self.display_surface.get_height() * 0.8
        item_width = self.display_surface.get_width() // (len(self.player.upgrades) + 1)
        increment = self.display_surface.get_width() // len(self.player.upgrades)
        self.items = []
        for index, (name, upgrade) in enumerate(self.player.upgrades.items()):
            x = (index * increment) + (increment - item_width) // 2
            y = self.display_surface.get_height() * 0.1
            item = UpgradeMenuItem(x, y, item_width, item_height, name, upgrade['cost'],
                                   self.player.current_stats[name],
                                   self.player.max_stats[name],
                                   self.font, self.player)
            self.items.append(item)

    def input(self):
        if not self.selecting:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.selecting = True
                self.selection_time = pygame.time.get_ticks()
                self.selected_index += 1
                if self.selected_index >= len(self.player.upgrades):
                    self.selected_index = 0
            elif keys[pygame.K_LEFT]:
                self.selecting = True
                self.selection_time = pygame.time.get_ticks()
                self.selected_index -= 1
                if self.selected_index < 0:
                    self.selected_index = len(self.player.upgrades) - 1
            elif keys[pygame.K_SPACE]:
                self.selecting = True
                self.selection_time = pygame.time.get_ticks()
                if self.items[self.selected_index].confirm_upgrade():
                    self.create_items()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if self.selecting and current_time - self.selection_time >= self.selection_cooldown:
            self.selecting = False

    def draw(self):
        for index, item in enumerate(self.items):
            item.draw(index == self.selected_index)

    def update(self):
        self.cooldowns()
        self.input()
        self.draw()


class UpgradeMenuItem:
    def __init__(self, x, y, width, height, name, cost, current_value, max_value, font, player):
        self.display_surface = pygame.display.get_surface()
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.cost = cost
        self.current_value = current_value
        self.max_value = max_value
        self.font = font
        self.player = player

    def draw_texts(self, selected):
        if selected:
            text_color = TEXT_COLOR_SELECTED
        else:
            text_color = TEXT_COLOR
        name_surface = self.font.render(self.name, False, text_color)
        name_rect = name_surface.get_rect(
            midtop=(self.rect.midtop[0], self.rect.midtop[1] + 20))
        self.display_surface.blit(name_surface, name_rect)
        if int(self.cost) > self.player.current_stats['exp']:
            text_color = TEXT_COLOR_FORBIDDEN
        cost_surface = self.font.render(
            f'EXP: {int(self.cost)}', False, text_color)
        cost_rect = cost_surface.get_rect(
            midbottom=(self.rect.midbottom[0], self.rect.midbottom[1] - 20))
        self.display_surface.blit(cost_surface, cost_rect)

    def draw_bar(self, selected):
        top = (self.rect.midtop[0], self.rect.midtop[1] + 60)
        bottom = (self.rect.midbottom[0], self.rect.midbottom[1] - 60)
        if selected:
            bar_color = BAR_COLOR_SELECTED
        else:
            bar_color = BAR_COLOR
        full_height = bottom[1] - top[1]
        relative_height = self.current_value / self.max_value
        current_height = full_height * relative_height
        value_rect = pygame.Rect(
            top[0] - (BAR_VALUE_WIDTH / 2), bottom[1] - current_height, BAR_VALUE_WIDTH, BAR_VALUE_HEIGHT)
        pygame.draw.line(self.display_surface, bar_color,
                         top, bottom, BAR_WIDTH)
        pygame.draw.rect(self.display_surface, bar_color, value_rect)

    def confirm_upgrade(self):
        if int(self.player.upgrades[self.name]['cost']) <= self.player.current_stats['exp']:
            self.player.upgrade_stats(self.name)
            return True
        return False

    def draw(self, selected):
        if selected:
            background_color = UPGRADE_BG_COLOR_SELECTED
            border_color = UI_BORDER_COLOR_ACTIVE
        else:
            background_color = UI_BG_COLOR
            border_color = UI_BORDER_COLOR
        pygame.draw.rect(self.display_surface, background_color, self.rect)
        pygame.draw.rect(self.display_surface, border_color,
                         self.rect, ITEM_BOX_BORDER_WIDTH)
        self.draw_texts(selected)
        self.draw_bar(selected)
