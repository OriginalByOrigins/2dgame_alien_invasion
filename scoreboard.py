"""
scoreboard contain ScoreBoard class,
    whiich has object to be drawn as a scoreboard
"""

import pygame

from ship import Ship
# To display group of ships as ship_left

from pygame.sprite import Group


class ScoreBoard():

    def __init__(self, input_ai_settings, input_screen, input_stats):
        """Initialize scoreboard's attribute"""
        self.ai_settings = input_ai_settings
        self.screen = input_screen
        self.screen_rect = input_screen.get_rect()
        self.stats = input_stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Prepare score as a image for drawing"""
        rounded_score = round(self.stats.score, -1)
        score_str = '{:,}'.format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.ai_settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20 

    def prep_high_score(self):
        """Prepare high score for drawing."""
        rounded_high_score = round(self.stats.high_score, -1)
        high_score_str = '{:,}'.format(rounded_high_score)
        self.high_score_image = self.font.render(
            high_score_str, True,
            self.text_color, self.ai_settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_level(self):
        """Prepare level for drawing"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.ai_settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Prepare group of ships for drawing"""
        self.ships = Group()
        for ship_index in range(self.stats.ship_left):
            drawn_ship = Ship(self.ai_settings, self.screen)
            drawn_ship.rect.x = 10 + drawn_ship.rect.width*ship_index
            drawn_ship.rect.y = 10
            self.ships.add(drawn_ship)

    def draw_score(self):
        """Draw the score"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)