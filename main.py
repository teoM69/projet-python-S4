"""Point d'entree du jeu.

Ce module orchestre:
- l'initialisation Pygame,
- la gestion des etats (menu, partie, game over),
- les mises a jour gameplay (vitesse, gravite, score),
- le rendu de tous les elements visuels.
"""

import pygame
import random
from code.game import Game
from code.lobby import Lobby
from code.Player import Player
from code.ObstacleGenerator import ObstacleGenerator
from code.VisualEffects import VisualEffects
from code.constants import (
    OBSTACLE_SPAWN_MIN_MS,
    OBSTACLE_SPAWN_MAX_MS,
    GAME_SPEED_START,
    GAME_SPEED_MAX,
    GAME_SPEED_RAMP_DURATION_SEC,
    GAME_SPEED_RAMP_EXPONENT,
    OBSTACLE_SPEED_MULT_MIN,
    OBSTACLE_SPEED_MULT_MAX,
    SCORE_BASE_PER_SEC,
    SCORE_SPEED_BONUS_FACTOR,
    PLAYER_GRAVITY_SPEED,
    PLAYER_GRAVITY_MAX,
    PLAYER_GRAVITY_RAMP_DURATION_SEC,
    PLAYER_GRAVITY_RAMP_EXPONENT,
    PLAYER_RESPAWN_X,
    PLAYER_OUT_OF_BOUNDS_MARGIN,
    SWITCH_SUPPORT_SPAN_RATIO,
    SWITCH_SUPPORT_SPAN_MAX,
    SWITCH_SURFACE_TOLERANCE,
    SWITCH_INPUT_BUFFER_MS,
    GAME_OVER_DELAY_MS,
    GAME_OVER_RETURN_LOBBY_MS,
    STATE_MENU,
    STATE_PLAYING,
    STATE_GAME_OVER,
    TARGET_FPS,
    FRAME_SCALE_MIN,
    FRAME_SCALE_MAX,
)
from code.interface import Interface


def can_switch_on_surface(player, floor_y, ceiling_y, tolerance=SWITCH_SURFACE_TOLERANCE):
    """Retourne True si le joueur est considere en contact avec une surface.

    Le switch de gravite n'est autorise que si le joueur est colle au sol
    (ou au plafond), avec une tolerance pour absorber les micro-ecarts de frame.
    """
    on_floor = floor_y is not None and abs(player.playerPosition.y - (floor_y - player.height)) <= tolerance
    on_ceiling = ceiling_y is not None and abs(player.playerPosition.y - ceiling_y) <= tolerance
    return on_floor or on_ceiling


def start_new_run(game, player, obstacle_generator, visual_effects, now_ms):
    """Reinitialise une partie complete et renvoie les timers de depart.

    Valeurs retour:
    - run_start_time_ms,
    - last_spawn_ms,
    - prochain intervalle de spawn.
    """
    # Remet a zero tous les etats qui doivent repartir pour une nouvelle partie.
    game.start()
    game.world.reset_structures()
    spawn_y = game.world.floor_y - player.height
    player.spawn(PLAYER_RESPAWN_X, spawn_y)
    player.alive = True
    player.gravity_direction = 1
    player.gravity_speed = PLAYER_GRAVITY_SPEED
    player.is_flipping = False
    obstacle_generator.obstacles.clear()
    visual_effects.clear()
    spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)
    return now_ms, now_ms, spawn_interval


pygame.init()
try:
    screen = pygame.display.set_mode((1000, 700), vsync=1)
except TypeError:
    screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()

game = Game(screen)
lobby = Lobby(screen, game)
interface = Interface(screen)
visual_fx = VisualEffects()

player = Player("player", 100, screen.get_height() - 50 - 165 - 55)
ob_gen = ObstacleGenerator(screen.get_width(), screen.get_height())
last_spawn = pygame.time.get_ticks()
spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)
paused = False
run_start_time = pygame.time.get_ticks()
death_time_ms = None
game_state = STATE_MENU
switch_request_until = 0

running = True

