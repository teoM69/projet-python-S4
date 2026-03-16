import pygame

class Lobby:
        def __init__(self, screen):
             self.inMenu = true
        def run(self, screen):            
             while   self.inMenu:
                  for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                              self.inMenu = false
                              self.quitGame(screen)
                        if event.type == pygame.KEYDOWN:
                              if event.key == pygame.K_RETURN:
                                    self.inMenu = false
                                    self.launchGame(screen)
        def showMenu(self, screen):
            # Affiche le menu de jeu
            font = pygame.font.Font(None, 74)
            text = font.render("Appuyez sur Entrée pour jouer", True, (255, 255, 255))
            text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
              
            
        def launchGame(self, screen):
            # Lancer le jeu principal
            pass  # Remplacez par le code pour démarrer le jeu
              
    
        def quitGame(self, screen):
            # Quitter le jeu
            pygame.quit()
            exit()
            