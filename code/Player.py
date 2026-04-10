import os
import pygame
from code.constants import OBSTACLE_DEFAULT_SIZE


class Player:
    def __init__(self, nom, x, y):
        self.nom = nom
        self.gravity_direction = 1  # 1 = normal, -1 = inversé
        self.gravity_speed = 5
        self.is_flipping = False
        self.playerPosition = pygame.Vector2(x, y)

        # size / hitbox
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)
        self.alive = True

        # --- Chargement des images (fallback si absent) ---
        anim_dir = os.path.join('assets', 'Images', 'mov_animation')
        def safe_load(name):
            path = os.path.join(anim_dir, name)
            try:
                img = pygame.image.load(path)
                try:
                    img = img.convert_alpha()
                except Exception:
                    img = img.convert()
                return img
            except Exception:
                surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                surf.fill((0, 255, 0))
                return surf

        # Using available filenames in repository (fallback to simple surfaces)
        self.walk_normal = [safe_load('mov1_1.img.png'), safe_load('mov2_1.img.png'), safe_load('mov1_1.img.png')]
        self.walk_inverted = [safe_load('mov1_-1.img.png'), safe_load('mov2_-1.img.png'), safe_load('mov1_-1.img.png')]
        self.flip_imgs = [safe_load('flip1.img.png'), safe_load('flip2.img.png')]

        self.current_image = self.walk_normal[0]
        self.anim_index = 0
        self.anim_timer = 0

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
        # On change la direction et on lance l'animation de salto
        self.gravity_direction *= -1
        self.is_flipping = True
        self.anim_index = 0

    def mov(self):
        # 1. Gestion du timing de l'animation
        self.anim_timer += 1
        if self.anim_timer > 10:
            self.anim_index += 1
            self.anim_timer = 0

        # 2. Logique visuelle (Quelle image afficher ?)
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

        # 3. Application du mouvement physique
        self.playerPosition.y += (self.gravity_speed * self.gravity_direction)
        self.update_rect()

    def draw(self, screen):
        # blit current image at rect.topleft
        screen.blit(self.current_image, self.rect.topleft)

    def die(self):
        print("die")

    def spawn(self, x=None, y=None):
        if x is not None and y is not None:
            self.playerPosition = pygame.Vector2(x, y)
        self.update_rect()
       