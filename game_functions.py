"""
game_functions module contains a number of functions
    that makes Alien Invasion works.
"""


import sys
# sys module helps exit the game when players quit.

import pygame

from alien import Alien

from bullet import Bullet
# To create new bullet when the space key is pressed.

from time import sleep
# Freeze the screen when this ship is hit.


def open_high_score_file_read(ai_settings, stats):
    """Open file contains high score and return a file object"""
    try:
        file_read = open(ai_settings.high_score_file)
    except FileNotFoundError:
        pass
    else:
        stats.high_score = int(file_read.read())
        file_read.close()


def open_high_score_file_write(ai_settings, stats):
    """Open high score file and write new high score to it"""
    file_write = open(ai_settings.high_score_file, 'w')
    file_write.write(str(stats.high_score))
    file_write.close()


def check_events(
        ai_settings, screen, stats,play_button,
        scoreboard, ship, aliens, bullets):
    """Respond to keypresses and mouse events."""
    # Event loop.
    for event in pygame.event.get():
        # Watch for keyboard and mouse event.
        if event.type == pygame.QUIT:
            open_high_score_file_write(ai_settings, stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(
                event, ai_settings, screen, stats, play_button,
                scoreboard, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(
                ai_settings, screen, stats, play_button,
                scoreboard, ship, aliens, bullets, mouse_x, mouse_y)


def check_keydown_events(
        event, ai_settings, screen, stats, play_button,
        scoreboard, ship, aliens, bullets):
    """Respond to keypresses"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        open_high_score_file_write(ai_settings, stats)
        sys.exit()
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(
                ai_settings, screen, stats, play_button,
                scoreboard, ship, aliens, bullets)


def fire_bullets(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit not reached yet."""
    # Create a bullet then add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Repond to keyreleases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(
        ai_settings, screen, stats, play_button,
        scoreboard, ship, aliens, bullets, mouse_x, mouse_y):
    """Check if the mouse click the play button"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(
            ai_settings, screen, stats,play_button,
            scoreboard, ship, aliens, bullets)


def start_game(
        ai_settings, screen, stats, play_button,
        scoreboard, ship, aliens, bullets):
    """Start the game if player pressed p or clicked Play"""
    # Hide mouse cursor.
    pygame.mouse.set_visible(False)

    stats.reset_stats()
    stats.game_active = True
    ai_settings.initialize_dynamic_settings()

    scoreboard.prep_score()
    scoreboard.prep_high_score()
    scoreboard.prep_level()
    scoreboard.prep_ships()

    # Delete remaining bullets and aliens
    bullets.empty()
    aliens.empty()

    # Create a new alien fleet and center the ship
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def bullets_update(
        ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """
    Update position of bullets and delete old bullets
    If a fleet of alien has been destroy,
        delete all remaining bullets and create a new alien fleet
    """
    # Update bullets positions
    bullets.update()

    # Delete bullets that have been disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(
        ai_settings, screen, stats, scoreboard, ship, aliens, bullets)


def check_high_score(stats, scoreboard):
    """Check if a new high score is set"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()


def check_bullet_alien_collisions(
        ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """Respond to bullet-alien collision"""
    # Check for bullet-alien collision
    # If there are, delete the bullet and the alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for hit_aliens in collisions.values():
            stats.score += (ai_settings.alien_points*len(hit_aliens))
            scoreboard.prep_score()
            check_high_score(stats, scoreboard)

    if len(aliens) == 0:
        # Destroy existing bullets and create new alien fleet
        bullets.empty()
        # Display new level
        stats.level += 1
        scoreboard.prep_level()
        # Increase difficulty
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Return the number of aliens in one row"""
    available_space_x = ai_settings.screen_width - 2*alien_width
    return available_space_x // (2*alien_width)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Return the number of rows"""
    available_space_y = (ai_settings.screen_height
                        - 3*alien_height - ship_height)
    return available_space_y // (2*alien_height)


def create_alien(
        ai_settings, screen, aliens,alien_width,
        alien_height, row, alien_index):
    """Create an alien then add it to the fleet"""
    new_alien = Alien(ai_settings, screen)
    new_alien.x = alien_width + 2*alien_width*alien_index
    new_alien.rect.x = new_alien.x
    new_alien.rect.y = alien_height + 2*alien_height*row
    aliens.add(new_alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a fleet of alien ships at the top of the screen."""
    sample_alien = Alien(ai_settings, screen)
    alien_width = sample_alien.rect.width
    alien_height = sample_alien.rect.height

    # Compute the number of aliens in one fleet.
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)

    # Compute the number of rows.
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien_height)

    # Create alien then add it to the aliens group.
    for row in range(number_rows):
        for alien_index in range(number_aliens_x):
            create_alien(
                ai_settings, screen, aliens,
                alien_width, alien_height, row, alien_index)


def change_fleet_direction(ai_settings, aliens):
    """Drop the fleet and change their direction"""
    for alien in aliens:
        alien.rect.y += alien.ai_settings.fleet_drop_speed

    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    """"Respond if any alien reaches the edges."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def aliens_update(
    ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """ Check if fleet hits edges then update new positions of aliens"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for ship-alien update.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(
            ai_settings, screen, stats,
            scoreboard, ship, aliens, bullets)

    # Look for aliens hitting the bottom
    check_aliens_bottom(
        ai_settings, screen, stats, scoreboard, ship, aliens, bullets)


def check_aliens_bottom(
        ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """Check for aliens hitting the bottom of the screen"""
    screen_bottom = screen.get_rect().bottom

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_bottom:
            # Treat it like ship is being hit
            ship_hit(
                ai_settings, screen, stats,
                scoreboard, ship, aliens, bullets)
            break


def ship_hit(
        ai_settings, screen, stats, scoreboard, ship, aliens, bullets):
    """Respond when the ship is hit"""
    if stats.ship_left > 0:
        # Decrease ship_left
        stats.ship_left -= 1
        scoreboard.prep_ships()

        # Delete current bullets and alien
        bullets.empty()
        aliens.empty()

        # Recreate a new alien fleet
        create_fleet(ai_settings, screen, ship, aliens)

        # Recenter the ship
        ship.center_ship()

        # Pause
        sleep(0.5)
    else:
        stats.game_active = False
        #Set mouse cursor visible to click Play
        pygame.mouse.set_visible(True)


def update_screen(
        ai_settings, screen, stats, play_button,
        scoreboard, ship, aliens, bullets):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    # The screen.fill() is equivalent to
    #  pygame.draw.rect(screen, ai_settings.bg_color, screen.get_rect())

    # Redraw bullets behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # Redraw the ship during each pass through the loop 
    ship.blitme()

    # Draw all aliens.
    aliens.draw(screen)

    # Draw Score Board
    scoreboard.draw_score()

    # Draw the play button when game is not active
    if not stats.game_active:
        play_button.draw_button()


    # Make the most rexently drawn creen visible.
    pygame.display.flip()