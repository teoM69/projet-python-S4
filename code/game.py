from code.world import World
import json
import os

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.inGame = False
        self.gameSpeed = 5.0
        self.difficulty = 1.0
        self.score = 0
        self.name = ""
        self.bestScore = 0
        self.personalBest = 0
        self.contactObstacleType = ""
        
        self.world = World(5, self.screen.get_width(), self.screen.get_height())
    def start(self):
        # Demarrer ou redemarrer
        self.inGame = True
        self.score = 0
        self.difficulty = 1.0
        self.gameSpeed = 5.0
        # self.player.spawn()
        # self.world.obstacles = []
        # self.sounds.playBackgroundMusic()
    def end(self):
        if self.score > self.bestScore:
            self.bestScore = self.score  # a modifier

    def loadFile(self):
        if not os.path.exists("scores.json"):
            return {"global_best": 0, "personal_bests": {}}
        with open("scores.json", "r") as f:
            return json.load(f)

    def getBestScore(self, data):
        return data["global_best"]
    
    def getPersonalbest(self, data):
        return data["personal_bests"].get(self.name, 0)
    
    def setScores(self):
       data = self.loadFile()
       self.bestScore = self.getBestScore(data)
       self.personalBest = self.getPersonalbest(data)
       print(self.personalBest)