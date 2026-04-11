import pygame

class Player:
    def __init__(self, nom, x, y):
        self.nom = nom
        self.gravity_direction = 1  # 1 = normal, -1 = inversé
        self.gravity_speed = 5
        self.is_flipping = False
        self.playerPosition = pygame.Vector2(x, y)
        
        # --- Chargement des images ---
        # Note : Remplace 'imgX.png' par tes vrais noms de fichiers
        self.walk_normal = [pygame.image.load(f"walk1.png"), pygame.image.load(f"walk2.png"), pygame.image.load(f"walk3.png")]
        self.walk_inverted = [pygame.image.load(f"inv1.png"), pygame.image.load(f"inv2.png"), pygame.image.load(f"inv3.png")]
        self.flip_imgs = [pygame.image.load(f"flip1.png"), pygame.image.load(f"flip2.png")]
        
        self.current_image = self.walk_normal[0]
        self.anim_index = 0
        self.anim_timer = 0

    def switchGravity(self):
        # On change la direction et on lance l'animation de salto
        self.gravity_direction *= -1
        self.is_flipping = True
        self.anim_index = 0 # Recommence l'animation au début

    def mov(self):
        # 1. Gestion du timing de l'animation
        self.anim_timer += 1
        if self.anim_timer > 10: # Ajuste ce chiffre pour ralentir/accélérer l'animation
            self.anim_index += 1
            self.anim_timer = 0

        # 2. Logique visuelle (Quelle image afficher ?)
        if self.is_flipping:
            # Animation de Salto (2 images)
            if self.anim_index >= len(self.flip_imgs):
                self.is_flipping = False # Salto terminé
                self.anim_index = 0
            else:
                self.current_image = self.flip_imgs[self.anim_index]
        
        elif self.gravity_direction == 1:
            # Marche Normale (3 images)
            self.anim_index %= len(self.walk_normal)
            self.current_image = self.walk_normal[self.anim_index]
            
        elif self.gravity_direction == -1:
            # Marche Inversée (3 images)
            self.anim_index %= len(self.walk_inverted)
            self.current_image = self.walk_inverted[self.anim_index]

        # 3. Application du mouvement physique
        self.playerPosition.y += (self.gravity_speed * self.gravity_direction)

    def draw(self, screen):
        # Pour afficher le joueur sur l'écran
        screen.blit(self.current_image, self.playerPosition)

    def die(self):
        print("die")
    
    def spawn(self):
        print("spawn")
       