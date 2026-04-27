import pygame


class Interface:
    """Couche d'interface utilisateur en surimpression.

    Gere:
    - score et best score,
    - ecrans d'etat (pause, game over),
    - mecanisme de cache pour eviter de rerender du texte inutilement.
    """
    def __init__(self, screen):
        self.screen = screen

        # Polices de l'UI (titre, texte principal, sous-texte).
        self.font_main = pygame.font.SysFont('Arial', 32)
        self.font_title = pygame.font.SysFont('Arial', 72, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 24)

        # Palette UI.
        self.color_white = (255, 255, 255)
        self.color_gold = (255, 215, 0)
        self.color_red = (250, 50, 50)
        self.overlay_color = (0, 0, 0, 150)

        # Cache des surfaces score/best pour limiter les allocations et render text.
        self._cached_score = None
        self._cached_best = None
        self._score_surf = None
        self._best_surf = None
        self._best_rect = None

        # Overlay translucide reutilise pour les ecrans de pause/game over.
        self._overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self._overlay.fill(self.overlay_color)

        # Cache de messages generiques (titre + hint + couleur) pour eviter rerender.
        self._message_cache = {}

    def show_score(self, score, best_score):
        """Dessine le score courant et le meilleur score en haut de l'ecran."""
        # score en haut à gauche
        if score != self._cached_score:
            self._cached_score = score
            self._score_surf = self.font_main.render(f"Score: {score}", True, self.color_white)
        if self._score_surf is not None:
            self.screen.blit(self._score_surf, (25, 25))

        # best score en haut à droite
        if best_score != self._cached_best:
            self._cached_best = best_score
            self._best_surf = self.font_main.render(f"Best: {best_score}", True, self.color_gold)
            self._best_rect = self._best_surf.get_rect(topright=(self.screen.get_width() - 25, 25))
        if self._best_surf is not None and self._best_rect is not None:
            self.screen.blit(self._best_surf, self._best_rect)

    def draw_overlay(self):
        """Dessine un voile sombre derriere les messages d'etat."""
        self.screen.blit(self._overlay, (0, 0))

    def show_message(self, title, hint, color):
        """Affiche un panneau centre avec titre et sous-texte, avec cache memoise."""
        self.draw_overlay()
        key = (title, hint, color)
        cached = self._message_cache.get(key)
        if cached is None:
            # titre
            title_surf = self.font_title.render(title, True, color)
            title_rect = title_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

            # sous titre
            hint_surf = self.font_small.render(hint, True, self.color_white)
            hint_rect = hint_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 60))
            cached = (title_surf, title_rect, hint_surf, hint_rect)
            self._message_cache[key] = cached

        title_surf, title_rect, hint_surf, hint_rect = cached
        self.screen.blit(title_surf, title_rect)
        self.screen.blit(hint_surf, hint_rect)

    def show_pause(self):
        """Affiche l'ecran de pause."""
        self.show_message("PAUSE", "Appuyez sur P pour reprendre", self.color_white)

    def show_game_over(self):
        """Affiche l'ecran de fin de partie."""
        self.show_message("GAME OVER", "Appuyez sur R pour rejouer", self.color_red)