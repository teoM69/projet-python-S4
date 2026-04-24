import pygame

class Interface:
    def __init__(self, screen):
        self.screen = screen
        self.font_main = pygame.font.SysFont('Arial', 32)
        self.font_title = pygame.font.SysFont('Arial', 72, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 24)  # Nouvelle police pour les sous-titres
        
        self.color_white = (255, 255, 255)
        self.color_gold = (255, 215, 0)
        self.color_red = (250, 50, 50)
        self.overlay_color = (0, 0, 0, 150)  # Noir transparent

    def show_score(self, score):
        score_surf = self.font_main.render(f"Score: {score}", True, self.color_white) 
        self.screen.blit(score_surf, (25, 25))

    def show_best_score(self, best_score):
        best_surf = self.font_main.render(f"Best: {best_score}", True, self.color_gold)
        rect = best_surf.get_rect(topright=(self.screen.get_width() - 25, 25))
        self.screen.blit(best_surf, rect)

    def draw_overlay(self):
        """Ajoute un voile sombre derriere le texte de pause et de fin de partie."""
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill(self.overlay_color)
        self.screen.blit(overlay, (0, 0))

    def show_pause(self):
        self.draw_overlay()
        pause_surf = self.font_title.render("PAUSE", True, self.color_white)
        rect = pause_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        # Instruction supplementaire.
        hint_surf = self.font_small.render("Appuyez sur P pour reprendre", True, self.color_white)
        hint_rect = hint_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 60))
        
        self.screen.blit(pause_surf, rect)
        self.screen.blit(hint_surf, hint_rect)

    def show_game_over(self):
        self.draw_overlay()
        gameover_surf = self.font_title.render("GAME OVER", True, self.color_red)
        rect = gameover_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        
        hint_surf = self.font_small.render("Appuyez sur R pour rejouer", True, self.color_white)
        hint_rect = hint_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 60))
        
        self.screen.blit(gameover_surf, rect)
        self.screen.blit(hint_surf, hint_rect)