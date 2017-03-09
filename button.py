"""
button module contains Button class,
    which helps us to display the play button.
"""


import pygame.font


class Button():

    def __init__(self, input_ai_settings, input_screen, msg):
        """Initialize a button that display msg."""
        self.ai_settings = input_ai_settings
        self.screen = input_screen
        self.screen_rect = input_screen.get_rect()

        # Set the dimension and properties of the button
        self.width = 200
        self.height = 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build a button's rect object and put it at the screen's center
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Preped mag
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Set the button to display the msg"""
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the button with msg to the screen"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)