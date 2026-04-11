Player / Obstacle API (minimal)

Player (ce que les obstacles peuvent appeler / lire)
- `rect` : pygame.Rect — zone de collision du joueur
- `alive` : bool — True si le joueur est vivant
- `take_damage(amount)` : méthode pour appliquer des dégâts (peut tuer)
- `set_gravity(value)` : méthode pour régler la gravité (positive/negative)
- `update_rect()` : mettre à jour `rect` à partir de la position interne

Obstacle (ce que le moteur/appelant utilisera)
- `__init__(x, y, type, speed=0)` : constructeur
- `image` : surface utilisée pour le dessin
- `rect` : pygame.Rect utilisé pour collisions
- `update(speed=None)` : met à jour position (déplacement)
- `draw(surface)` : dessine l'obstacle
- `apply_effect(player)` : applique l'effet au `player` lors d'une collision

Conventions
- Les modules doivent charger les images à partir de `assets/Images/...`
- Ne modifiez pas les signatures publiques ci‑dessus sans prévenir l'équipe
