# code/campaign.py

class Level:
    def __init__(self, index, name, speed_start, speed_max, accel_per_frame, spawn_scale, world_difficulty_boost, target_score):
        self.index = index
        self.name = name
        self.speed_start = speed_start
        self.speed_max = speed_max
        self.accel_per_frame = accel_per_frame
        self.spawn_scale = spawn_scale
        self.world_difficulty_boost = world_difficulty_boost
        self.target_score = target_score

class CampaignMode:
    def __init__(self):
        self.levels = [
            Level(1, "Éveil", 5.0, 7.0, 0.005, 1.2, 0.0, 500),
            Level(2, "Intermediaire", 6.0, 9.0, 0.006, 1.0, 0.1, 800),
            Level(3, "Expert", 8.0, 12.0, 0.008, 0.8, 0.2, 1000)
        ]
        self.current_level_idx = 0
        self.total_score = 0

    @property
    def current_level(self):
        return self.levels[self.current_level_idx]

    def reset(self):
        self.current_level_idx = 0
        self.total_score = 0

    def advance_level(self):
        self.current_level_idx += 1
        return self.current_level_idx < len(self.levels)

    def add_level_score(self, score):
        self.total_score += score