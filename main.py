import pygame
from code.game import Game
from code.lobby import Lobby
from code.Player import Player
from code.ObstacleGenerator import ObstacleGenerator
import random

pygame.init()
screen = pygame.display.set_mode((1000, 700))
clock = pygame.time.Clock()
game = Game(screen)
lobby = Lobby(screen)

# simple player and obstacle generator for runtime testing
player = Player("player", screen.get_height() // 2, 100)
ob_gen = ObstacleGenerator(screen.get_width(), screen.get_height())
last_spawn = pygame.time.get_ticks()
spawn_interval = random.randint(1500, 2600)

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
        game.world.drawBackGround(screen)
        game.world.drawWalls(screen)

        # spawn obstacles periodically
        now = pygame.time.get_ticks()
        if now - last_spawn >= spawn_interval:
            # randomize obstacle speed a bit so they don't all move identically
            speed = game.gameSpeed * random.uniform(0.8, 1.4)
            ob_gen.generate_obstacle(None, speed)
            last_spawn = now
            # pick next spawn interval (ms)
            spawn_interval = random.randint(1500, 3000)

        # update and draw obstacles
        ob_gen.update(game.gameSpeed)
        ob_gen.draw(screen)

        # draw player as a simple rectangle and check collisions
        player.update_rect()
        pygame.draw.rect(screen, (0, 255, 0), player.rect)

        for ob in ob_gen.list_obstacles()[:]:
            if player.rect.colliderect(ob.rect):
                ob.apply_effect(player)
                try:
                    ob_gen.obstacles.remove(ob)
                except ValueError:
                    pass
                # if player died, end game
                if not getattr(player, 'alive', True):
                    game.inGame = False

    pygame.display.flip()
    # limit to 60 FPS to keep obstacle speed consistent
    clock.tick(60)

pygame.quit()