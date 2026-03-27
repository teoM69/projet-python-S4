import pygame
from code.game import Game
from code.lobby import Lobby

pygame.init()
screen = pygame.display.set_mode((1000, 700))
game = Game(screen)
lobby = Lobby(screen)
running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if lobby.inMenu:
        lobby.showMenu(screen)
        lobby.run(screen)
    else:
        game.world.drawBackGround(screen)
        game.world.drawWalls(screen)

    pygame.display.flip()
pygame.quit()
