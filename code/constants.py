# Constantes globales partagees par tous les modules du jeu.
# L'objectif est de centraliser le tuning gameplay et les valeurs de rendu.

# Cadence cible et garde-fous de normalisation frame-time.
TARGET_FPS = 60
FRAME_SCALE_MIN = 0.6
FRAME_SCALE_MAX = 1.8

# Geometrie de base des supports et des obstacles.
WALL_HEIGHT = 50
PLATFORM_BOTTOM_OFFSET = 165
OBSTACLE_DEFAULT_SIZE = (50, 50)
OBSTACLE_SPAWN_MIN_MS = 1200
OBSTACLE_SPAWN_MAX_MS = 3000
DEFAULT_OBSTACLE_SPEED = 5.0

# Etats de la machine de jeu principale.
STATE_MENU = "menu"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

# Tuning global de la sensation "runner".
GAME_SPEED_START = 5.0
GAME_SPEED_MAX = 12.0
# Courbe de vitesse: lente au debut puis accelere de plus en plus.
GAME_SPEED_RAMP_DURATION_SEC = 70.0
GAME_SPEED_RAMP_EXPONENT = 1.75
PLAYER_GRAVITY_SPEED = 5
SPAWN_MIN_FLOOR_MS = 550
SPAWN_MAX_FLOOR_MS = 1200

# Barreme de score: base temporelle + bonus dependant de la vitesse.
SCORE_BASE_PER_SEC = 12.0
SCORE_SPEED_BONUS_FACTOR = 1.8

# Parametres de generation des obstacles (position, espacement, variation).
OBSTACLE_SPEED_MULT_MIN = 0.85
OBSTACLE_SPEED_MULT_MAX = 1.2
OBSTACLE_SPAWN_X_OFFSET_MIN = 180
OBSTACLE_SPAWN_X_OFFSET_MAX = 320
OBSTACLE_SPAWN_GAP_MIN = 100
OBSTACLE_SPAWN_GAP_MAX = 180
OBSTACLE_WORLD_MIN_RIGHT_EDGE = 220

# Probabilites de tirage des types d'obstacles.
# Ordre: bomb, double_bomb, push1, push2.
OBSTACLE_TYPE_WEIGHTS = (0.38, 0.24, 0.19, 0.19)

# Parametres joueur: respawn, marges de securite et fenetre de switch.
PLAYER_RESPAWN_X = 100
PLAYER_OUT_OF_BOUNDS_MARGIN = 40
SWITCH_SUPPORT_SPAN_RATIO = 0.8
SWITCH_SUPPORT_SPAN_MAX = 32
SWITCH_SURFACE_TOLERANCE = 8
SWITCH_INPUT_BUFFER_MS = 120

# Gravite du joueur: lente au debut, puis accelere progressivement jusqu'au plafond.
PLAYER_GRAVITY_MAX = 8.5
PLAYER_GRAVITY_RAMP_DURATION_SEC = 65.0
PLAYER_GRAVITY_RAMP_EXPONENT = 1.6

# Delais d'affichage en fin de run.
GAME_OVER_DELAY_MS = 500
GAME_OVER_RETURN_LOBBY_MS = None