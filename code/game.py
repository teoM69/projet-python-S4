from code.world import World
import json
import os


class Game:
    """Etat global d'une partie.

    Cette classe centralise les variables de progression (score, vitesse, nom du
    joueur) et la persistance des meilleurs scores.
    """
    def __init__(self, screen):
        # Surface principale utilisee par le jeu.
        self.screen = screen

        # Etats runtime.
        self.inGame = False
        self.gameSpeed = 5.0
        self.difficulty = 1.0
        self.score = 0

        # Donnees joueur et scores.
        self.name = ""
        self.bestScore = 0
        self.personalBest = 0
        self.contactObstacleType = ""

        # Monde de jeu (plateformes et ambiance).
        self.world = World(5, self.screen.get_width(), self.screen.get_height())

    def start(self):
        """Demarre une nouvelle run en reinitialisant les compteurs de session."""
        # Demarrer ou redemarrer.
        self.inGame = True
        self.score = 0
        self.difficulty = 1.0
        self.gameSpeed = 5.0
        # self.player.spawn()
        # self.world.obstacles = []
        # self.sounds.playBackgroundMusic()

    def loadFile(self):
        """Charge le fichier de scores, ou renvoie une structure par defaut."""
        if not os.path.exists("scores.json"):
            return {"global_best": 0, "personal_bests": {}}
        with open("scores.json", "r") as f:
            return json.load(f)

    def saveScores(self, data):
        """Ecrit les meilleurs scores sur disque avec une indentation lisible."""
        
        with open("scores.json", "w") as f:
            json.dump(data, f, indent=4)

    def end(self):
        """Termine la partie et persiste les records battus si necessaire."""
        data = self.loadFile()
        # Mise a jour du meilleur score global.
        if self.score > self.bestScore:
            data["global_best"] = self.score
            self.bestScore = self.score

        # Mise a jour du meilleur score personnel pour le nom courant.
        if self.score > self.personalBest:
            data["personal_bests"][self.name] = self.score
            self.personalBest = self.score

        data["last_name"] = self.name
        self.saveScores(data)

    def getBestScore(self, data):
        """Extrait le meilleur score global depuis la structure de persistance."""
        return data["global_best"]

    def getPersonalbest(self, data):
        """Extrait le record du joueur courant, ou 0 si absent."""
        return data["personal_bests"].get(self.name, 0)

    def setScores(self):
       """Recharge les scores courant depuis le fichier persistant."""
       data = self.loadFile()
       self.bestScore = self.getBestScore(data)
       self.personalBest = self.getPersonalbest(data)
       print(self.personalBest)