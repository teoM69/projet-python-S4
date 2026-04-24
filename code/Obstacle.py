import os
import math
from collections import deque
import pygame
from code.constants import OBSTACLE_DEFAULT_SIZE

_IMAGE_NAMES = [
    'bomb.png',
    'double_bomb.png',
    'obstacle_push1.png',
    'obstacle_push2.png',
]

# Liste publique des types d'obstacles (noms de fichiers). Importable sans charger les images.
OBSTACLE_TYPES = list(_IMAGE_NAMES)

# Stocke les chemins et charge les images paresseusement au premier besoin (apres pygame.init()).
IMAGES = {}
_IMAGE_PATHS = {}

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
    if _OB_DIR:
        path = os.path.join(_OB_DIR, name)
        if os.path.isfile(path):
            _IMAGE_PATHS[name] = path


def ensure_images_loaded():
    """Charge les images dans le dictionnaire IMAGES au premier usage. Appelable a tout moment ;
    en cas d'echec de chargement, des surfaces de remplacement sont creees."""
    if IMAGES:
        return
    for name in _IMAGE_NAMES:
        img = None
        path = _IMAGE_PATHS.get(name)
        if path:
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
        # S'assure que les images sont chargees (chargement paresseux apres pygame.init()).
        try:
            ensure_images_loaded()
        except Exception:
            pass
        self.coord = pygame.math.Vector2(x, y)
        self.type = obstacleType
        self.image = IMAGES.get(obstacleType)
        if self.image is None:
            # Repli de secours.
            self.image = next(iter(IMAGES.values()))
        self.rect = self.image.get_rect(topleft=(int(x), int(y)))
        self.speed = speed
        self.spawn_time_ms = pygame.time.get_ticks()
        self.trail = deque(maxlen=8)

    def move(self, speed):
        self.coord.x -= speed
        self.rect.x = int(self.coord.x)

    def update(self, speed=None):
        s = speed if speed is not None else self.speed
        self.move(s)
        self.trail.append((self.rect.centerx, self.rect.centery))

    def draw(self, surface):
        # Evite les effets couteux tant que l'obstacle est hors de l'ecran.
        if self.rect.right < -80 or self.rect.left > surface.get_width() + 80:
            return

        now = pygame.time.get_ticks()
        age_ms = now - self.spawn_time_ms

        t = (self.type or '').lower()
        if 'bomb' in t:
            base_color = (255, 96, 96)
            trail_color = (255, 120, 120)
        elif 'push' in t:
            base_color = (110, 205, 255)
            trail_color = (130, 220, 255)
        else:
            base_color = (220, 220, 220)
            trail_color = (220, 220, 220)

        # Trainee lumineuse discrète pour mieux lire le mouvement.
        trail_len = len(self.trail)
        if trail_len > 1:
            for idx, point in enumerate(self.trail):
                ratio = (idx + 1) / trail_len
                radius = int(2 + (4 * ratio))
                alpha = int(15 + (65 * ratio))
                glow = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(glow, (trail_color[0], trail_color[1], trail_color[2], alpha), (radius + 2, radius + 2), radius)
                surface.blit(glow, (point[0] - radius - 2, point[1] - radius - 2))

        shadow = pygame.Surface((self.rect.width + 10, self.rect.height + 10), pygame.SRCALPHA)
        pygame.draw.ellipse(
            shadow,
            (0, 0, 0, 85),
            (4, self.rect.height - 4, max(8, self.rect.width - 2), 10),
        )
        surface.blit(shadow, (self.rect.x - 5, self.rect.y))

        surface.blit(self.image, self.rect)

        pulse = 0.5 + (0.5 * math.sin((pygame.time.get_ticks() * 0.012) + (self.rect.x * 0.04)))
        glow_alpha = int(55 + (85 * pulse))
        glow = pygame.Surface((self.rect.width + 20, self.rect.height + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(glow, (base_color[0], base_color[1], base_color[2], glow_alpha), glow.get_rect(), width=3)
        surface.blit(glow, (self.rect.x - 10, self.rect.y - 10))

        # Petit flash d'apparition pour eviter l'effet "pop" sec.
        if age_ms < 240:
            progress = age_ms / 240.0
            ring_w = int(self.rect.width + 10 + (36 * progress))
            ring_h = int(self.rect.height + 10 + (36 * progress))
            ring_alpha = int(150 * (1.0 - progress))
            ring = pygame.Surface((ring_w, ring_h), pygame.SRCALPHA)
            pygame.draw.ellipse(ring, (base_color[0], base_color[1], base_color[2], ring_alpha), ring.get_rect(), width=2)
            surface.blit(ring, (self.rect.centerx - (ring_w // 2), self.rect.centery - (ring_h // 2)))

    def apply_effect(self, player):
        t = (self.type or '').lower()
        # bombe => degats
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
        # poussoir => inverse la gravite si possible
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