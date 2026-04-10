import pygame


class Player:
      def __init__(self, nom, y, x):
            self.nom = nom
            self.gravity = 5
            self.isStucked = False
            # store position as Vector2(x, y)
            self.playerPosition = pygame.Vector2(x, y)
            # basic size for collision
            self.width = 40
            self.height = 40
            self.alive = True
            # rect for collisions; keep in sync by calling update_rect()
            self.rect = pygame.Rect(int(self.playerPosition.x), int(self.playerPosition.y), self.width, self.height)

      def update_rect(self):
            self.rect.topleft = (int(self.playerPosition.x), int(self.playerPosition.y))

      def take_damage(self, amount=1):
            # simple implementation: any damage kills player
            self.alive = False

      def set_gravity(self, value):
            self.gravity = value

      def die(self):
            print("Player died")

      def spawn(self, x, y):
            self.playerPosition = pygame.Vector2(x, y)
            self.update_rect()

      def switchGravity(self):
            self.gravity = -self.gravity