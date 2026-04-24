import pygame
import random
from code.game import Game
from code.lobby import Lobby
from code.Player import Player
from code.ObstacleGenerator import ObstacleGenerator
from code.VisualEffects import VisualEffects
from code.constants import OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS
from code.interface import Interface

GAME_OVER_DELAY_MS = 500
GAME_OVER_RETURN_LOBBY_MS = None


def can_switch_on_surface(player, floor_y, ceiling_y):
    on_floor = floor_y is not None and abs(player.playerPosition.y - (floor_y - player.height)) <= 2
    on_ceiling = ceiling_y is not None and abs(player.playerPosition.y - ceiling_y) <= 2
    return on_floor or on_ceiling


def start_new_run(game, player, obstacle_generator, visual_effects):
    # Remet a zero tous les etats qui doivent repartir pour une nouvelle partie.
    game.start()
    game.world.reset_structures()
    spawn_y = game.world.floor_y - player.height
    player.spawn(100, spawn_y)
    player.alive = True
    player.gravity_direction = 1
    player.gravity_speed = 5
    player.is_flipping = False
    obstacle_generator.obstacles.clear()
    visual_effects.clear()


pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()

game = Game(screen)
lobby = Lobby(screen)
interface = Interface(screen)
visual_fx = VisualEffects()

# Garde le joueur aligne sur la ligne de sol initiale avec la hauteur actuelle du sprite.
player = Player("player", 100, screen.get_height() - 50 - 165 - 55)
ob_gen = ObstacleGenerator(screen.get_width(), screen.get_height())
last_spawn = pygame.time.get_ticks()
spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)
paused = False
run_start_time = pygame.time.get_ticks()
was_in_menu = lobby.inMenu
pending_new_run = False
death_time_ms = None

running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if lobby.inMenu:
        lobby.run(screen, events)
        if not lobby.inMenu:
            pending_new_run = True
    else:
        if was_in_menu or pending_new_run:
            start_new_run(game, player, ob_gen, visual_fx)
            paused = False
            last_spawn = pygame.time.get_ticks()
            spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)
            run_start_time = pygame.time.get_ticks()
            pending_new_run = False
            death_time_ms = None

        now = pygame.time.get_ticks()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if not player.alive:
                    if event.key == pygame.K_r:
                        pending_new_run = True
                        lobby.inMenu = False
                        death_time_ms = None
                        paused = False
                    elif event.key in (pygame.K_ESCAPE, pygame.K_m):
                        lobby.inMenu = True
                else:
                    if event.key == pygame.K_ESCAPE:
                        lobby.inMenu = True
                    elif event.key == pygame.K_p:
                        paused = not paused
                    elif event.key in (pygame.K_SPACE, pygame.K_UP) and not paused:
                        support_span = min(player.width * 0.8, 32)
                        floor_y = game.world.find_floor_y(player.rect.centerx, support_span, player.rect.top)
                        ceiling_y = game.world.find_ceiling_y(player.rect.centerx, support_span, player.rect.bottom)
                        if can_switch_on_surface(player, floor_y, ceiling_y):
                            player.switchGravity()

        game.world.drawBackGround(screen)
        game.world.drawWalls(screen)

        if not paused and player.alive:
            game.gameSpeed = min(9.0, game.gameSpeed + 0.0018)
            game.world.update_structures(game.gameSpeed, min(1.0, (game.gameSpeed - 5.0) / 4.0))

        support_span = min(player.width * 0.8, 32)
        floor_y = game.world.find_floor_y(player.rect.centerx, support_span, player.rect.top)
        ceiling_y = game.world.find_ceiling_y(player.rect.centerx, support_span, player.rect.bottom)

        if not paused and player.alive:
            if now - last_spawn >= spawn_interval:
                speed = game.gameSpeed * random.uniform(0.85, 1.2)
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
            speed_bonus = max(0.0, game.gameSpeed - 5.0) * 1.8
            game.score = int((elapsed_s * 12) + (elapsed_s * speed_bonus))
            ob_gen.update(game.gameSpeed)
            player.mov(floor_y=floor_y, ceiling_y=ceiling_y)

            if player.rect.top > screen.get_height() + 40 or player.rect.bottom < -40:
                player.alive = False

            for ob in ob_gen.list_obstacles()[:]:
                if player.rect.colliderect(ob.rect):
                    visual_fx.spawn_for_obstacle(ob.type, ob.rect.center)
                    ob.apply_effect(player)
                    try:
                        ob_gen.obstacles.remove(ob)
                    except ValueError:
                        pass

            if not player.alive:
                game.end()
                paused = False
                ob_gen.obstacles.clear()
                if death_time_ms is None:
                    death_time_ms = now

        ob_gen.draw(screen)
        visual_fx.update_and_draw(screen)
        player.draw(screen)

        interface.show_score(game.score)
        interface.show_best_score(game.bestScore)

        if paused:
            interface.show_pause()

        if not player.alive:
            if death_time_ms is None:
                death_time_ms = now

            dead_elapsed = now - death_time_ms
            if dead_elapsed >= GAME_OVER_DELAY_MS:
                interface.show_game_over()

            if GAME_OVER_RETURN_LOBBY_MS is not None and dead_elapsed >= GAME_OVER_RETURN_LOBBY_MS:
                lobby.inMenu = True

    was_in_menu = lobby.inMenu
    pygame.display.flip()
    clock.tick(60)

pygame.quit()