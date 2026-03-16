import pygame 

class Interface:
     def __init__(self, screen):
            self.screen = screen
            self.font_main = pygame.font.SysFont('Arial', 32)
            self.font_title = pygame.font.SysFont('Arial', 72, bold=True)
            self.color_white = (255, 255, 255)
            self.color_gold = (255, 215, 0)
            self.color_red = (250, 50, 50)
            
     def show_score(self, score):
              score_surf = self.font_main.render(f"Score:{score}", True, self.color_white) 
              self.screen.blit(score_surf,(25,25))
              print("score") 
              
     def show_best_score(self, best_score):
              best_surf = self.font_main.render(f"Best: {best_score}", True, self.color_gold)
              rect = best_surf.get_rect(topright=(self.screen.get_width() - 25, 25))
              self.screen.blit(best_surf, rect)
              print("best score")

     def show_pause(self):
              pause_surf = self.font_title.render("PAUSE", True, self.color_white)
              rect = pause_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
              self.screen.blit(pause_surf, rect)
              print("pause")
    
     def show_game_over(self):
             gameover_surf = self.font_title.render("GAME OVER", True, self.color_red)
             rect = gameover_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
             self.screen.blit(gameover_surf, rect)
             print("game over")
             