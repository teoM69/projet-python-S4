import os
import pygame
from code.constants import OBSTACLE_DEFAULT_SIZE

# Load obstacle images
IMAGES = {}
_IMAGE_NAMES = [
    'bomb.png',
    'double_bomb.png',
    'obstacle_push1.png',
    'obstacle_push2.png',
]

def _obstacles_dir():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    candidates = [
        os.path.join(base, 'assets', 'Images', 'obstacles'),
        os.path.join(base, 'assets', 'images', 'obstacles'),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return None

_OB_DIR = _obstacles_dir()
for name in _IMAGE_NAMES:
    img = None
    if _OB_DIR:
        path = os.path.join(_OB_DIR, name)
        if os.path.isfile(path):
            try:
                img = pygame.image.load(path)
                try:
                    img = img.convert_alpha()
                except Exception:
                    img = img.convert()
            except Exception:
                img = None
    if img is None:
        surf = pygame.Surface(OBSTACLE_DEFAULT_SIZE, pygame.SRCALPHA)
        surf.fill((255, 0, 0, 180))
        IMAGES[name] = surf
    else:
        IMAGES[name] = pygame.transform.scale(img, OBSTACLE_DEFAULT_SIZE)


class Obstacle:
    def __init__(self, x, y, obstacleType, speed=0):
        self.coord = pygame.math.Vector2(x, y)
        self.type = obstacleType
        self.image = IMAGES.get(obstacleType)
        if self.image is None:
            # fallback
            self.image = next(iter(IMAGES.values()))
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        self.speed = speed

    def move(self, speed):
        self.coord.x -= speed
        self.rect.x = int(self.coord.x)

    def update(self, speed=None):
        s = speed if speed is not None else self.speed
        self.move(s)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def apply_effect(self, player):
        t = (self.type or '').lower()
        # bomb => damage
        if 'bomb' in t:
            if hasattr(player, 'take_damage'):
                try:
                    player.take_damage(1)
                except Exception:
                    pass
            else:
                try:
                    player.alive = False
                except Exception:
                    pass
        # push => flip gravity if available
        if 'push' in t:
            if hasattr(player, 'switchGravity'):
                try:
                    player.switchGravity()
                except Exception:
                    pass
            elif hasattr(player, 'set_gravity'):
                try:
                    player.set_gravity(-getattr(player, 'gravity_speed', 5))
                except Exception:
                    pass