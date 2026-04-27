import os
import pygame


class VisualEffects:
    """Gestionnaire d'effets visuels temporaires (impact, explosion, push).

    Chaque effet est anime dans le temps avec un fondu alpha et une legere
    variation d'echelle pour renforcer le feedback visuel.
    """
    def __init__(self):
        # Liste des effets actifs a dessiner.
        self.effects = []
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        effect_dir = os.path.join(base_dir, "assets", "Images", "visual effect")

        # Catalogue de sprites d'effets, avec fallback colore si asset absent.
        self.catalog = {
            "effectpush": self._load_image(os.path.join(effect_dir, "effectpush.png"), (120, 210, 255)),
            "explosionbombe": self._load_image(os.path.join(effect_dir, "explosionBombe.png"), (255, 140, 140)),
            "explosiondoublebombe": self._load_image(
                os.path.join(effect_dir, "explosionDoubleBombe.png"),
                (255, 105, 105),
            ),
        }

    def _load_image(self, path, fallback_color):
        """Charge une image et cree un placeholder visuel en cas d'echec."""
        try:
            image = pygame.image.load(path).convert_alpha()
            return image
        except Exception:
            # Fallback visuel si l'asset est manquant.
            surface = pygame.Surface((72, 72), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*fallback_color, 180), (36, 36), 26)
            pygame.draw.circle(surface, (*fallback_color, 70), (36, 36), 33, 4)
            return surface

    def clear(self):
        """Vide tous les effets actifs (utile au reset de run)."""
        self.effects.clear()

    def spawn(self, key, position, duration_ms=260):
        """Instancie un effet du catalogue a la position donnee."""
        image = self.catalog.get((key or "").lower())
        if image is None:
            return
        self.effects.append(
            {
                "key": key.lower(),
                "image": image,
                "pos": position,
                "born": pygame.time.get_ticks(),
                "duration": max(80, int(duration_ms)),
            }
        )

    def spawn_for_obstacle(self, obstacle_type, position):
        """Mappe un type d'obstacle vers un effet visuel adapte."""
        obstacle_name = (obstacle_type or "").lower()
        if "double_bomb" in obstacle_name:
            self.spawn("explosiondoublebombe", position, duration_ms=300)
        elif "bomb" in obstacle_name:
            self.spawn("explosionbombe", position, duration_ms=260)
        elif "push" in obstacle_name:
            self.spawn("effectpush", position, duration_ms=220)

    def update_and_draw(self, screen):
        """Met a jour la vie des effets et dessine ceux encore actifs."""
        if not self.effects:
            return

        now = pygame.time.get_ticks()
        alive = []
        for fx in self.effects:
            elapsed = now - fx["born"]
            duration = fx["duration"]
            if elapsed >= duration:
                continue

            progress = elapsed / duration
            alpha = int(255 * (1.0 - progress))
            scale = 0.92 + (0.40 * progress)

            # Animation: grossissement progressif + disparition en fondu.
            src = fx["image"]
            w = max(1, int(src.get_width() * scale))
            h = max(1, int(src.get_height() * scale))
            frame = pygame.transform.smoothscale(src, (w, h))
            frame.set_alpha(alpha)
            rect = frame.get_rect(center=fx["pos"])
            screen.blit(frame, rect)
            alive.append(fx)

        self.effects = alive