# Gravity Runner

Projet de jeu 2D type "runner" en Python avec `pygame`.

## Equipe

- Téo MENUEL
- Papa Maguette DIOP
- Badr EL MJIYAD

## Aperçu

Le joueur avance automatiquement dans un monde en défilement horizontal.
Vous devez alterner la gravité pour rester sur les structures (haut, bas, milieu)
et éviter les obstacles.

## Prérequis

- Python 3.10 ou plus récent (3.11 recommandé)
- `pip`

## Dépendances

Le projet utilise une dépendance externe principale:

- `pygame`

Installation rapide:

```bash
pip install -r requirements.txt
```

Ou manuellement:

```bash
pip install pygame
```

## Installation (propre)

Depuis la racine du projet.

### Windows (PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Lancement du jeu

```bash
py main.py
```

Sur macOS/Linux, utilisez:

```bash
python3 main.py
```

## Contrôles

### Menu

- `Entrée`: lancer la partie
- `Échap`: quitter
- Clic sur le bouton bleu: modifier le nom

### En jeu

- `Espace` ou `Flèche Haut`: inverser la gravité (si le joueur touche une surface)
- `P`: pause / reprise
- `Échap`: retour au menu

## Structure du projet

```text
main.py                 # Boucle principale du jeu
code/
	game.py               # Etat global de partie
	world.py              # Génération et rendu des structures
	Player.py             # Logique du joueur
	Obstacle.py           # Types et effets d'obstacles
	ObstacleGenerator.py  # Spawn des obstacles
	lobby.py              # Menu
	interface.py          # HUD (score, pause, game over)
assets/
	Images/               # Sprites, obstacles, background, animations
```

## Notes

- Le jeu charge les assets depuis `assets/Images/...`.
- Si des images sont absentes, certains modules utilisent des surfaces de secours.
- La version courante de `pygame` testée localement est `2.6.x`.
