import pygame

class Obstacle:
        def __init__(self, x, y, obstacleType, speed):
            self.coord = pygame.math.Vector2(x,y)
            self.type= obstacleType
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))
            self.rect = self.image.get_rect(topleft=(x, y))
        def move(self, speed):
            self.coord.x -= speed
            self.rect.x = self.coord.x