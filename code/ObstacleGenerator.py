import pygame
import random

from code.Obstacle import Obstacle, IMAGES


class ObstacleGenerator:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.obstacles = []
        self.spawn_interval = 1500

    def list_obstacles(self):
        return self.obstacles

    def generate_obstacle(self, obstacleType=None, speed=0):
        # choose a random obstacle type if none provided
        if obstacleType is None:
            obstacleType = random.choice(list(IMAGES.keys()))
        x = self.screen_width
        # position Y so obstacle sits on the platform area (above the purple platform)
        img = IMAGES.get(obstacleType)
        h = img.get_height() if img is not None else 50
        # world.yBottomwall = screen_height - wallHeight - 165, with wallHeight=50
        # place obstacle so its bottom aligns with the top of the bottom wall
        y = self.screen_height - 50 - 165 - h
        new_obstacle = Obstacle(x, y, obstacleType, speed)
        self.obstacles.append(new_obstacle)

    def update(self, speed):
        for obstacle in self.obstacles:
            obstacle.update(speed)
        # keep only obstacles that are still on screen
        self.obstacles = [ob for ob in self.obstacles if ob.rect.right > 0]

    def draw(self, surface):
        for ob in self.obstacles:
            ob.draw(surface)