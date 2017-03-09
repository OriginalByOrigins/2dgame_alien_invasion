"""
alien module contains Alien class
"""


import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """Create an alien ship at the top of the screen"""

    def __init__(
            self, input_ai_settings, input_screen):
        """Initialize an alien ship"""

        super().__init__()

        self.ai_settings = input_ai_settings
        self.screen = input_screen

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = input_screen.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of the screen"""
        if self.rect.right >= self.screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Update new posotion of aliens"""

        self.x += (self.ai_settings.alien_speed_factor
                  * self.ai_settings.fleet_direction)

        self.rect.x = self.x


    def blitme(self):
        """Draw the alien ship to the screen"""
        self.screen.blit(self.image, self.rect)