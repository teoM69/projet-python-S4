"""Script local de test rapide.

Ce fichier semble etre un brouillon de test lance depuis Code Runner.
Il n'est pas aligne avec la boucle principale de main.py mais reste documente
pour clarifier son intention et son fonctionnement.
"""

import pygame
import random
from code.game import Game
from code.lobby import Lobby
from code.Player import Player
from code.ObstacleGenerator import ObstacleGenerator
from code.constants import OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS
from code.interface import Interface

pygame.init()
# Fenetre de test simple, sans les options avancees utilisees dans main.py.
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()

game = Game(screen)
lobby = Lobby(screen, game)
interface = Interface(screen)

# Test local de creation du joueur et du generateur d'obstacles.
player = Player("player", 100, screen.get_height() - 50 - 165 - 55)
print(player.nom)
ob_gen = ObstacleGenerator(screen.get_width(), screen.get_height())
last_spawn = pygame.time.get_ticks()
spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)

running = True
paused = False

while running:
    # Poll des evenements de la frame.
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    screen.fill((0, 0, 0))

    if lobby.inMenu:
        lobby.run(screen, events)
    else:
        # Synchronise les infos joueur avec l'etat du lobby.
        player.nom = lobby.name
        game.name = player.nom
        game.setScores()
        # Rendu du monde.
        game.world.drawBackGround(screen)
        game.world.drawWalls(screen)

        # === UPDATE WORLD STRUCTURES ===
        # Generate platforms (top, bottom, middle) with "holes" (gaps)
        game.world.update_structures(game.gameSpeed)

        # Spawn periodique sur les 3 voies possibles.
        now = pygame.time.get_ticks()
        if now - last_spawn >= spawn_interval:
            speed = game.gameSpeed * random.uniform(0.8, 1.3)
            # Coordonnees Y utilisees pour aligner correctement chaque lane.
            top_lane_y = game.world.roof_y
            bottom_lane_y = game.world.floor_y
            middle_lane_y = game.world.get_middle_spawn_y()

            # Generation d'un obstacle en deleguant le choix final au generateur.
            ob_gen.generate_obstacle(
                None, 
                speed,
                top_lane_y=top_lane_y,
                bottom_lane_y=bottom_lane_y,
                middle_lane_y=middle_lane_y
            )
            last_spawn = now
            spawn_interval = random.randint(OBSTACLE_SPAWN_MIN_MS, OBSTACLE_SPAWN_MAX_MS)

        # Mise a jour et rendu des obstacles.
        ob_gen.update(game.gameSpeed)
        ob_gen.draw(screen)

        # Detection des supports dynamiques avant de deplacer le joueur.
        support_span = player.width * 0.8
        floor_y = game.world.find_floor_y(player.rect.centerx, support_span, player.rect.top)
        ceiling_y = game.world.find_ceiling_y(player.rect.centerx, support_span, player.rect.bottom)

        # Mouvement du joueur sous contraintes sol/plafond.
        player.mov(floor_y=floor_y, ceiling_y=ceiling_y)
        player.draw(screen)

        interface.show_score(game.score, game.bestScore)

        if paused:
            interface.show_pause()

        if not player.alive:
            interface.show_game_over()

        # Collisions obstacle -> application d'effet gameplay.
        for ob in ob_gen.list_obstacles()[:]:
            if player.rect.colliderect(ob.rect):
                ob.apply_effect(player)
                try:
                    ob_gen.obstacles.remove(ob)
                except ValueError:
                    pass
                if not getattr(player, 'alive', True):
                    # Comportement de test: retour menu immediat apres mort.
                    lobby.inMenu = True

        # Score de test incremente a chaque frame.
        game.score += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()