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

    def generate_obstacle(self, obstacleType=None, speed=0, lane=None, top_lane_y=None, bottom_lane_y=None, middle_lane_y=None):
        if obstacleType is None:
            obstacleType = random.choice(OBSTACLE_TYPES)
        if lane is None:
            if middle_lane_y is not None:
                lane = random.choices(["top", "bottom", "middle"], weights=[0.4, 0.4, 0.2])[0]
            else:
                lane = random.choice(["top", "bottom"])
        x = self.screen_width
        img = IMAGES.get(obstacleType)
        h = img.get_height() if img is not None else 50

        floor_y = bottom_lane_y if bottom_lane_y is not None else self.screen_height - WALL_HEIGHT - PLATFORM_BOTTOM_OFFSET
        if lane == "top":
            y = top_lane_y if top_lane_y is not None else WALL_HEIGHT
        elif lane == "middle" and middle_lane_y is not None:
            y = middle_lane_y - h
        else:
            # align obstacle bottom to top of bottom wall
            y = floor_y - h

        new_obstacle = Obstacle(x, y, obstacleType, speed)
        self.obstacles.append(new_obstacle)

    def update(self, speed):
        for obstacle in self.obstacles:
            obstacle.update(speed)
        self.obstacles = [ob for ob in self.obstacles if ob.rect.right > 0]

    def draw(self, surface):
        for ob in self.obstacles:
            ob.draw(surface)