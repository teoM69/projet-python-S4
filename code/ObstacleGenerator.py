import pygame
import random
from code.Obstacle import Obstacle, IMAGES, OBSTACLE_TYPES, ensure_images_loaded
from code.constants import WALL_HEIGHT, PLATFORM_BOTTOM_OFFSET


class ObstacleGenerator:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.obstacles = []
        self.spawn_interval = 1500

    def list_obstacles(self):
        return self.obstacles

    def _spawn_x(self):
        x = self.screen_width
        # Keep a minimum horizontal spacing near the spawn edge to avoid
        # stacked obstacles appearing at odd positions.
        if self.obstacles:
            rightmost = max(ob.rect.right for ob in self.obstacles)
            min_gap = random.randint(80, 160)
            x = max(x, rightmost + min_gap)
        return x

    def _clamp_y(self, y, h):
        min_y = 0
        max_y = max(0, self.screen_height - h)
        return max(min_y, min(max_y, int(y)))

    def generate_obstacle(self, obstacleType=None, speed=0, lane=None, top_lane_y=None, bottom_lane_y=None, middle_lane_y=None):
        ensure_images_loaded()

        if obstacleType is None:
            obstacleType = random.choice(OBSTACLE_TYPES)

        available_lanes = ["top", "bottom"]
        if middle_lane_y is not None:
            available_lanes.append("middle")

        if lane not in available_lanes:
            lane = None

        if lane is None:
            if "middle" in available_lanes:
                lane = random.choices(["top", "bottom", "middle"], weights=[0.4, 0.4, 0.2])[0]
            else:
                lane = random.choice(["top", "bottom"])

        x = self._spawn_x()
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

        y = self._clamp_y(y, h)

        new_obstacle = Obstacle(x, y, obstacleType, speed)
        self.obstacles.append(new_obstacle)

    def update(self, speed):
        for obstacle in self.obstacles:
            obstacle.update(speed)
        self.obstacles = [ob for ob in self.obstacles if ob.rect.right > 0]

    def draw(self, surface):
        for ob in self.obstacles:
            ob.draw(surface)