"""
Each time we introduce new functionalities to our game,
    we introduce some new settings as well
settings module contains a class called Settings to
    store all settings in one place, which allows us to
    pass around one setting object not many individual settings 
"""


class Settings():
    """A class stores all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game settings."""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings.
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # Alien settings
        self.fleet_drop_speed = 10
        
        # How fast to increase the speed of the game
        self.speedup_scale = 1.2

        # How fast to increase the score received
        self.score_scale = 1.5

        # File store high_score
        self.high_score_file = 'high_score.txt'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Set default speed of ship, aliens and bullets"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        #   fleet_direction of 1 : right, -1 : left
        self.fleet_direction = 1

        # Default point.
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed every leveling up."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        # Increase point received every leveling up."""
        self.alien_points = int(self.alien_points*self.score_scale)




