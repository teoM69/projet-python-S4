import pygame
import random
from code.Obstacle import Obstacle, IMAGES, OBSTACLE_TYPES, ensure_images_loaded
from code.constants import (
    WALL_HEIGHT,
    PLATFORM_BOTTOM_OFFSET,
    OBSTACLE_SPAWN_X_OFFSET_MIN,
    OBSTACLE_SPAWN_X_OFFSET_MAX,
    OBSTACLE_SPAWN_GAP_MIN,
    OBSTACLE_SPAWN_GAP_MAX,
    OBSTACLE_WORLD_MIN_RIGHT_EDGE,
    OBSTACLE_TYPE_WEIGHTS,
)


class ObstacleGenerator:
    """Fabrique et met a jour les obstacles actifs.

    Le generateur choisit un type d'obstacle, selectionne une lane valide,
    calcule une position de spawn coherente avec le monde, puis conserve la
    liste des obstacles a mettre a jour et dessiner.
    """
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.obstacles = []
        self.spawn_interval = 1500

    def set_screen_size(self, screen_width, screen_height):
        """Met a jour les dimensions de reference de l'ecran."""
        self.screen_width = int(screen_width)
        self.screen_height = int(screen_height)

    def list_obstacles(self):
        """Expose la liste courante des obstacles."""
        return self.obstacles

    def _spawn_x(self):
        """Calcule une position X de spawn hors ecran avec espacement minimum."""
        x = self.screen_width + random.randint(OBSTACLE_SPAWN_X_OFFSET_MIN, OBSTACLE_SPAWN_X_OFFSET_MAX)
        # Conserve un espacement horizontal minimum pres du point d'apparition pour eviter
        # que des obstacles empiles apparaissent dans des positions bizarres.
        if self.obstacles:
            rightmost = max(ob.rect.right for ob in self.obstacles)
            min_gap = random.randint(OBSTACLE_SPAWN_GAP_MIN, OBSTACLE_SPAWN_GAP_MAX)
            x = max(x, rightmost + min_gap)
        return x

    def _clamp_y(self, y, h):
        """Contraint la coordonnee Y dans les limites de l'ecran."""
        min_y = 0
        max_y = max(0, self.screen_height - h)
        return max(min_y, min(max_y, int(y)))

    def _choose_obstacle_type(self):
        """Tire un type d'obstacle selon une loi ponderee."""
        # Les bombes sont plus frequentes que les obstacles de poussée.
        return random.choices(
            OBSTACLE_TYPES,
            weights=OBSTACLE_TYPE_WEIGHTS,
            k=1,
        )[0]

    def generate_obstacle(self, obstacleType=None, speed=0, lane=None, top_lane_y=None, bottom_lane_y=None, middle_lane_y=None, world=None):
        """Genere un obstacle sur une lane valide.

        Retourne True si un obstacle est cree, False sinon (aucune lane valide).
        """
        ensure_images_loaded()

        if obstacleType is None:
            obstacleType = self._choose_obstacle_type()

        x = self._spawn_x()
        img = IMAGES.get(obstacleType)
        h = img.get_height() if img is not None else 50

        supported_lanes = []
        if world is not None:
            supported_lanes = world.get_spawn_targets(min_right_edge=self.screen_width + OBSTACLE_WORLD_MIN_RIGHT_EDGE)
        else:
            supported_lanes = [
                ("top", 0, self.screen_width, top_lane_y if top_lane_y is not None else WALL_HEIGHT),
                (
                    "bottom",
                    0,
                    self.screen_width,
                    bottom_lane_y if bottom_lane_y is not None else self.screen_height - WALL_HEIGHT - PLATFORM_BOTTOM_OFFSET,
                ),
            ]
            if middle_lane_y is not None:
                supported_lanes.append(("middle", 0, self.screen_width, middle_lane_y))

        if lane is not None:
            supported_lanes = [entry for entry in supported_lanes if entry[0] == lane]

        if not supported_lanes:
            return False

        if lane is None:
            lane, lane_left, lane_right, lane_y = random.choice(supported_lanes)
        else:
            lane_left, lane_right, lane_y = supported_lanes[0][1], supported_lanes[0][2], supported_lanes[0][3]

        if world is not None:
            # Restreint le spawn a une zone situee a droite de l'ecran visible.
            x_min = int(max(self.screen_width + OBSTACLE_WORLD_MIN_RIGHT_EDGE, lane_left))
            x_max = int(max(x_min, lane_right - max(1, h)))
            if x_max <= x_min:
                return False
            x = random.randint(x_min, x_max)

        if lane == "top":
            y = lane_y
        elif lane == "middle":
            y = lane_y - h
        else:
            # Aligne le bas de l'obstacle sur le haut du support du bas.
            y = lane_y - h

        y = self._clamp_y(y, h)

        new_obstacle = Obstacle(x, y, obstacleType, speed)
        self.obstacles.append(new_obstacle)
        return True

    def update(self, speed):
        """Met a jour les obstacles et supprime ceux sortis de l'ecran."""
        removed_count = 0
        for obstacle in self.obstacles:
            obstacle.update(speed)
        kept = []
        for obstacle in self.obstacles:
            if obstacle.rect.right > 0:
                kept.append(obstacle)
            else:
                removed_count += 1
        self.obstacles = kept
        return removed_count

    def draw(self, surface):
        """Dessine tous les obstacles actifs."""
        for ob in self.obstacles:
            ob.draw(surface)