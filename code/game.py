from code.world import World

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.inGame = False
        self.gameSpeed = 5.0
        self.difficulty = 1.0
        self.score = 0
        self.bestScore = 0  # a modifier
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