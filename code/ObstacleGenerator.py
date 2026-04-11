import pygame
import random
from code.Obstacle import Obstacle, IMAGES, OBSTACLE_TYPES
from code.constants import WALL_HEIGHT, PLATFORM_BOTTOM_OFFSET


class ObstacleGenerator:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.obstacles = []
        self.spawn_interval = 1500

    def list_obstacles(self):
        return self.obstacles

    def generate_obstacle(self, obstacleType=None, speed=0):
        if obstacleType is None:
            obstacleType = random.choice(OBSTACLE_TYPES)
        x = self.screen_width
        img = IMAGES.get(obstacleType)
        h = img.get_height() if img is not None else 50
        # align obstacle bottom to top of bottom wall
        y = self.screen_height - WALL_HEIGHT - PLATFORM_BOTTOM_OFFSET - h
        new_obstacle = Obstacle(x, y, obstacleType, speed)
        self.obstacles.append(new_obstacle)

    def update(self, speed):
        for obstacle in self.obstacles:
            obstacle.update(speed)
        self.obstacles = [ob for ob in self.obstacles if ob.rect.right > 0]

    def draw(self, surface):
        for ob in self.obstacles:
            ob.draw(surface)