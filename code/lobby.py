import pygame

class Lobby:
    """
    Classe représentant le menu d'accueil (Lobby) du jeu.
    Gère l'affichage du menu, la modification du nom du joueur et la transition vers le jeu.
    """
    def __init__(self, screen):
        # État global du menu
        self.inMenu = True             # True tant qu'on est dans le menu, False pour lancer le jeu
        self.changingName = False      # True si le joueur est en train de taper son pseudo
        self.name = "test"             # Nom par défaut du joueur
        
        # Initialisation de la police d'écriture (taille 74)
        self.font = pygame.font.Font(None, 74)
        
        # Gestion des erreurs (ex: si le joueur tente de valider un nom vide)
        self.showError = False

    def run(self, screen, events):
        """
        Méthode appelée à chaque image (frame) pour mettre à jour et afficher le lobby.
        :param screen: La surface de la fenêtre Pygame où dessiner.
        :param events: La liste des événements Pygame (clavier, souris, etc.) de la frame actuelle.
        """
        
        # --- ÉTAT 1 : MENU PRINCIPAL ---
        # Le joueur n'est pas en train de modifier son nom
        if self.changingName == False:
            
            # --- Création et positionnement des textes ---
            # Affichage du nom actuel
            text_name = self.font.render("Nom: " + self.name, True, (255, 255, 255))
            text_name_rect = text_name.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 100))
            
            # Zone interactive (bouton bleu) placée à côté du nom pour le modifier
            change_name_rect = pygame.Rect(text_name_rect.right + 10, text_name_rect.top, 200, 50)

            # Instructions de jeu
            text_play = self.font.render("Entree pour jouer", True, (255, 255, 255))
            text_quit = self.font.render("Echap pour quitter", True, (255, 255, 255))
            
            # --- Dessin sur l'écran ---
            screen.blit(text_play, (screen.get_width() // 2 - 200, screen.get_height() // 2))
            screen.blit(text_quit, (screen.get_width() // 2 - 200, screen.get_height() // 2 + 100))
            screen.blit(text_name, text_name_rect)
            
            # Dessin du bouton pour changer de nom (un simple rectangle bleu pour l'instant)
            pygame.draw.rect(screen, "blue", change_name_rect)

            # --- Gestion des événements du menu principal ---
            for event in events:
                # Clic de souris (clic gauche = button 1)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Si on clique dans le rectangle bleu, on passe en mode "saisie de nom"
                    if change_name_rect.collidepoint(event.pos):
                        self.changingName = True
                
                # Touches du clavier
                if event.type == pygame.KEYDOWN:
                    # Touche 'Entrée' : on quitte le menu pour lancer le jeu
                    if event.key == pygame.K_RETURN:
                        self.inMenu = False
                    # Touche 'Échap' : on ferme complètement le jeu
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                        
        # --- ÉTAT 2 : SAISIE DU NOM ---
        # Le joueur est en train de taper son nouveau nom
        else:
            # --- Dessin de l'interface de saisie ---
            title = self.font.render("Entrez votre nom", True, (255, 255, 255))
            screen.blit(title, (screen.get_width() // 2 - 200, screen.get_height() // 2 - 100))
            
            # Affiche le nom en cours de frappe avec un curseur "|" à la fin
            name_input = self.font.render(self.name + "|", True, (0, 255, 255)) 
            screen.blit(name_input, (screen.get_width() // 2 - 200, screen.get_height() // 2))
            
            # Affichage du message d'erreur si l'utilisateur a essayé de valider un nom vide
            if self.showError:
                error = self.font.render("Nom vide interdit", True, (230, 23, 16)) # Rouge
                screen.blit(error, (screen.get_width() // 2, screen.get_height() // 2 + 200))
                
            # --- Gestion des événements de la saisie de texte ---
            for event in events:
                if event.type == pygame.KEYDOWN:
                    # Touche 'Entrée' pour valider le nouveau nom
                    if event.key == pygame.K_RETURN:
                        if self.name != "": # Le nom est valide
                            self.showError = False
                            self.changingName = False # Retour au menu principal
                        else: # Le nom est vide, on déclenche l'erreur
                            self.showError = True
                            
                    # Touche 'Retour arrière' (Backspace) pour effacer le dernier caractère
                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1] # Retire la dernière lettre de la chaîne
                        
                # Événement de saisie de texte (gère automatiquement les majuscules, caractères spéciaux, etc.)
                if event.type == pygame.TEXTINPUT:
                    self.name += event.text # Ajoute le caractère tapé à la fin du nom