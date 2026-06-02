"""Systeme de combo pour augmenter le score quand le joueur survit sans erreur.

Le combo augmente progressivement pendant que le joueur evite les obstacles,
et se reinitialise quand le joueur subit une collision.
"""

from code.constants import (
    COMBO_THRESHOLD_SEC,
    COMBO_MULTIPLIER_BASE,
    COMBO_MULTIPLIER_MAX,
    COMBO_MULTIPLIER_INCREMENT,
    COMBO_LEVEL_MAX,
)


class ComboSystem:
    """Gere le systeme de combo et le multiplicateur de score associe."""
    
    def __init__(self):
        """Initialise le systeme de combo."""
        self.combo_level = 0  # Niveau de combo courant (0-20)
        self.time_since_last_hit = 0.0  # Temps en secondes depuis la derniere collision
        self.has_hit_this_frame = False  # Flag pour detecter une collision dans le frame courant
        self.total_combo_hits = 0  # Nombre total de fois que le combo a ete resetee
    
    def reset(self):
        """Remet le combo a zero (utilisee au demarrage d'une run)."""
        self.combo_level = 0
        self.time_since_last_hit = 0.0
        self.total_combo_hits = 0
        self.has_hit_this_frame = False
    
    def on_obstacle_hit(self):
        """Appele quand le joueur se cogne contre un obstacle."""
        self.has_hit_this_frame = True
    
    def update(self, delta_time_ms):
        """Met a jour le combo a chaque frame.
        
        Args:
            delta_time_ms: Temps ecoule depuis le dernier frame en millisecondes.
        """
        delta_time_s = delta_time_ms / 1000.0
        
        if self.has_hit_this_frame:
            # Reset le combo si on s'est cogne contre un obstacle ce frame
            if self.combo_level > 0:
                self.total_combo_hits += 1
            self.combo_level = 0
            self.time_since_last_hit = 0.0
            self.has_hit_this_frame = False
        else:
            # Incremente le temps depuis la derniere collision
            self.time_since_last_hit += delta_time_s
            
            # Incremente le combo si assez de temps s'est ecoule sans collision
            if self.time_since_last_hit >= COMBO_THRESHOLD_SEC and self.combo_level < COMBO_LEVEL_MAX:
                self.combo_level += 1
                self.time_since_last_hit = 0.0
    
    def get_score_multiplier(self) -> float:
        """Retourne le multiplicateur de score actuel (1.0 a 3.0)."""
        multiplier = COMBO_MULTIPLIER_BASE + (self.combo_level * COMBO_MULTIPLIER_INCREMENT)
        return min(multiplier, COMBO_MULTIPLIER_MAX)
    
    def get_combo_percentage(self) -> float:
        """Retourne le pourcentage du combo courant (0.0 a 1.0) pour l'affichage."""
        if COMBO_LEVEL_MAX == 0:
            return 1.0
        return min(self.combo_level / COMBO_LEVEL_MAX, 1.0)
