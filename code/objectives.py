"""Missions secondaires de run.

Chaque partie choisit une mission parmi une petite liste de défis cohérents :
- survivre un certain temps,
- esquiver un nombre d'obstacles,
- faire une série d'esquives sans toucher d'obstacle.
"""

from dataclasses import dataclass
import random


@dataclass
class SecondaryObjective:
    """Modele d'une mission secondaire pour une run.

    Attributs:
    - title: intitule court affiche dans l'UI.
    - description: consigne lisible pour le joueur.
    - kind: type de logique de progression (temps, obstacles, etc.).
    - target: objectif numerique a atteindre.
    - reward: bonus de score attribue a la validation.
    - progress: progression courante de la mission.
    - completed/failed: etat final de la mission.
    - reward_claimed: evite de donner la recompense plusieurs fois.
    """
    title: str
    description: str
    kind: str
    target: int
    reward: int
    progress: int = 0
    completed: bool = False
    failed: bool = False
    reward_claimed: bool = False

    def update_elapsed(self, elapsed_seconds):
        """Met a jour la progression des objectifs bases sur le temps de survie."""
        if self.kind != "survive_time" or self.completed or self.failed:
            return
        self.progress = min(self.target, int(elapsed_seconds))
        if elapsed_seconds >= self.target:
            self.completed = True

    def register_obstacles_passed(self, count):
        """Incremente la progression des objectifs d'esquive d'obstacles."""
        if self.kind != "pass_obstacles" or self.completed or self.failed:
            return
        self.progress = min(self.target, self.progress + max(0, count))
        if self.progress >= self.target:
            self.completed = True

    def consume_reward(self):
        """Retourne la recompense une seule fois une fois l'objectif valide."""
        if self.completed and not self.reward_claimed:
            self.reward_claimed = True
            return self.reward
        return 0

    def status_label(self):
        """Renvoie le libelle d'etat a afficher dans l'interface."""
        if self.completed:
            return "Reussie"
        if self.failed:
            return "Ratee"
        return "En cours"

    def progress_label(self):
        """Formate la progression selon le type de mission."""
        if self.kind == "survive_time":
            return f"{min(self.progress, self.target)}/{self.target} s"
        if self.kind == "pass_obstacles":
            return f"{self.progress}/{self.target} obstacles"
        if self.kind == "streak_survival":
            return f"{self.progress}/{self.target} obstacles evit\u00e9s"
        return f"{self.progress}/{self.target}"


class ObjectiveManager:
    """Orchestre les missions secondaires disponibles pendant une run.

    Le manager choisit une mission au debut de partie, relaie les mises a jour
    de progression, puis expose la recompense une fois la mission terminee.
    """
    def __init__(self):
        # Mission active pendant la run (None avant start_run).
        self.current = None

        # Bibliotheque de missions templates. Chaque run clone une entree
        # pour repartir sur un etat vierge (progress/reward non consomme).
        self.templates = [
            SecondaryObjective(
                "Survivre 30 secondes",
                "Reste en vie pendant 30 secondes.",
                "survive_time",
                30,
                250,
            ),
            SecondaryObjective(
                "Survivre 45 secondes",
                "Tient la cadence le plus longtemps possible.",
                "survive_time",
                45,
                400,
            ),
            SecondaryObjective(
                "Passer 10 obstacles",
                "Evite 10 obstacles sans les toucher.",
                "pass_obstacles",
                10,
                300,
            ),
            SecondaryObjective(
                "Passer 20 obstacles",
                "Fais une vraie serie d'esquive.",
                "pass_obstacles",
                20,
                500,
            ),
            SecondaryObjective(
                "Serie de 5 obstacles",
                "Enchaine 5 obstacles evites sans te faire toucher.",
                "pass_obstacles",
                5,
                180,
            ),
        ]

    def _clone(self, template):
        """Clone un template en nouvelle instance mutable pour la run courante."""
        return SecondaryObjective(
            template.title,
            template.description,
            template.kind,
            template.target,
            template.reward,
        )

    def start_run(self):
        """Selectionne aleatoirement une mission et l'active pour la run."""
        # On clone le template pour garder une copie propre d'une partie a l'autre.
        self.current = self._clone(random.choice(self.templates))
        return self.current

    def update_elapsed(self, elapsed_seconds):
        """Relaye la progression temporelle a la mission active."""
        if self.current is None:
            return
        # Les missions de survie avancent automatiquement avec le temps passe en jeu.
        self.current.update_elapsed(elapsed_seconds)

    def register_obstacles_passed(self, count):
        """Relaye le nombre d'obstacles evites a la mission active."""
        if self.current is None:
            return
        # Les obstacles supprimes sans collision comptent pour les objectifs d'esquive.
        self.current.register_obstacles_passed(count)

    def consume_reward(self):
        """Recupere la recompense de mission si elle est disponible."""
        if self.current is None:
            return 0
        # La recompense n'est distribuee qu'une seule fois.
        return self.current.consume_reward()