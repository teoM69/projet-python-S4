import pygame

class Obstacle:
        def __init__(self, x, y, obstacleType):
            self.coord = pygame.math.Vector2(x,y)
            self.type= obstacleType
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
        def move(self, speed):
            self.coord.x -= speed
            self.rect.x = self.coord.x