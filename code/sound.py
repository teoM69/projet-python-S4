import pygame
# Cette classe gère les sons du jeu, y compris la musique de fond et les effets sonores pour les différentes actions (changement de gravité, collision avec des obstacles, fin de partie).
class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.backgroundMusicOn = True
        try:
            self.game_over_sfx = pygame.mixer.Sound("assets/Sounds/sound.gameover.mp3")
            self.gravity_sfx = pygame.mixer.Sound("assets/Sounds/sound.gravity.mp3")
            self.obstacle_sfx = pygame.mixer.Sound("assets/Sounds/sound.obstacle.mp3")
        except pygame.error as e:
            print(f"Erreur lors du chargement des sons : {e}")
# Remplacer les noms de fichiers par tes propres chemins
# Chargement de la musique (on utilise music car c'est plus léger pour les longs fichiers)
        try:
            pygame.mixer.music.load("assets/Sounds/sound.background.mp3")
        except pygame.error as e:
            print(f"Erreur lors du chargement de la musique : {e}")
            
   
    def playBackgroundMusic(self):
        if self.backgroundMusicOn:# -1 signifie que la musique boucle à l'infini
            pygame.mixer.music.play(-1)

    def stopBackgroundMusic(self):
        pygame.mixer.music.stop()


    def playGameOverSound(self):
        self.game_over_sfx.play()

    def playGravitySwitchSound(self):
        self.gravity_sfx.play()

    def playObstacleSound(self):
        self.obstacle_sfx.play()


    def toggleMusic(self):
        self.backgroundMusicOn = not self.backgroundMusicOn
        if not self.backgroundMusicOn:
            self.stopBackgroundMusic()
        else:
            self.playBackgroundMusic()
