"""
ship module contains Ship class, this class will manage
    most of behavior of player's ship
"""


import pygame

from pygame.sprite import Sprite
# For displaying ship_left, we display group of ship


class Ship(Sprite):

    def __init__(self, input_ai_settings, input_screen):
        """ Initialize the ship and set its starting position."""
        super().__init__()

        self.screen = input_screen
        self.ai_settings = input_ai_settings

        # Load the ship image and get it rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        # Access the surface(image object)'s rect attributes
        self.screen_rect = input_screen.get_rect()
        # Store the screen object's rect

        # Set starting position at the center-bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value of ship's center
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """Recenter the ship when it is hit"""
        self.center = self.screen_rect.centerx

    def update(self):
        """ Update the ship's position based on the movement flag."""
        # Update the ship's center value, not the rect.
        if (self.moving_right and
            self.rect.right < self.screen_rect.right):
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update the rect's center
        self.rect.centerx = self.center


    def blitme(self):
        """ Draw the ship at this current location."""
        self.screen.blit(self.image, self.rect)