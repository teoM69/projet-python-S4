import os
import pygame
import sys


class Lobby:
    """Menu d'accueil du jeu Gravity Runner."""

    def __init__(self, screen, game):
        self.inMenu = True
        self.changingName = False
        self.name = "Joueur 1"
        self.game = game
        self.showError = False
        self.selected_mode = "solo"

        # Polices
        self.font_title = pygame.font.Font(None, 85)
        self.font_medium = pygame.font.Font(None, 50)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 24)

        self.menu_bg = self._load_menu_background(screen)
        self.menu_bg_scroll = 0.0

        # Animation
        self.cursor_visible = True
        self.cursor_timer = 0

    def _load_menu_background(self, screen):
        """Charge le fond principal (meme que le jeu) avec fallback robuste."""
        bg_path = os.path.join("assets", "Images", "BackGround.png")
        try:
            image = pygame.image.load(bg_path).convert()
            return pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
        except Exception:
            fallback = pygame.Surface((screen.get_width(), screen.get_height()))
            fallback.fill((12, 10, 28))
            return fallback

    def _draw_menu_background(self, screen):
        """Dessine le fond en defilement horizontal + voiles de lisibilite."""
        if self.menu_bg.get_size() != (screen.get_width(), screen.get_height()):
            self.menu_bg = pygame.transform.scale(self.menu_bg, (screen.get_width(), screen.get_height()))

        self.menu_bg_scroll = (self.menu_bg_scroll + 0.5) % max(1, screen.get_width())
        offset = int(self.menu_bg_scroll)
        screen.blit(self.menu_bg, (-offset, 0))
        screen.blit(self.menu_bg, (screen.get_width() - offset, 0))

        # Voile global
        shade = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        shade.fill((6, 8, 18, 160))
        screen.blit(shade, (0, 0))

    def run(self, screen, events):
        if not self.changingName:
            self._draw_main_menu(screen, events)
        else:
            self._draw_name_input(screen, events)

    def _draw_main_menu(self, screen, events):
        self._draw_menu_background(screen)
        mx, my = pygame.mouse.get_pos()

        # Panneau central
        panel_w, panel_h = 700, 480
        panel_rect = pygame.Rect((screen.get_width() - panel_w) // 2, (screen.get_height() - panel_h) // 2, panel_w, panel_h)

        # Dessin du panel (fond + bordure)
        pygame.draw.rect(screen, (8, 12, 24, 240), panel_rect, border_radius=20)
        pygame.draw.rect(screen, (96, 144, 230), panel_rect, width=2, border_radius=20)

        # --- TITRE ---
        title_surf = self.font_title.render("GRAVITY RUNNER", True, (248, 250, 255))
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, panel_rect.top + 60))
        screen.blit(title_surf, title_rect)

        subtitle = self.font_small.render("Pret pour le defi ?", True, (148, 243, 170))
        screen.blit(subtitle, subtitle.get_rect(center=(screen.get_width() // 2, panel_rect.top + 110)))

        # --- SECTION JOUEUR ---
        name_tag = self.font_tiny.render("PROFIL JOUEUR", True, (155, 172, 196))
        screen.blit(name_tag, (panel_rect.left + 50, panel_rect.top + 160))

        name_label = self.font_medium.render(f"{self.name}", True, (255, 255, 255))
        name_pos = (panel_rect.left + 50, panel_rect.top + 185)
        screen.blit(name_label, name_pos)

        # Bouton Modifier
        btn_edit_rect = pygame.Rect(panel_rect.right - 180, panel_rect.top + 180, 130, 40)
        is_hover_edit = btn_edit_rect.collidepoint(mx, my)
        color_btn = (42, 126, 234) if is_hover_edit else (22, 101, 206)
        pygame.draw.rect(screen, color_btn, btn_edit_rect, border_radius=8)
        edit_txt = self.font_tiny.render("MODIFIER", True, (255, 255, 255))
        screen.blit(edit_txt, edit_txt.get_rect(center=btn_edit_rect.center))

        # --- SECTION MODE DE JEU ---
        mode_title = self.font_small.render("SELECTION DU MODE", True, (180, 190, 210))
        screen.blit(mode_title, (panel_rect.left + 50, panel_rect.top + 260))

        solo_rect = pygame.Rect(panel_rect.left + 50, panel_rect.top + 290, 290, 60)
        duo_rect = pygame.Rect(panel_rect.right - 340, panel_rect.top + 290, 290, 60)

        for rect, mode, label in ((solo_rect, "solo", "SOLO"), (duo_rect, "duo", "DUO")):
            selected = self.selected_mode == mode
            hover = rect.collidepoint(mx, my)
            bg_color = (60, 140, 255) if selected else (30, 40, 60)
            if hover and not selected:
                bg_color = (45, 55, 80)

            pygame.draw.rect(screen, bg_color, rect, border_radius=12)
            pygame.draw.rect(screen, (100, 200, 255) if selected else (70, 80, 100), rect, width=2, border_radius=12)
            txt_surf = self.font_medium.render(label, True, (255, 255, 255))
            screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))

        # --- BAS DU PANNEAU (AIDE & START) ---
        help_text = "Controles: Espace (J1) | Haut ou Clic (J2)"
        help_surf = self.font_tiny.render(help_text, True, (150, 160, 180))
        screen.blit(help_surf, help_surf.get_rect(center=(screen.get_width() // 2, panel_rect.bottom - 90)))

        hint_play = self.font_small.render("Appuyez sur ENTREE pour demarrer", True, (200, 200, 200))
        screen.blit(hint_play, hint_play.get_rect(center=(screen.get_width() // 2, panel_rect.bottom - 50)))

        hint_exit = self.font_tiny.render("ECHAP pour quitter", True, (100, 110, 130))
        screen.blit(hint_exit, hint_exit.get_rect(center=(screen.get_width() // 2, panel_rect.bottom - 20)))

        # Gestion des interactions souris/clavier.
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_edit_rect.collidepoint(event.pos):
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
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def _draw_name_input(self, screen, events):
        """Ecran de saisie epure."""
        self._draw_menu_background(screen)

        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))

        # Curseur clignotant
        self.cursor_timer = (self.cursor_timer + 1) % 60
        cursor = "|" if self.cursor_timer < 30 else ""

        prompt = self.font_medium.render("Choisissez votre Pseudo", True, (255, 255, 255))
        screen.blit(prompt, prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 80)))

        name_surf = self.font_title.render(f"{self.name}{cursor}", True, (80, 200, 255))
        screen.blit(name_surf, name_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)))

        instr = self.font_small.render("Appuyez sur ENTREE pour valider", True, (150, 150, 150))
        screen.blit(instr, instr.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 80)))

        if self.showError:
            err = self.font_small.render("Le nom ne peut pas etre vide !", True, (255, 50, 50))
            screen.blit(err, err.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 100)))

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