while running:
    # Delta temps normalise: permet de garder un comportement stable meme si le
    # framerate varie legerement selon la machine.
    frame_ms = clock.tick(TARGET_FPS)
    target_frame_ms = 1000.0 / TARGET_FPS
    frame_scale = max(FRAME_SCALE_MIN, min(FRAME_SCALE_MAX, frame_ms / target_frame_ms))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if game_state == STATE_MENU:
        # Le lobby gere l'entree utilisateur et decide quand demarrer une partie.
        lobby.inMenu = True
        lobby.run(screen, events)
        if not lobby.inMenu:
            now = pygame.time.get_ticks()
            run_start_time, last_spawn, spawn_interval = start_new_run(game, player, ob_gen, visual_fx, now)
            paused = False
            death_time_ms = None
            switch_request_until = 0
            game_state = STATE_PLAYING
    else:
        now = pygame.time.get_ticks()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if game_state == STATE_GAME_OVER:
                    # Pendant l'ecran de game over: R relance, ESC/M retourne au menu.
                    if event.key == pygame.K_r:
                        run_start_time, last_spawn, spawn_interval = start_new_run(game, player, ob_gen, visual_fx, now)
                        lobby.inMenu = False
                        death_time_ms = None
                        paused = False
                        game_state = STATE_PLAYING
                    elif event.key in (pygame.K_ESCAPE, pygame.K_m):
                        lobby.inMenu = True
                        game_state = STATE_MENU
                else:
                    # En jeu: ESC menu, P pause, SPACE/UP bufferise la demande de switch.
                    if event.key == pygame.K_ESCAPE:
                        lobby.inMenu = True
                        game_state = STATE_MENU
                    elif event.key == pygame.K_p:
                        paused = not paused
                    elif event.key in (pygame.K_SPACE, pygame.K_UP) and not paused:
                        switch_request_until = now + SWITCH_INPUT_BUFFER_MS

        game.world.drawBackGround(screen)
        game.world.drawWalls(screen)

        if game_state == STATE_PLAYING and not paused and player.alive:
            # Augmente progressivement la vitesse globale selon une courbe exponentielle.
            elapsed_s = (now - run_start_time) / 1000.0
            ramp_ratio = min(1.0, elapsed_s / max(0.001, GAME_SPEED_RAMP_DURATION_SEC))
            speed_curve = ramp_ratio ** GAME_SPEED_RAMP_EXPONENT
            game.gameSpeed = GAME_SPEED_START + ((GAME_SPEED_MAX - GAME_SPEED_START) * speed_curve)

            # Meme principe pour la gravite du joueur pour durcir la partie dans le temps.
            gravity_ratio = min(1.0, elapsed_s / max(0.001, PLAYER_GRAVITY_RAMP_DURATION_SEC))
            gravity_curve = gravity_ratio ** PLAYER_GRAVITY_RAMP_EXPONENT
            player.gravity_speed = PLAYER_GRAVITY_SPEED + ((PLAYER_GRAVITY_MAX - PLAYER_GRAVITY_SPEED) * gravity_curve)

            # Fait defiler les structures du monde en coherence avec la vitesse de jeu.
            game.world.update_structures(
                game.gameSpeed * frame_scale,
                min(1.0, (game.gameSpeed - GAME_SPEED_START) / max(0.001, (GAME_SPEED_MAX - GAME_SPEED_START))),
            )

        # Recherche des supports proches du joueur (sol/plafond) pour collisions et switch.
        support_span = min(player.width * SWITCH_SUPPORT_SPAN_RATIO, SWITCH_SUPPORT_SPAN_MAX)
        floor_y = game.world.find_floor_y(player.rect.centerx, support_span, player.rect.top)
        ceiling_y = game.world.find_ceiling_y(player.rect.centerx, support_span, player.rect.bottom)

        if game_state == STATE_PLAYING and not paused and player.alive:
            # Input buffer: la touche peut etre presse juste avant l'impact sur surface.
            if switch_request_until >= now and can_switch_on_surface(player, floor_y, ceiling_y):
                player.switchGravity()
                switch_request_until = 0
            elif switch_request_until < now:
                switch_request_until = 0

        if game_state == STATE_PLAYING and not paused and player.alive:
            # Spawn periodique avec intervalle aleatoire pour casser les patterns repetitifs.
            if now - last_spawn >= spawn_interval:
                speed = game.gameSpeed * random.uniform(OBSTACLE_SPEED_MULT_MIN, OBSTACLE_SPEED_MULT_MAX)
                spawned = ob_gen.generate_obstacle(
                    None,
                    speed,
                    top_lane_y=game.world.roof_y,
                    bottom_lane_y=game.world.floor_y,
                    middle_lane_y=game.world.get_middle_spawn_y(game.world.screen_width, 50),
                    world=game.world,
                )
                if spawned:
                    last_spawn = now
                    spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)

            # Le score combine duree de survie + bonus de vitesse.
            elapsed_s = (now - run_start_time) / 1000.0
            speed_bonus = max(0.0, game.gameSpeed - GAME_SPEED_START) * SCORE_SPEED_BONUS_FACTOR
            game.score = int((elapsed_s * SCORE_BASE_PER_SEC) + (elapsed_s * speed_bonus))

            # Mise a jour du gameplay: obstacles, joueur, puis verification des limites monde.
            ob_gen.update(game.gameSpeed * frame_scale)
            player.mov(floor_y=floor_y, ceiling_y=ceiling_y, time_scale=frame_scale)

            if (
                player.rect.top > screen.get_height() + PLAYER_OUT_OF_BOUNDS_MARGIN
                or player.rect.bottom < -PLAYER_OUT_OF_BOUNDS_MARGIN
            ):
                player.alive = False

            # Collision obstacle -> effet visuel + effet gameplay + suppression obstacle touche.
            for ob in ob_gen.list_obstacles()[:]:
                if player.rect.colliderect(ob.rect):
                    visual_fx.spawn_for_obstacle(ob.type, ob.rect.center)
                    ob.apply_effect(player)
                    try:
                        ob_gen.obstacles.remove(ob)
                    except ValueError:
                        pass

            if not player.alive:
                # Transition vers l'etat GAME_OVER: on fige la partie active.
                game.end()
                paused = False
                ob_gen.obstacles.clear()
                if death_time_ms is None:
                    death_time_ms = now
                game_state = STATE_GAME_OVER

        ob_gen.draw(screen)
        visual_fx.update_and_draw(screen)
        player.draw(screen)

        interface.show_score(game.score, game.bestScore)

        if game_state == STATE_PLAYING and paused:
            interface.show_pause()

        if game_state == STATE_GAME_OVER:
            if death_time_ms is None:
                death_time_ms = now

            # Affiche le texte GAME OVER apres un court delai pour laisser "respirer" l'impact.
            dead_elapsed = now - death_time_ms
            if dead_elapsed >= GAME_OVER_DELAY_MS:
                interface.show_game_over()

            # Option de retour automatique menu si ce delai est configure.
            if GAME_OVER_RETURN_LOBBY_MS is not None and dead_elapsed >= GAME_OVER_RETURN_LOBBY_MS:
                lobby.inMenu = True
                game_state = STATE_MENU

    pygame.display.flip()

pygame.quit()