import pygame

from code.Obstacle import Obstacle

class ObstacleGenerator:
        def __init__(self, screen_width, screen_height):
            self.screen_width = screen_width
            self.screen_height = screen_height
            self.obstacles = []
            self.spawn_interval = 1500
        def list_obstacles(self):
            return self.obstacles
        
        def generate_obstacle(self, obstacleType, speed):
            x = self.screen_width
            y = self.screen_height - 50  # Assuming the obstacle height is 50
            new_obstacle = Obstacle(x, y, obstacleType, speed)
            self.obstacles.append(new_obstacle)
        
        def update(self, speed):
            for obstacle in self.obstacles:
                obstacle.move(speed)
            self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.coord.x + 50 > 0]