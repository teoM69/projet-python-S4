import os
import pygame
from code.constants import OBSTACLE_DEFAULT_SIZE


class Player:
    """Unified Player class: provides the simple API expected by obstacles
    and also supports simple sprite animations if image files exist.
    """
    def __init__(self, nom, x, y):
        self.nom = nom
        # gravity: direction and speed
        self.gravity_direction = 1  # 1 = normal, -1 = inverted
        self.gravity_speed = 5
        self.is_flipping = False
        self.playerPosition = pygame.Vector2(x, y)

        # size / hitbox
        self.width = 55
        self.height = 55
        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)
        self.alive = True

        # --- safe image loading for animations ---
        anim_dir = os.path.join('assets', 'Images', 'mov_animation')

        def safe_load(name):
            path = os.path.join(anim_dir, name)
            try:
                img = pygame.image.load(path)
                try:
                    img = img.convert_alpha()
                except Exception:
                    img = img.convert()
                # scale to player size
                try:
                    img = pygame.transform.scale(img, (self.width, self.height))
                except Exception:
                    pass
                return img
            except Exception:
                surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                surf.fill((0, 255, 0))
                return surf

        # Prefer available animation files; fallback to solid surfaces
        self.walk_normal = [safe_load('mov1_1.img.png'), safe_load('mov2_1.img.png'), safe_load('mov1_1.img.png')]
        self.walk_inverted = [safe_load('mov1_-1.img.png'), safe_load('mov2_-1.img.png'), safe_load('mov1_-1.img.png')]
        self.flip_imgs = [safe_load('flip1.img.png'), safe_load('flip2.img.png')]
        self.dead_image = safe_load('dead.png')

        self.current_image = self.walk_normal[0]
        self.anim_index = 0
        self.anim_timer = 0

    # API methods required by obstacles / game
    def update_rect(self):
        self.rect.topleft = (int(self.playerPosition.x), int(self.playerPosition.y))

    def take_damage(self, amount=1):
        # simple: any damage kills player
        self.alive = False

    def set_gravity(self, value):
        try:
            self.gravity_speed = abs(value)
            self.gravity_direction = 1 if value >= 0 else -1
        except Exception:
            pass

    def switchGravity(self):
        # flip gravity and start flip animation
        self.gravity_direction *= -1
        self.is_flipping = True
        self.anim_index = 0

    def die(self):
        if  self.alive:
            print('Player died')
            self.alive = False
            self.current_image = self.dead_image

    def spawn(self, x=None, y=None):
        if x is not None and y is not None:
            self.playerPosition = pygame.Vector2(x, y)
        self.update_rect()

    # movement / animation
    def mov(self, floor_y=None):
        # animation timing
        self.anim_timer += 1
        if self.anim_timer > 10:
            self.anim_index += 1
            self.anim_timer = 0

        if self.is_flipping:
            if self.anim_index >= len(self.flip_imgs):
                self.is_flipping = False
                self.anim_index = 0
            else:
                self.current_image = self.flip_imgs[self.anim_index]
        elif self.gravity_direction == 1:
            self.anim_index %= len(self.walk_normal)
            self.current_image = self.walk_normal[self.anim_index]
        else:
            self.anim_index %= len(self.walk_inverted)
            self.current_image = self.walk_inverted[self.anim_index]

        # apply physics
        self.playerPosition.y += (self.gravity_speed * self.gravity_direction)
        # clamp to floor if provided (player bottom should not go below floor_y)
        if floor_y is not None:
            max_y = floor_y - self.height
            if self.playerPosition.y > max_y:
                self.playerPosition.y = max_y
                self.is_flipping = False
            if self.playerPosition.y < 0:
                self.playerPosition.y = 0
        self.update_rect()

    def draw(self, screen):
        # blit current image at rect.topleft
        screen.blit(self.current_image, self.rect.topleft)

       