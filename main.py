import pygame
from code.game import Game

pygame.init()
screen = pygame.display.set_mode((1000, 700))
game = Game(screen)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    game.world.drawBackGround(screen)
    game.world.drawWalls(screen)
    pygame.display.flip()
pygame.quit()