import os
import pygame
import sys


class Lobby:
    """Menu d'accueil du jeu.

    Responsabilites:
    - afficher les options principales,
    - gerer la saisie du nom joueur,
    - lancer la partie en preparant les scores dans l'objet Game.
    """

    def __init__(self, screen, game):
        # Etat de navigation du lobby.
        self.inMenu = True
        self.changingName = False
        self.name = "Joueur 1"

        # Polices.
        self.font_title = pygame.font.Font(None, 80)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 36)

        self.game = game
    # Active l'affichage d'un message d'erreur si le pseudo est invalide.
        self.showError = False
    # Placeholder pour des variantes de jeu futures.
        self.selected_mode = "solo"

        self.menu_bg = self._load_menu_background(screen)

    def _load_menu_background(self, screen):
        """Charge le fond du lobby fourni par l'utilisateur avec fallback robuste."""
        bg_path = os.path.join("assets", "Images", "Menu-arriere-plan.png")
        try:
            image = pygame.image.load(bg_path).convert()
            return pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
        except Exception:
            fallback = pygame.Surface((screen.get_width(), screen.get_height()))
            fallback.fill((12, 10, 28))
            return fallback

    def _draw_menu_background(self, screen):
        """Dessine le fond puis un voile pour garantir la lisibilite du menu."""
        if self.menu_bg.get_size() != (screen.get_width(), screen.get_height()):
            self.menu_bg = pygame.transform.scale(self.menu_bg, (screen.get_width(), screen.get_height()))

        screen.blit(self.menu_bg, (0, 0))

        shade = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        shade.fill((6, 8, 18, 140))
        screen.blit(shade, (0, 0))

        top_band = pygame.Surface((screen.get_width(), 180), pygame.SRCALPHA)
        top_band.fill((20, 36, 62, 120))
        screen.blit(top_band, (0, 0))

        bottom_band = pygame.Surface((screen.get_width(), 130), pygame.SRCALPHA)
        bottom_band.fill((16, 12, 34, 110))
        screen.blit(bottom_band, (0, screen.get_height() - 130))

    def run(self, screen, events):
        """Met a jour et dessine le lobby pour la frame courante."""
        if not self.changingName:
            self._draw_main_menu(screen, events)
        else:
            self._draw_name_input(screen, events)

    def _draw_main_menu(self, screen, events):
        """Dessine le menu principal et traite les interactions de base.

        Elements principaux:
        - panneau central translucide,
        - titre du jeu,
        - section pseudo + bouton de modification,
        - consignes clavier.
        """
        # Fond image + voiles pour lisibilite.
        self._draw_menu_background(screen)

        for bubble_x, bubble_y, radius, color in (
            (120, 92, 78, (74, 122, 220)),
            (screen.get_width() - 140, 136, 64, (136, 94, 220)),
            (178, screen.get_height() - 118, 92, (74, 205, 180)),
        ):
            glow = pygame.Surface((radius * 2 + 16, radius * 2 + 16), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*color, 22), (radius + 8, radius + 8), radius)
            pygame.draw.circle(glow, (*color, 10), (radius + 8, radius + 8), radius + 8)
            screen.blit(glow, (bubble_x - radius - 8, bubble_y - radius - 8))

        # Panneau principal centré.
        panel_width, panel_height = 760, 500
        panel_rect = pygame.Rect(
            (screen.get_width() - panel_width) // 2,
            (screen.get_height() - panel_height) // 2 + 6,
            panel_width,
            panel_height,
        )

        # Surface alpha: fond + contour pour un rendu plus lisible.
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (8, 12, 24, 230), panel_surface.get_rect(), border_radius=28)
        pygame.draw.rect(panel_surface, (96, 144, 230, 255), panel_surface.get_rect(), width=3, border_radius=26)
        inner_rect = panel_surface.get_rect().inflate(-20, -20)
        pygame.draw.rect(panel_surface, (18, 24, 42, 195), inner_rect, border_radius=22)
        screen.blit(panel_surface, panel_rect.topleft)

        title_surf = self.font_title.render("GRAVITY RUNNER", True, (248, 250, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, panel_rect.top + 70))
        screen.blit(title_surf, title_rect)

        subtitle = self.font_small.render("Choisis ton mode puis lance la partie", True, (180, 190, 210))
        screen.blit(subtitle, subtitle.get_rect(center=(screen.get_width() // 2, panel_rect.top + 110)))

        name_tag = self.font_small.render("JOUEUR", True, (155, 172, 196))
        screen.blit(name_tag, name_tag.get_rect(center=(screen.get_width() // 2 - 120, panel_rect.top + 196)))

        name_label = self.font_medium.render(f"{self.name}", True, (255, 255, 255))
        name_label_rect = name_label.get_rect(center=(screen.get_width() // 2 - 80, panel_rect.top + 236))
        screen.blit(name_label, name_label_rect)

        btn_rect = pygame.Rect(name_label_rect.right + 20, name_label_rect.top - 2, 170, 50)
        pygame.draw.rect(screen, (22, 121, 226), btn_rect, border_radius=12)
        pygame.draw.rect(screen, (120, 184, 255), btn_rect, width=2, border_radius=12)
        btn_text = self.font_small.render("Changer", True, (255, 255, 255))
        screen.blit(btn_text, btn_text.get_rect(center=btn_rect.center))

        mode_title = self.font_medium.render("MODE DE JEU", True, (148, 243, 170))
        screen.blit(mode_title, mode_title.get_rect(center=(screen.get_width() // 2, panel_rect.top + 330)))

        solo_rect = pygame.Rect((screen.get_width() // 2) - 210, panel_rect.top + 368, 180, 58)
        duo_rect = pygame.Rect((screen.get_width() // 2) + 30, panel_rect.top + 368, 180, 58)
        solo_selected = self.selected_mode == "solo"
        duo_selected = self.selected_mode == "duo"

        pygame.draw.rect(screen, (28, 38, 62) if not solo_selected else (42, 126, 234), solo_rect, border_radius=14)
        pygame.draw.rect(screen, (28, 38, 62) if not duo_selected else (122, 70, 200), duo_rect, border_radius=14)
        pygame.draw.rect(screen, (120, 184, 255), solo_rect, width=2, border_radius=14)
        pygame.draw.rect(screen, (120, 184, 255), duo_rect, width=2, border_radius=14)

        solo_text = self.font_small.render("SOLO", True, (255, 255, 255))
        duo_text = self.font_small.render("DUO", True, (255, 255, 255))
        screen.blit(solo_text, solo_text.get_rect(center=solo_rect.center))
        screen.blit(duo_text, duo_text.get_rect(center=duo_rect.center))

        mode_help = self.font_small.render("Solo: Espace / Haut / clic   |   Duo: J1 Espace, J2 Haut / clic", True, (198, 205, 218))
        screen.blit(mode_help, mode_help.get_rect(center=(screen.get_width() // 2, panel_rect.top + 452)))

        hint_play = self.font_small.render("Appuyez sur ENTREE pour demarrer", True, (200, 200, 200))
        hint_exit = self.font_small.render("ECHAP pour quitter", True, (150, 150, 150))
        screen.blit(hint_play, hint_play.get_rect(center=(screen.get_width() // 2, panel_rect.bottom - 48)))
        screen.blit(hint_exit, hint_exit.get_rect(center=(screen.get_width() // 2, panel_rect.bottom - 18)))

        # Gestion des interactions souris/clavier.
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_rect.collidepoint(event.pos):
                    self.changingName = True
                elif solo_rect.collidepoint(event.pos):
                    self.selected_mode = "solo"
                elif duo_rect.collidepoint(event.pos):
                    self.selected_mode = "duo"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.name.strip() != "":
                        self.game.name = self.name
                        self.game.setScores()
                        self.inMenu = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def _draw_name_input(self, screen, events):
        """Dessine l'ecran de saisie du pseudo et traite la validation."""
        self._draw_menu_background(screen)
        # Overlay sombre pour focaliser la saisie.
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 220))
        screen.blit(overlay, (0, 0))

        prompt = self.font_medium.render("Entrez votre pseudo :", True, (255, 255, 255))
        screen.blit(prompt, prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 60)))

        name_surf = self.font_title.render(self.name + "|", True, (0, 255, 255))
        screen.blit(name_surf, name_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 20)))

        if self.showError:
            err = self.font_small.render("Le nom ne peut pas etre vide !", True, (255, 50, 50))
            screen.blit(err, err.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100)))

        # Validation clavier et saisie texte character-by-character.
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
                if len(self.name) < 12:
                    self.name += event.text
