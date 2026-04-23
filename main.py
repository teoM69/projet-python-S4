import pygame
import random
from code.game import Game
from code.lobby import Lobby
from code.Player import Player
from code.ObstacleGenerator import ObstacleGenerator
from code.constants import OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS
from code.interface import Interface

pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()

game = Game(screen)
lobby = Lobby(screen)
interface = Interface(screen)

# test player and obstacle generator (kept local here for quick testing)
player = Player('player', 100, screen.get_height() - 50 - 165 - 55)
ob_gen = ObstacleGenerator(screen.get_width(), screen.get_height())
last_spawn = pygame.time.get_ticks()
spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)

running = True
paused = False

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:       # ← ajoute ça
            if event.key == pygame.K_p:        # ← et ça
                paused = not paused     

    screen.fill((0, 0, 0))

    if lobby.inMenu:
        lobby.run(screen, events)
    else:
        # draw world
        game.world.drawBackGround(screen)
        game.world.drawWalls(screen)

        # === UPDATE WORLD STRUCTURES ===
        # Generate platforms (top, bottom, middle) with "holes" (gaps)
        game.world.update_structures(game.gameSpeed)

        # spawn obstacles periodically on 3 different lanes
        now = pygame.time.get_ticks()
        if now - last_spawn >= spawn_interval:
            speed = game.gameSpeed * random.uniform(0.8, 1.3)
            # Get Y positions for each lane to spawn obstacles correctly
            top_lane_y = game.world.roof_y
            bottom_lane_y = game.world.floor_y
            middle_lane_y = game.world.get_middle_spawn_y()
            
            # Spawn obstacle with all 3 lanes (creates variety)
            ob_gen.generate_obstacle(
                None, 
                speed,
                top_lane_y=top_lane_y,
                bottom_lane_y=bottom_lane_y,
                middle_lane_y=middle_lane_y
            )
            last_spawn = now
            spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)

        # update and draw obstacles
        ob_gen.update(game.gameSpeed)
        ob_gen.draw(screen)

        # update/draw player (keep on platform)
        # === COLLISION & STRUCTURE SUPPORT (Joueur 1) ===
        # Détecte le toit et sol dynamiques du monde AVANT de bouger le joueur
        support_span = min(player.width * 0.8, 32)
        floor_y = game.world.find_floor_y(player.rect.centerx, support_span, player.rect.top)
        ceiling_y = game.world.find_ceiling_y(player.rect.centerx, support_span, player.rect.bottom)
        
        # Applique les contraintes de collision au mouvement du joueur
        player.mov(floor_y=floor_y, ceiling_y=ceiling_y)

        # Kill player if they fall out of the playable area.
        if player.rect.top > screen.get_height() + 40 or player.rect.bottom < -40:
            player.alive = False

        player.draw(screen)
       
        interface.show_score(game.score)
        interface.show_best_score(game.bestScore)

        if paused:
            interface.show_pause()

        if not player.alive:
            interface.show_game_over()
            lobby.inMenu = True

        # collisions with obstacles
        for ob in ob_gen.list_obstacles()[:]:
            if player.rect.colliderect(ob.rect):
                ob.apply_effect(player)
                try:
                    ob_gen.obstacles.remove(ob)
                except ValueError:
                    pass
                if not getattr(player, 'alive', True):
                    # simple: go back to menu on death
                    lobby.inMenu = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()