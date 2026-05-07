import pygame

"""Gestion audio du jeu.

Centralise:
- la musique de fond (boucle),
- les effets sonores gameplay (switch gravite, collision, game over),
- l'activation/desactivation rapide de la musique.
"""


class Sound:
    """Facade audio utilisee par la boucle principale."""
    def __init__(self):
        # Initialise le mixer Pygame une seule fois a la creation du gestionnaire.
        pygame.mixer.init()

        # Etat logique de la musique de fond (utile pour l'option mute).
        self.backgroundMusicOn = True

        # Charge les sons courts en memoire (latence de lecture minimale).
        try:
            self.game_over_sfx = pygame.mixer.Sound("assets/Sounds/sound.gameover.mp3")
            self.gravity_sfx = pygame.mixer.Sound("assets/Sounds/sound.gravity.mp3")
            self.obstacle_sfx = pygame.mixer.Sound("assets/Sounds/sound.obstacle.mp3")
        except pygame.error as e:
            print(f"Erreur lors du chargement des sons : {e}") # Affiche une erreur mais continue l'execution pour permettre de jouer sans son si

        # Charge la piste longue de fond via pygame.mixer.music (streaming).
        try:
            pygame.mixer.music.load("assets/Sounds/sound.background.mp3")
        except pygame.error as e:
            print(f"Erreur lors du chargement de la musique : {e}")
            
   
    def playBackgroundMusic(self):
        """Lance la musique en boucle infinie si elle est active."""
        # -1 signifie boucle infinie.
        if self.backgroundMusicOn:
            pygame.mixer.music.play(-1)

    def stopBackgroundMusic(self):
        """Arrete immediatement la musique de fond."""
        pygame.mixer.music.stop()


    def playGameOverSound(self):
        """Joue l'effet sonore de fin de partie."""
        self.game_over_sfx.play()

    def playGravitySwitchSound(self):
        """Joue le feedback sonore du changement de gravite."""
        self.gravity_sfx.play()

    def playObstacleSound(self):
        """Joue l'effet sonore de collision/impact obstacle."""
        self.obstacle_sfx.play()


    def toggleMusic(self): 
        """Bascule l'etat musique ON/OFF et applique immediatement le changement."""
        self.backgroundMusicOn = not self.backgroundMusicOn 
        if not self.backgroundMusicOn:
            self.stopBackgroundMusic()
        else:
            self.playBackgroundMusic()
