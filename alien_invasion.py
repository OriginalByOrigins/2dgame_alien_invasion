"""
This module helps create a pygame window.
"""

import pygame
# pygame module contains the functionality to make the game.

from settings import Settings
# Settings class stores all settings for our game.

from ship import Ship

from get_stats import GameStats

import game_functions as gf

from pygame.sprite import Group
# Manage a group of bullets.

from button import Button

from scoreboard import ScoreBoard


def run_game():
    """ Initialize pygame, settings and screen objects."""

    pygame.init()
    # Initialize the background setting that Pygame needs.

    ai_settings = Settings()
    # Create an instance of Settings.
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    # Create a display window called screen(screen object is a surface).
    # Argument (1200, 800) is a tuple defining the dimensions
    #   of the game window.
    pygame.display.set_caption('Alien Invasion')

    # Make a play button
    play_button = Button(ai_settings, screen, 'Play')

    # Make a ship.
    ship = Ship(ai_settings, screen)

    # Create a group to store a fleet of alien ships.
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Create a group to store bullets in.
    bullets = Group()

    # Create an instance of GameStats to store game statistics
    stats = GameStats(ai_settings)

    # Load high score to stats
    gf.open_high_score_file_read(ai_settings, stats)

    # Score object
    scoreboard = ScoreBoard(ai_settings, screen, stats)

    # Start the main loop for the game.
    while True:
        # Check for events.
        gf.check_events(
            ai_settings, screen, stats, play_button,
            scoreboard, ship, aliens, bullets)

        if stats.game_active:
            # Update ship's movement.
            ship.update()
            
            # Update bullets.
            # If a fleet of alien has been destroy,
            #  delete all remaining bullets and create a new alien fleet
            gf.bullets_update(
                ai_settings, screen, stats,
                scoreboard, ship, aliens, bullets)

            # Update aliens and look for ship-alien collision.
            gf.aliens_update(
                ai_settings, screen, stats,
                scoreboard, ship, aliens, bullets)

        # Update the screen.
        gf.update_screen(
            ai_settings, screen, stats, play_button,
            scoreboard, ship, aliens, bullets)


# Initialize the game and start the game loop.
run_game()
