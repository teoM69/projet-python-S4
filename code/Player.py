import pygame

class Player:
        def __init__(self, nom, y, x):
            self.nom = nom
            self.gravity = 5
            self.isStucked = False
            self.playerPosition = pygame.Vector2(x, y)
        def die():
              print("die") 
              
        def spawn():
              print("spawn")
        def switchGravity():
              print("switchGravity")