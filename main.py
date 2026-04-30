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
from code.campaign import CampaignMode
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

from code.campaign import CampaignMode

# Ajout des nouveaux états pour la campagne
STATE_LEVEL_WON = 3
STATE_CAMPAIGN_COMPLETE = 4

def can_switch_on_surface(player, floor_y, ceiling_y, tolerance=SWITCH_SURFACE_TOLERANCE):
    """Retourne True si le joueur est considere en contact avec une surface.

    Le switch de gravite n'est autorise que si le joueur est colle au sol
    (ou au plafond), avec une tolerance pour absorber les micro-ecarts de frame.
    """
    on_floor = floor_y is not None and abs(player.playerPosition.y - (floor_y - player.height)) <= tolerance
    on_ceiling = ceiling_y is not None and abs(player.playerPosition.y - ceiling_y) <= tolerance
    return on_floor or on_ceiling


def build_players(mode, screen_height):
    """Construit la liste des joueurs actifs selon le mode selectionne."""
    spawn_y = screen_height - 50 - 165 - 55
    players = [Player(PLAYER_RESPAWN_X, spawn_y)]
    lobby.name = players[0].nom
    if mode == "duo":
        players.append(Player(PLAYER_RESPAWN_X + 80, spawn_y))
    return players


def reset_players(game, players):
    """Repositionne tous les joueurs au lancement d'une nouvelle run."""
    spawn_y = game.world.floor_y - players[0].height
    for index, player in enumerate(players):
        spawn_x = PLAYER_RESPAWN_X + (index * (player.width + 25))
        player.spawn(spawn_x, spawn_y)
        player.alive = True
        player.gravity_direction = 1
        player.gravity_speed = PLAYER_GRAVITY_SPEED
        player.is_flipping = False


def start_new_run(game, players, obstacle_generator, visual_effects, now_ms):
    """Reinitialise une partie complete et renvoie les timers de depart.

    Valeurs retour:
    - run_start_time_ms,
    - last_spawn_ms,
    - prochain intervalle de spawn.
    """
    # Remet a zero tous les etats qui doivent repartir pour une nouvelle partie.
    game.start()
    game.world.reset_structures()
    reset_players(game, players)
    obstacle_generator.obstacles.clear()
    visual_effects.clear()
    spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)
    return now_ms, now_ms, spawn_interval


pygame.init()
WINDOWED_DEFAULT_SIZE = (1000, 700)
windowed_size = WINDOWED_DEFAULT_SIZE
is_fullscreen = False
try:
    screen = pygame.display.set_mode(WINDOWED_DEFAULT_SIZE, pygame.RESIZABLE, vsync=1)
except TypeError:
    screen = pygame.display.set_mode(WINDOWED_DEFAULT_SIZE, pygame.RESIZABLE)
clock = pygame.time.Clock()

game = Game(screen)
lobby = Lobby(screen, game)
interface = Interface(screen)
visual_fx = VisualEffects()
campaign = CampaignMode()

# Joueurs actifs: un seul en solo, deux en duo.
players = build_players(lobby.selected_mode, screen.get_height())
# Systeme de generation et de gestion des obstacles en flux continu.
ob_gen = ObstacleGenerator(screen.get_width(), screen.get_height())
last_spawn = pygame.time.get_ticks()
spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)
paused = False
run_start_time = pygame.time.get_ticks()
death_time_ms = None
game_state = STATE_MENU
switch_request_until = [0 for _ in players]


def apply_screen_resize(new_screen):
    """Synchronise les composants dependants de la taille d'ecran."""
    global screen
    screen = new_screen
    game.set_screen(screen)
    interface.set_screen(screen)
    ob_gen.set_screen_size(screen.get_width(), screen.get_height())

    # Recale les joueurs dans la nouvelle fenetre sans casser la run.
    for player in players:
        max_x = max(0, screen.get_width() - player.width)
        max_y = max(0, screen.get_height() - player.height)
        player.playerPosition.x = max(0, min(player.playerPosition.x, max_x))
        player.playerPosition.y = max(0, min(player.playerPosition.y, max_y))
        player.update_rect()


