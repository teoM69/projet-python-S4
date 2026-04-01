import pygame
from code.game import Game
from code.lobby import Lobby

pygame.init()
screen = pygame.display.set_mode((1000, 700))
game = Game(screen)
lobby = Lobby(screen)
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

    pygame.display.flip()

pygame.quit()