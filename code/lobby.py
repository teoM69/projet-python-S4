import pygame

class Lobby:
        def __init__(self, screen):
             self.inMenu = True
        def run(self, screen):            
             while   self.inMenu:
                  for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.inMenu = False
                            self.quitGame(screen)
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                self.inMenu = False
                            if event.key == pygame.K_ESCAPE:
                                 self.quitGame()
        def showMenu(self, screen):
            font = pygame.font.Font(None, 74)
            text1 = font.render("Appuyez sur Entrée pour jouer", True, (255, 255, 255))
            text2 = font.render("Echap pour quitter", True, (255, 255, 255))
            text1_rect = text1.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 30))
            text2_rect = text2.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 30))
            screen.blit(text1, text1_rect)
            screen.blit(text2, text2_rect)
            pygame.display.flip()
    
        def quitGame(self):
            pygame.quit()
            exit()
