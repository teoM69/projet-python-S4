import pygame
import sys

class Lobby:
    def __init__(self, screen, game):
        self.inMenu = True
        self.changingName = False
        self.name = "Joueur 1"
        
        # Polices
        self.font_title = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 36)
        self.game = game
        
        self.showError = False
        self.selected_mode = "arcade" # Mode par défaut

    def run(self, screen, events):
        if not self.changingName:
            self._draw_main_menu(screen, events)
        else:
            self._draw_name_input(screen, events)

    def _draw_main_menu(self, screen, events):
        # 1. Dessin du Panneau Central
        panel_width, panel_height = 700, 500
        panel_rect = pygame.Rect(
            (screen.get_width() - panel_width) // 2,
            (screen.get_height() - panel_height) // 2,
            panel_width,
            panel_height
        )
        
        # Surface avec transparence (Alpha)
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (12, 16, 30, 200), panel_surface.get_rect(), border_radius=20)
        pygame.draw.rect(panel_surface, (94, 138, 208, 255), panel_surface.get_rect(), width=3, border_radius=20)
        screen.blit(panel_surface, panel_rect.topleft)

        # 2. Titre
        title_surf = self.font_title.render("GRAVITY RUNNER", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, panel_rect.top + 60))
        screen.blit(title_surf, title_rect)

        # 3. Section Pseudo
        name_label = self.font_medium.render(f"Nom: {self.name}", True, (255, 255, 255))
        name_label_rect = name_label.get_rect(center=(screen.get_width() // 2 - 60, panel_rect.top + 180))
        screen.blit(name_label, name_label_rect)

        # Bouton "Modifier"
        btn_rect = pygame.Rect(name_label_rect.right + 20, name_label_rect.top - 5, 140, 50)
        pygame.draw.rect(screen, (0, 102, 204), btn_rect, border_radius=10)
        btn_text = self.font_small.render("Changer", True, (255, 255, 255))
        screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

        # 4. Mode de jeu (Fixé sur Survie pour l'instant)
        mode_text = self.font_medium.render("MODE : SURVIE", True, (148, 243, 170))
        screen.blit(mode_text, mode_text.get_rect(center=(screen.get_width() // 2, panel_rect.top + 300)))

        # 5. Instructions en bas
        hint_play = self.font_small.render("Appuyez sur ENTREE pour démarrer", True, (200, 200, 200))
        hint_exit = self.font_small.render("ECHAP pour quitter", True, (150, 150, 150))
        screen.blit(hint_play, hint_play.get_rect(center=(screen.get_width() // 2, panel_rect.bottom - 80)))
        screen.blit(hint_exit, hint_exit.get_rect(center=(screen.get_width() // 2, panel_rect.bottom - 40)))

        # 6. Gestion des événements du menu
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_rect.collidepoint(event.pos):
                    self.changingName = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.name.strip() != "":
                        self.inMenu = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def _draw_name_input(self, screen, events):
        # Fond sombre pour la saisie
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0,0))

        prompt = self.font_medium.render("Entrez votre pseudo :", True, (255, 255, 255))
        screen.blit(prompt, prompt.get_rect(center=(screen.get_width()//2, screen.get_height()//2 - 60)))

        # Affichage du texte en cours de saisie
        name_surf = self.font_title.render(self.name + "|", True, (0, 255, 255))
        screen.blit(name_surf, name_surf.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 20)))

        if self.showError:
            err = self.font_small.render("Le nom ne peut pas être vide !", True, (255, 50, 50))
            screen.blit(err, err.get_rect(center=(screen.get_width()//2, screen.get_height()//2 + 100)))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.name.strip() != "":
                        self.changingName = False
                        self.showError = False
                    else:
                        self.showError = True
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
            elif event.type == pygame.TEXTINPUT:
                # Limite à 12 caractères pour pas que ça dépasse
                if len(self.name) < 12:
                    self.name += event.text