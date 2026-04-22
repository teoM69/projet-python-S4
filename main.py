import pygame
import random
from code.game import Game
from code.lobby import Lobby
from code.Player import Player
from code.ObstacleGenerator import ObstacleGenerator
from code.constants import OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS

pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()

game = Game(screen)
lobby = Lobby(screen)

# test player and obstacle generator (kept local here for quick testing)
player = Player('player', 100, screen.get_height() - 50 - 165 - 40)
ob_gen = ObstacleGenerator(screen.get_width(), screen.get_height())
last_spawn = pygame.time.get_ticks()
spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)

running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if lobby.inMenu:
        lobby.run(screen, events)
    else:
        # draw world
        game.world.drawBackGround(screen)
        game.world.drawWalls(screen)

        # spawn obstacles periodically
        now = pygame.time.get_ticks()
        if now - last_spawn >= spawn_interval:
            speed = game.gameSpeed * random.uniform(0.8, 1.3)
            ob_gen.generate_obstacle(None, speed)
            last_spawn = now
            spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)

        # update and draw obstacles
        ob_gen.update(game.gameSpeed)
        ob_gen.draw(screen)

        # update/draw player (keep on platform)
        floor_y = screen.get_height() - 50 - 165
        player.mov(floor_y=floor_y)
        player.draw(screen)

        # collisions
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
        
        # === COLLISION & STRUCTURE SUPPORT (Joueur 1) ===
        # Détecte si le joueur se pose sur les structures du monde
        support_span = player.width * 0.8  # Zone de collision du joueur (80% de sa largeur)
        floor_y = game.world.find_floor_y(player.rect.centerx, support_span, player.rect.top)  # Sol le plus proche
        ceiling_y = game.world.find_ceiling_y(player.rect.centerx, support_span, player.rect.bottom)  # Plafond le plus proche
        
        # === COLLISION & STRUCTURE SUPPORT (Joueur 2) - Mode Duo ===
        # Même détection pour le joueur 2 en mode duo
        floor_y_p2 = None
        ceiling_y_p2 = None
        # À implémenter : détection pour joueur 2 si mode duo actif
        
        # === AUTRES POINTS DE DÉTECTION ===
        # Points de détection additionnels pour une physique plus précise
        # À implémenter selon les besoins du gameplay

    pygame.display.flip()
    clock.tick(60)

pygame.quit()