import os
import pygame
from code.constants import OBSTACLE_DEFAULT_SIZE

"""Module joueur.

Expose une classe Player compatible avec les obstacles et la boucle principale:
- gravite normale/inversee,
- animations simples (marche + flip),
- deplacement contraint par sol/plafond dynamiques,
- rendu avec traines et aura.
"""


class Player:
    """Classe Joueur unifiee: fournit l'API attendue par les obstacles
    et prend aussi en charge des animations de sprite simples si les images existent.
    """
    def __init__(self, nom, x, y):
        self.nom = nom
        # Gravite : direction et vitesse.
        self.gravity_direction = 1  # 1 = normal, -1 = inverted
        self.gravity_speed = 5
        self.is_flipping = False
        self.playerPosition = pygame.Vector2(x, y)

        # Taille / hitbox.
        self.width = 55
        self.height = 55
        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)
        self.alive = True

        # Chargement securise des images d'animation.
        # Si un asset manque, une surface de secours est creee.
        anim_dir = os.path.join('assets', 'Images', 'mov_animation')

        def safe_load(name):
            path = os.path.join(anim_dir, name)
            try:
                img = pygame.image.load(path)
                try:
                    img = img.convert_alpha()
                except Exception:
                    img = img.convert()
                # Redimensionne a la taille du joueur.
                try:
                    img = pygame.transform.scale(img, (self.width, self.height))
                except Exception:
                    pass
                return img
            except Exception:
                surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                surf.fill((0, 255, 0))
                return surf

        # Prefere les fichiers d'animation disponibles ; repli sur des surfaces unies.
        self.walk_normal = [safe_load('mov1_1.img.png'), safe_load('mov2_1.img.png'), safe_load('mov1_1.img.png')]
        self.walk_inverted = [safe_load('mov1_-1.img.png'), safe_load('mov2_-1.img.png'), safe_load('mov1_-1.img.png')]
        self.flip_imgs = [safe_load('flip1.img.png'), safe_load('flip2.img.png')]

        self.current_image = self.walk_normal[0]
        self.anim_index = 0
        self.anim_timer = 0

        # Historique visuel pour dessiner un effet de trainee.
        self.trail_points = []
        self.max_trail_points = 10

    # Methodes d'API requises par les obstacles et le jeu.
    def update_rect(self):
        """Synchronise la hitbox pygame avec la position flottante."""
        self.rect.topleft = (int(self.playerPosition.x), int(self.playerPosition.y))

    def take_damage(self, amount=1):
        """Interface de degats: ici tout degat est fatal."""
        # Simple : n'importe quel degat tue le joueur.
        self.alive = False

    def set_gravity(self, value):
        """Force la gravite a partir d'une valeur signee."""
        try:
            self.gravity_speed = abs(value)
            self.gravity_direction = 1 if value >= 0 else -1
        except Exception:
            pass

    def switchGravity(self):
        """Inverse la gravite et active l'animation de bascule."""
        # Inverse la gravite et lance l'animation de bascule.
        self.gravity_direction *= -1
        self.is_flipping = True
        self.anim_index = 0

    def die(self):
        print('Player died')

    def spawn(self, x=None, y=None):
        """Repositionne le joueur et remet son etat visuel a zero."""
        if x is not None and y is not None:
            self.playerPosition = pygame.Vector2(x, y)
        self.trail_points = []
        self.update_rect()

    # Deplacement / animation.
    def mov(self, floor_y=None, ceiling_y=None, time_scale=1.0):
        """Met a jour animation + physique verticale avec contraintes support."""
        # Temporisation de l'animation.
        self.anim_timer += time_scale
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

        # Applique le mouvement vertical avec une petite tolerance de rattrapage pour eviter
        # de traverser occasionnellement des supports fins ou mobiles.
        prev_y = self.playerPosition.y
        vertical_step = self.gravity_speed * max(0.5, time_scale)
        next_y = prev_y + (vertical_step * self.gravity_direction)
        snap_tolerance = max(18, vertical_step * 3)

        if self.gravity_direction < 0 and ceiling_y is not None:
            min_y = ceiling_y
            if next_y <= min_y and prev_y >= (min_y - snap_tolerance):
                next_y = min_y
                self.is_flipping = False

        if self.gravity_direction > 0 and floor_y is not None:
            max_y = floor_y - self.height
            if next_y >= max_y and prev_y <= (max_y + snap_tolerance):
                next_y = max_y
                self.is_flipping = False

        self.playerPosition.y = next_y
        self.update_rect()

        # Ajoute la position courante dans le buffer de trail (taille bornée).
        self.trail_points.append((self.rect.centerx, self.rect.centery, self.gravity_direction))
        if len(self.trail_points) > self.max_trail_points:
            self.trail_points.pop(0)

    def draw(self, screen):
        """Dessine le joueur avec trail et aura de gravite."""
        trail_len = len(self.trail_points)
        if trail_len > 1:
            for idx, point in enumerate(self.trail_points[:-1]):
                ratio = (idx + 1) / trail_len
                radius = int(3 + (4 * ratio))
                alpha = int(20 + (90 * ratio))
                color = (105, 208, 255, alpha) if point[2] < 0 else (255, 186, 122, alpha)
                glow = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
                pygame.draw.circle(glow, color, (radius + 1, radius + 1), radius)
                screen.blit(glow, (point[0] - radius - 1, point[1] - radius - 1))

        aura_color = (100, 196, 255, 90) if self.gravity_direction < 0 else (255, 172, 110, 90)
        aura = pygame.Surface((self.width + 24, self.height + 24), pygame.SRCALPHA)
        pygame.draw.ellipse(aura, aura_color, aura.get_rect())
        screen.blit(aura, (self.rect.x - 12, self.rect.y - 12))

        # Affiche l'image courante a la position du rectangle.
        screen.blit(self.current_image, self.rect.topleft)