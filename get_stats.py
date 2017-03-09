"""
game_stats module contains GameStats class which stores game statistics
"""

import pygame


class GameStats():
    """Track statistics for Alien Invasion"""

    def __init__(self, imput_ai_settings):
        """Initialize statistics"""
        self.ai_settings = imput_ai_settings
        self.reset_stats()

        # Start Alien Invasion in an active state
        self.game_active = False

        # High Score
        self.high_score = 0

    def reset_stats(self):
        """Reset statistics for new game."""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1