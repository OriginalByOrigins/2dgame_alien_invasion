"""
bullet module stores the bullet class
"""


import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(
            self, input_ai_settings,
            input_screen, input_ship):
        """Create a bullet object at the ship's position."""

        super().__init__()

        self.screen = input_screen

        # Create a bullet at (0, 0) then set correct position.
        self.rect = pygame.Rect(
            0, 0, input_ai_settings.bullet_width,
            input_ai_settings.bullet_height)
        self.rect.centerx = input_ship.rect.centerx
        self.rect.top = input_ship.rect.top

        # Store the bullet's y position as a decimal value.
        self.y = float(self.rect.y)

        # Store bullet's color and speed
        self.color = input_ai_settings.bullet_color
        self.speed_factor = input_ai_settings.bullet_speed_factor

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
        # Thy pygame.draw.rect is equivalent to
        #   self.screen.fill(self.color, self.rect)