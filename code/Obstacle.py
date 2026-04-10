import os
import pygame

# Load obstacle images once at module import
IMAGES = {}
_IMAGE_NAMES = [
    'Bomb.png',
    'double_bomb.png',
    'obstacle_push1.png',
    'obstacle_push2.png',
]

def _find_obstacles_dir():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    # try common capitalizations
    candidates = [
        os.path.join(base, 'assets', 'Images', 'obstacles'),
        os.path.join(base, 'assets', 'images', 'obstacles'),
        os.path.join(base, 'assets', 'Images', 'Obstacles'),
    ]
    for c in candidates:
        if os.path.isdir(c):
            return c
    return None

_OBSTACLES_DIR = _find_obstacles_dir()
for name in _IMAGE_NAMES:
    if _OBSTACLES_DIR:
        path = os.path.join(_OBSTACLES_DIR, name)
    else:
        path = None
    try:
        if path and os.path.isfile(path):
            img = pygame.image.load(path)
            # convert_alpha requires a display surface; fall back to convert()
            try:
                if pygame.display.get_init() and pygame.display.get_surface() is not None:
                    img = img.convert_alpha()
                else:
                    img = img.convert()
            except Exception:
                # if conversion fails, keep original
                pass
            # normalize size: scale to 50x50 by default
            IMAGES[name] = pygame.transform.scale(img, (50, 50))
        else:
            raise FileNotFoundError(path)
    except Exception:
        # placeholder surface when image missing or loading failed
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        surf.fill((255, 0, 0, 180))
        IMAGES[name] = surf


class Obstacle:
    def __init__(self, x, y, obstacleType, speed=0):
        self.coord = pygame.math.Vector2(x, y)
        self.type = obstacleType
        self.image = IMAGES.get(obstacleType)
        if self.image is None:
            # fallback to first image
            self.image = next(iter(IMAGES.values()))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def move(self, speed):
        self.coord.x -= speed
        self.rect.x = int(self.coord.x)

    def update(self, speed=None):
        # Move obstacle; prefer passed speed over stored
        s = speed if speed is not None else self.speed
        self.move(s)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def apply_effect(self, player):
        """Apply obstacle-specific effect to `player` safely.

        - obstacles with 'push' in the filename will try to invert or change gravity
        - obstacles with 'bomb' will try to mark player as dead or call `take_damage`
        This method performs attribute checks to avoid breaking unknown Player API.
        """
        t = (self.type or '').lower()
        if 'push' in t:
            if hasattr(player, 'gravity'):
                try:
                    player.gravity = -player.gravity
                except Exception:
                    pass
            elif hasattr(player, 'set_gravity'):
                try:
                    current = getattr(player, 'gravity', 1)
                    player.set_gravity(-current)
                except Exception:
                    pass
        elif 'bomb' in t:
            if hasattr(player, 'take_damage'):
                try:
                    player.take_damage(1)
                except Exception:
                    pass
            elif hasattr(player, 'alive'):
                try:
                    player.alive = False
                except Exception:
                    pass
            else:
                try:
                    setattr(player, 'dead', True)
                except Exception:
                    pass
