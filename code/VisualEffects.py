import pygame

class VisualEffects:
        def __init__():
           
        def list(self, effect, x, y, screen):
            return effect
             
              
        def CreateEffect(self, effect, x, y, screen):
            if effect == "explosion":
                explosion_image = pygame.image.load("assets/explosion.png")
                explosion_rect = explosion_image.get_rect(center=(x, y))
                screen.blit(explosion_image, explosion_rect)
             
       def DeleteEffect(self, effect):
            del effect