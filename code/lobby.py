import pygame


class Lobby:
    """Menu d'accueil du jeu.

    Responsabilites:
    - afficher les options principales,
    - gerer la saisie du nom joueur,
    - lancer la partie en preparant les scores dans l'objet Game.
    """

    def __init__(self, screen, game):
        # Etat global du menu.
        self.inMenu = True
        self.changingName = False
        self.name = "test"

        # Ressource d'affichage des textes.
        self.font = pygame.font.Font(None, 74)

        # Affichage conditionnel d'un message d'erreur (nom vide).
        self.showError = False

        # Reference au coeur de jeu pour synchroniser nom + scores.
        self.game = game

    def run(self, screen, events):
        """Met a jour et dessine le lobby pour la frame courante."""

        # ETAT 1: menu principal.
        if self.changingName is False:
            # Texte du nom courant et zone cliquable pour edition.
            text_name = self.font.render("Nom: " + self.name, True, (255, 255, 255))
            text_name_rect = text_name.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
            change_name_rect = pygame.Rect(text_name_rect.right + 10, text_name_rect.top, 200, 50)

            # Raccourcis disponibles.
            text_play = self.font.render("Entree pour jouer", True, (255, 255, 255))
            text_quit = self.font.render("Echap pour quitter", True, (255, 255, 255))

            # Rendu des textes et du bouton bleu de changement de nom.
            screen.blit(text_play, (screen.get_width() // 2 - 200, screen.get_height() // 2))
            screen.blit(text_quit, (screen.get_width() // 2 - 200, screen.get_height() // 2 + 100))
            screen.blit(text_name, text_name_rect)
            pygame.draw.rect(screen, "blue", change_name_rect)

            # Gestion des interactions du menu principal.
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if change_name_rect.collidepoint(event.pos):
                        self.changingName = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Valide le nom et prepare les records avant de lancer la run.
                        self.game.name = self.name
                        self.game.setScores()
                        self.inMenu = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        # ETAT 2: edition du nom.
        else:
            title = self.font.render("Entrez votre nom", True, (255, 255, 255))
            screen.blit(title, (screen.get_width() // 2 - 200, screen.get_height() // 2 - 100))

            # Curseur textuel minimaliste avec suffixe "|".
            name_input = self.font.render(self.name + "|", True, (0, 255, 255))
            screen.blit(name_input, (screen.get_width() // 2 - 200, screen.get_height() // 2))

            if self.showError:
                error = self.font.render("Nom vide interdit", True, (230, 23, 16))
                screen.blit(error, (screen.get_width() // 2, screen.get_height() // 2 + 200))

            # Gestion de la saisie texte.
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.name != "":
                            self.showError = False
                            self.changingName = False
                        else:
                            self.showError = True

                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]

                if event.type == pygame.TEXTINPUT:
                    self.name += event.text
