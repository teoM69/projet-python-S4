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
        if self.kind != "survive_time" or self.completed or self.failed:
            return
        self.progress = min(self.target, int(elapsed_seconds))
        if elapsed_seconds >= self.target:
            self.completed = True

    def register_obstacles_passed(self, count):
        if self.kind != "pass_obstacles" or self.completed or self.failed:
            return
        self.progress = min(self.target, self.progress + max(0, count))
        if self.progress >= self.target:
            self.completed = True

    def consume_reward(self):
        if self.completed and not self.reward_claimed:
            self.reward_claimed = True
            return self.reward
        return 0

    def status_label(self):
        if self.completed:
            return "Reussie"
        if self.failed:
            return "Ratee"
        return "En cours"

    def progress_label(self):
        if self.kind == "survive_time":
            return f"{min(self.progress, self.target)}/{self.target} s"
        if self.kind == "pass_obstacles":
            return f"{self.progress}/{self.target} obstacles"
        if self.kind == "streak_survival":
            return f"{self.progress}/{self.target} obstacles evit\u00e9s"
        return f"{self.progress}/{self.target}"


class ObjectiveManager:
    def __init__(self):
        self.current = None
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
        return SecondaryObjective(
            template.title,
            template.description,
            template.kind,
            template.target,
            template.reward,
        )

    def start_run(self):
        self.current = self._clone(random.choice(self.templates))
        return self.current

    def update_elapsed(self, elapsed_seconds):
        if self.current is None:
            return
        self.current.update_elapsed(elapsed_seconds)

    def register_obstacles_passed(self, count):
        if self.current is None:
            return
        self.current.register_obstacles_passed(count)

    def consume_reward(self):
        if self.current is None:
            return 0
        return self.current.consume_reward()