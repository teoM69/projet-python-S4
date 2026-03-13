import pygame
from Obstacle import Obstacle
class World:
        def __init__(self, speed, screen_height, screen_width):
            self.speed = speed
            self.wallHeight = 50
            self.obstacle = []
            self.yUpperWall = 0
            self.yBottomwall = screen_height - self.wallHeight
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.bg_image = pygame.image.load('assets\Images\BackGround.png').convert
            self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
              
        def drawBackGround(self, screen):
             screen.blit(self.bg_image, (0, 0))
              
        def drawWalls(self, screen):
              pygame.draw.rect(screen, "RED", [0, self.yUpperWall, self.screen_width, self.wallHeight])
              pygame.draw.rect(screen, "RED", [0, self.yBottomwall, self.screen_width, self.wallHeight])