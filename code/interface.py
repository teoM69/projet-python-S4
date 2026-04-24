import pygame

class Interface:
    def __init__(self, screen):
        self.screen = screen
        self.font_main = pygame.font.SysFont('Arial', 32)
        self.font_title = pygame.font.SysFont('Arial', 72, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 24)
        
        self.color_white = (255, 255, 255)
        self.color_gold = (255, 215, 0)
        self.color_red = (250, 50, 50)
        self.overlay_color = (0, 0, 0, 150)

        self._cached_score = None
        self._cached_best = None
        self._score_surf = None
        self._best_surf = None
        self._best_rect = None

        self._overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self._overlay.fill(self.overlay_color)

        self._message_cache = {}

    def show_score(self, score, best_score):
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
        self.screen.blit(self._overlay, (0, 0))

    def show_message(self, title, hint, color):
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
        self.show_message("PAUSE", "Appuyez sur P pour reprendre", self.color_white)

    def show_game_over(self):
        self.show_message("GAME OVER", "Appuyez sur R pour rejouer", self.color_red)