def toggle_fullscreen():
    """Bascule entre mode fenetre redimensionnable et plein ecran."""
    global is_fullscreen, windowed_size
    if is_fullscreen:
        try:
            new_screen = pygame.display.set_mode(windowed_size, pygame.RESIZABLE, vsync=1)
        except TypeError:
            new_screen = pygame.display.set_mode(windowed_size, pygame.RESIZABLE)
        is_fullscreen = False
    else:
        windowed_size = (screen.get_width(), screen.get_height())
        try:
            new_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, vsync=1)
        except TypeError:
            new_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        is_fullscreen = True

    apply_screen_resize(new_screen)

running = True

while running:
    frame_ms = clock.tick(TARGET_FPS)
    target_frame_ms = 1000.0 / TARGET_FPS
    frame_scale = max(FRAME_SCALE_MIN, min(FRAME_SCALE_MAX, frame_ms / target_frame_ms))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            toggle_fullscreen()
        elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
            windowed_size = (max(640, event.w), max(360, event.h))
            try:
                resized = pygame.display.set_mode(windowed_size, pygame.RESIZABLE, vsync=1)
            except TypeError:
                resized = pygame.display.set_mode(windowed_size, pygame.RESIZABLE)
            apply_screen_resize(resized)

    screen.fill((0, 0, 0))

    if game_state == STATE_MENU:
        lobby.run(screen, events)
        if not lobby.inMenu:
            players = build_players(lobby.selected_mode, screen.get_height())
            switch_request_until = [0 for _ in players]
            now = pygame.time.get_ticks()
            run_start_time, last_spawn, spawn_interval = start_new_run(game, players, ob_gen, visual_fx, now)
            paused = False
            death_time_ms = None
            game_state = STATE_PLAYING
    else:
        now = pygame.time.get_ticks()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if game_state == STATE_GAME_OVER:
                    if event.key == pygame.K_r:
                        run_start_time, last_spawn, spawn_interval = start_new_run(game, players, ob_gen, visual_fx, now)
                        lobby.inMenu = False
                        death_time_ms = None
                        paused = False
                        game_state = STATE_PLAYING
                    elif event.key in (pygame.K_ESCAPE, pygame.K_m):
                        lobby.inMenu = True
                        game_state = STATE_MENU
                elif game_state == STATE_LEVEL_WON:
                    if event.key == pygame.K_RETURN:
                        if campaign.advance_level():
                            run_start_time, last_spawn, spawn_interval = start_new_run(game, players, ob_gen, visual_fx, now)
                            game_state = STATE_PLAYING
                        else:
                            game_state = STATE_CAMPAIGN_COMPLETE
            
                elif game_state == STATE_CAMPAIGN_COMPLETE:
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_m):
                        lobby.inMenu = True
                        game_state = STATE_MENU
                else:
                    if event.key == pygame.K_ESCAPE:
                        lobby.inMenu = True
                        game_state = STATE_MENU
                    elif event.key == pygame.K_p:
                        paused = not paused
                    elif not paused:
                        if len(players) == 1:
                            if event.key in (pygame.K_SPACE, pygame.K_UP):
                                switch_request_until[0] = now + SWITCH_INPUT_BUFFER_MS
                        else:
                            if event.key == pygame.K_SPACE:
                                switch_request_until[0] = now + SWITCH_INPUT_BUFFER_MS
                            elif event.key == pygame.K_UP:
                                switch_request_until[1] = now + SWITCH_INPUT_BUFFER_MS
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_state == STATE_PLAYING and not paused and players:
                if len(players) == 1:
                    switch_request_until[0] = now + SWITCH_INPUT_BUFFER_MS
                else:
                    switch_request_until[1] = now + SWITCH_INPUT_BUFFER_MS

        game.world.drawBackGround(screen)
        game.world.drawWalls(screen)

        living_players = [player for player in players if player.alive]
        if game_state == STATE_PLAYING and not paused and living_players:
            elapsed_s = (now - run_start_time) / 1000.0
            ramp_ratio = min(1.0, elapsed_s / max(0.001, GAME_SPEED_RAMP_DURATION_SEC))
            speed_curve = ramp_ratio ** GAME_SPEED_RAMP_EXPONENT

            if lobby.selected_mode == "campaign":
                sp_start = campaign.current_level.speed_start
                sp_max = campaign.current_level.speed_max
            else:
                sp_start = GAME_SPEED_START
                sp_max = GAME_SPEED_MAX

            sp_start + ((sp_max - sp_start) * speed_curve)

            gravity_ratio = min(1.0, elapsed_s / max(0.001, PLAYER_GRAVITY_RAMP_DURATION_SEC))
            gravity_curve = gravity_ratio ** PLAYER_GRAVITY_RAMP_EXPONENT
            gravity_speed = PLAYER_GRAVITY_SPEED + ((PLAYER_GRAVITY_MAX - PLAYER_GRAVITY_SPEED) * gravity_curve)
            for player in living_players:
                player.gravity_speed = gravity_speed

            game.world.update_structures(
                game.gameSpeed * frame_scale,
                min(1.0, (game.gameSpeed - GAME_SPEED_START) / max(0.001, (GAME_SPEED_MAX - GAME_SPEED_START))),
            )

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

            elapsed_s = (now - run_start_time) / 1000.0
            speed_bonus = max(0.0, game.gameSpeed - GAME_SPEED_START) * SCORE_SPEED_BONUS_FACTOR
            game.score = int((elapsed_s * SCORE_BASE_PER_SEC) + (elapsed_s * speed_bonus))

            ob_gen.update(game.gameSpeed * frame_scale)

            for index, player in enumerate(players):
                if not player.alive:
                    continue

                support_span = min(player.width * SWITCH_SUPPORT_SPAN_RATIO, SWITCH_SUPPORT_SPAN_MAX)
                floor_y = game.world.find_floor_y(player.rect.centerx, support_span, player.rect.top)
                ceiling_y = game.world.find_ceiling_y(player.rect.centerx, support_span, player.rect.bottom)

                if switch_request_until[index] >= now and can_switch_on_surface(player, floor_y, ceiling_y):
                    player.switchGravity()
                    switch_request_until[index] = 0
                elif switch_request_until[index] < now:
                    switch_request_until[index] = 0

                player.mov(floor_y=floor_y, ceiling_y=ceiling_y, time_scale=frame_scale)

                if (
                    player.rect.top > screen.get_height() + PLAYER_OUT_OF_BOUNDS_MARGIN
                    or player.rect.bottom < -PLAYER_OUT_OF_BOUNDS_MARGIN
                ):
                    player.alive = False

                for ob in ob_gen.list_obstacles()[:]:
                    if player.rect.colliderect(ob.rect):
                        visual_fx.spawn_for_obstacle(ob.type, ob.rect.center)
                        ob.apply_effect(player)
                        try:
                            ob_gen.obstacles.remove(ob)
                        except ValueError:
                            pass

            if not any(player.alive for player in players):
                game.end()
                paused = False
                ob_gen.obstacles.clear()
                if death_time_ms is None:
                    death_time_ms = now
                game_state = STATE_GAME_OVER

            elif lobby.selected_mode == "campaign":
                if game.score >= campaign.current_level.target_score:
                    campaign.add_level_score(game.score)
                    last_level_score = game.score
                    paused = False
                    ob_gen.obstacles.clear()
                    game_state = STATE_LEVEL_WON

        ob_gen.draw(screen)
        visual_fx.update_and_draw(screen)
        for player in players:
            player.draw(screen)

        interface.show_score(game.score, game.bestScore)#jai aussi modifier ca 

        if game_state == STATE_PLAYING and paused:
            interface.show_pause()

        if game_state == STATE_GAME_OVER:
            if death_time_ms is None:
                death_time_ms = now

            dead_elapsed = now - death_time_ms
            if dead_elapsed >= GAME_OVER_DELAY_MS:
                interface.show_game_over()

            if GAME_OVER_RETURN_LOBBY_MS is not None and dead_elapsed >= GAME_OVER_RETURN_LOBBY_MS:
                lobby.inMenu = True
                game_state = STATE_MENU

    pygame.display.flip()

pygame.quit()