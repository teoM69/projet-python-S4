"""Gestion du mode campagne.

Ce module decrit une suite de niveaux a difficulte croissante.
Chaque niveau fournit ses parametres de gameplay (vitesse, acceleration,
densite de spawn) et un objectif de score a atteindre.
"""

class Level:
    """Conteneur de configuration pour un niveau de campagne."""
    def __init__(self, index, name, speed_start, speed_max, accel_per_frame, spawn_scale, world_difficulty_boost, target_score):
        # Index humain (1, 2, 3...) et libelle affiche dans l'UI.
        self.index = index
        self.name = name

        # Bornes de vitesse du niveau.
        self.speed_start = speed_start
        self.speed_max = speed_max

        # Facteur d'acceleration applique a chaque frame.
        self.accel_per_frame = accel_per_frame

        # Multiplicateur de frequence de spawn (plus petit => plus frequent).
        self.spawn_scale = spawn_scale

        # Ajustement de difficulte procedurale du monde (plateformes, gaps, etc.).
        self.world_difficulty_boost = world_difficulty_boost

        # Score minimal a atteindre pour valider le niveau.
        self.target_score = target_score

class CampaignMode:
    """Machine d'etat du mode campagne.

    Elle maintient le niveau courant, le score cumule de la campagne et
    expose des utilitaires pour reset/progression.
    """
    def __init__(self):
        # Progression ordonnee de la campagne (du plus simple au plus difficile).
        self.levels = [
            Level(1, "Éveil", 5.0, 7.0, 0.005, 1.2, 0.0, 100),
            Level(2, "Intermediaire", 6.0, 9.0, 0.006, 1.0, 0.1, 500),
            Level(3, "Expert", 8.0, 12.0, 0.008, 0.8, 0.2, 1000)
        ]
        # Index du niveau actif et compteur global de score campagne.
        self.current_level_idx = 0
        self.total_score = 0

    @property
    def current_level(self):
        """Retourne l'objet niveau actuellement joue."""
        return self.levels[self.current_level_idx]

    def reset(self):
        """Relance la campagne depuis le premier niveau."""
        self.current_level_idx = 0
        self.total_score = 0

    def advance_level(self):
        """Passe au niveau suivant.

        Retourne True s'il existe encore un niveau a jouer, sinon False.
        """
        self.current_level_idx += 1
        return self.current_level_idx < len(self.levels)

    def add_level_score(self, score):
        """Ajoute le score du niveau termine au total campagne."""
        self.total_score += score