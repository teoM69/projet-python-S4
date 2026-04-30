import pygame

class Sound:
    def __init__(self):
        pygame.mixer.init()
        self.backgroundMusicOn = True
        try:
            self.game_over_sfx = pygame.mixer.Sound("sound.gameover.wav")
            self.gravity_sfx = pygame.mixer.Sound("sound.gravity.wav")
            self.obstacle_sfx = pygame.mixer.Sound("sound.obstacle.wav")
        except pygame.error as e:
            print(f"Erreur lors du chargement des sons : {e}")
# Remplacer les noms de fichiers par tes propres chemins
# Chargement de la musique (on utilise music car c'est plus léger pour les longs fichiers)
        try:
            pygame.mixer.music.load("sound.background.wav")
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
