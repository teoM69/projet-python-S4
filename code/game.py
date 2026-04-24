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

    def loadFile(self):
        if not os.path.exists("scores.json"):
            return {"global_best": 0, "personal_bests": {}}
        with open("scores.json", "r") as f:
            return json.load(f)
        
    def saveScores(self, data):
        with open("scores.json", "w") as f:
            json.dump(data, f, indent=4)

    def end(self):
        data = self.loadFile()
        has_changed = False
        if self.score > self.bestScore:
            data["global_best"] = self.score
            self.bestScore = self.score
            has_changed = True
        if self.score > self.personalBest:
            data["personal_bests"][self.name] = self.score
            self.personalBest = self.score
            has_changed = True
        if has_changed:
            self.saveScores(data)

    def getBestScore(self, data):
        return data["global_best"]
    
    def getPersonalbest(self, data):
        return data["personal_bests"].get(self.name, 0)
    
    def setScores(self):
       data = self.loadFile()
       self.bestScore = self.getBestScore(data)
       self.personalBest = self.getPersonalbest(data)
       print(self.personalBest)