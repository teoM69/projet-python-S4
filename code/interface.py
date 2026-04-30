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

    def set_screen(self, screen):
        """Met a jour la surface cible apres resize/plein ecran."""
        self.screen = screen
        self._overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self._overlay.fill(self.overlay_color)
        # Invalide les positions dependantes de la taille d'ecran.
        self._best_rect = None
        self._message_cache = {}

    def show_score(self, score, best_score):
        if score != self._cached_score:
            self._cached_score = score
            self._score_surf = self.font_main.render(f"  {score}", True, self.color_white)
        if best_score != self._cached_best:
            self._cached_best = best_score
            self._best_surf = self.font_main.render(f"  {best_score}", True, self.color_gold)
        if self._score_surf is None or self._best_surf is None:
            return
        label_score = self.font_small.render("SCORE", True, (180, 180, 180))
        label_best = self.font_small.render("MEILLEUR", True, (255, 200, 0))
        padding = 18
        spacing = 10
        separator = 1
        inner_width = max(
              self._score_surf.get_width(), self._best_surf.get_width(),
                label_score.get_width(), label_best.get_width()
                )
        box_width = inner_width + padding * 2
        box_height = (
            label_best.get_height() + self._best_surf.get_height() +
            spacing + separator + spacing +
            label_score.get_height() + self._score_surf.get_height() +
            padding * 2
            )
        box_x = self.screen.get_width() - box_width - 20
        box_y = 20
        box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA) # Fond principal semi-transparent
        
        for i in range(box_height):
            alpha = int(180 - (i / box_height) * 60) # Fond dégradé simulé avec plusieurs rectangles
            pygame.draw.line(box_surf, (60, 10, 120, alpha), (0, i), (box_width, i))
        pygame.draw.rect(box_surf, (255, 255, 255, 180), (0, 0, box_width, box_height), width=2, border_radius=12)
        self.screen.blit(box_surf, (box_x, box_y))
        sep_y = box_y + padding + label_best.get_height() + self._best_surf.get_height() + spacing# Ligne de séparation dorée au milieu
        pygame.draw.line(
            self.screen, (255, 200, 0, 80),
            (box_x + 10, sep_y),
            (box_x + box_width - 10, sep_y),
            1
        )
        cur_y = box_y + padding # Best score en haut
        label_x = box_x + (box_width - label_best.get_width()) // 2
        self.screen.blit(label_best, (label_x, cur_y))
        cur_y += label_best.get_height() + 2
        best_x = box_x + (box_width - self._best_surf.get_width()) // 2
        self.screen.blit(self._best_surf, (best_x, cur_y))
        cur_y = sep_y + spacing # Score en bas
        label_x = box_x + (box_width - label_score.get_width()) // 2
        self.screen.blit(label_score, (label_x, cur_y))
        cur_y += label_score.get_height() + 2
        score_x = box_x + (box_width - self._score_surf.get_width()) // 2
        self.screen.blit(self._score_surf, (score_x, cur_y))

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