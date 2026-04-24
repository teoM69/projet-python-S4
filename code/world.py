import os
import random
import pygame


def _lerp_color(color_a, color_b, t):
    t = max(0.0, min(1.0, t))
    return (
        int(color_a[0] + (color_b[0] - color_a[0]) * t),
        int(color_a[1] + (color_b[1] - color_a[1]) * t),
        int(color_a[2] + (color_b[2] - color_a[2]) * t),
    )


class World:
    def __init__(self, speed, screen_width, screen_height):
        self.speed = speed
        self.wallHeight = 42
        self.obstacle = []
        self.screen_width = screen_width
        self.screen_height = screen_height

        # === GEOMETRIE DE L'ECRAN ===
        # Calcule les positions du plafond et du sol.
        # Le plafond est situe a environ 25 % du haut de l'ecran (75 % du bas).
        # Cela cree le couloir superieur ou les obstacles peuvent apparaitre.
        self.roof_y = int(self.screen_height * 0.25)
        
        # Position du sol : hauteur de l'ecran - marge superieure (50) - hauteur du sol (165).
        # Cela cree le couloir inferieur ou les obstacles peuvent apparaitre.
        self.floor_y = self.screen_height - 50 - 165

        self.top_structures = []
        self.bottom_structures = []
        self.middle_structures = []
        self._next_top_x = 0
        self._next_bottom_x = 0
        self._next_middle_x = 0
        self._rng = random.Random()
        self.difficulty_ratio = 0.0
        self.parallax_x = 0.0
        self.has_bg_image = False

        bg_path = os.path.join("assets", "Images", "BackGround.png")
        try:
            self.bg_image = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (self.screen_width, self.screen_height))
            self.has_bg_image = True
        except Exception:
            self.bg_image = pygame.Surface((self.screen_width, self.screen_height))
            self.bg_image.fill((35, 35, 35))

        self._gradient_overlay = self._build_gradient_overlay()
        self._scanline_overlay = self._build_scanline_overlay()
        self._vignette_overlay = self._build_vignette_overlay()
        self._fx_surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self._particles = self._build_particles(80)
        self._light_columns = self._build_light_columns(7)

        self.reset_structures()

    def _build_gradient_overlay(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        top_color = (8, 22, 52)
        bottom_color = (38, 15, 40)
        for y in range(self.screen_height):
            t = y / max(1, self.screen_height - 1)
            color = _lerp_color(top_color, bottom_color, t)
            alpha = int(85 + (60 * t))
            pygame.draw.line(overlay, (color[0], color[1], color[2], alpha), (0, y), (self.screen_width, y))
        return overlay

    def _build_scanline_overlay(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        for y in range(0, self.screen_height, 4):
            pygame.draw.line(overlay, (255, 255, 255, 12), (0, y), (self.screen_width, y))
        return overlay

    def _build_vignette_overlay(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        border = min(self.screen_width, self.screen_height) // 2
        for i in range(0, border, 10):
            w = self.screen_width - (2 * i)
            h = self.screen_height - (2 * i)
            if w <= 0 or h <= 0:
                break
            alpha = int(115 * (1.0 - (i / max(1, border))))
            pygame.draw.rect(overlay, (0, 0, 0, alpha), (i, i, w, h), width=2, border_radius=20)
        return overlay

    def _build_particles(self, count):
        particles = []
        for _ in range(count):
            particles.append(
                {
                    "x": self._rng.uniform(0, self.screen_width),
                    "y": self._rng.uniform(0, self.screen_height),
                    "r": self._rng.randint(1, 2),
                    "speed": self._rng.uniform(0.25, 1.0),
                    "alpha": self._rng.randint(50, 150),
                }
            )
        return particles

    def _build_light_columns(self, count):
        columns = []
        for _ in range(count):
            width = self._rng.randint(90, 190)
            columns.append(
                {
                    "x": self._rng.uniform(-self.screen_width, self.screen_width),
                    "w": width,
                    "alpha": self._rng.randint(14, 30),
                    "speed": self._rng.uniform(0.08, 0.2),
                }
            )
        return columns

    def _update_ambient(self, speed):
        self.parallax_x = (self.parallax_x + (speed * 0.5)) % self.screen_width

        for particle in self._particles:
            particle["x"] -= speed * (0.22 + particle["speed"] * 0.22)
            if particle["x"] < -4:
                particle["x"] = self.screen_width + self._rng.randint(0, 90)
                particle["y"] = self._rng.uniform(0, self.screen_height)
                particle["alpha"] = self._rng.randint(50, 150)

        for column in self._light_columns:
            column["x"] -= speed * column["speed"]
            if column["x"] + column["w"] < -10:
                column["x"] = self.screen_width + self._rng.randint(60, 260)
                column["w"] = self._rng.randint(90, 190)
                column["alpha"] = self._rng.randint(14, 30)
                column["speed"] = self._rng.uniform(0.08, 0.2)

    def _draw_segment(self, screen, rect, body_color, inner_color, edge_color, glow_color, contact_edge):
        shadow = rect.move(0, 4)
        pygame.draw.rect(screen, (8, 8, 12), shadow, border_radius=8)
        pygame.draw.rect(screen, body_color, rect, border_radius=8)

        inner = rect.inflate(-6, -6)
        if inner.width > 0 and inner.height > 0:
            pygame.draw.rect(screen, inner_color, inner, border_radius=6)

        if contact_edge == "top":
            line_y = rect.top + 2
            glow_y = rect.top - 4
        else:
            line_y = rect.bottom - 2
            glow_y = rect.bottom - 4

        pygame.draw.line(screen, edge_color, (rect.left + 6, line_y), (rect.right - 6, line_y), 2)
        glow = pygame.Surface((max(1, rect.width), 8), pygame.SRCALPHA)
        glow.fill((glow_color[0], glow_color[1], glow_color[2], 75))
        screen.blit(glow, (rect.x, glow_y))

    def _draw_middle_segment(self, screen, rect):
        self._draw_segment(
            screen,
            rect,
            body_color=(46, 50, 64),
            inner_color=(74, 79, 96),
            edge_color=(160, 206, 214),
            glow_color=(118, 188, 197),
            contact_edge="top",
        )
        glow = pygame.Surface((max(1, rect.width), 8), pygame.SRCALPHA)
        glow.fill((118, 188, 197, 60))
        screen.blit(glow, (rect.x, rect.bottom - 4))

    def _draw_ambient(self, screen):
        self._fx_surface.fill((0, 0, 0, 0))

        for column in self._light_columns:
            pygame.draw.rect(
                self._fx_surface,
                (98, 148, 238, column["alpha"]),
                (int(column["x"]), 0, int(column["w"]), self.screen_height),
            )

        for particle in self._particles:
            pygame.draw.circle(
                self._fx_surface,
                (190, 220, 255, particle["alpha"]),
                (int(particle["x"]), int(particle["y"])),
                particle["r"],
            )

        screen.blit(self._fx_surface, (0, 0))

    def reset_structures(self):
        self.top_structures = [{"x": -120, "w": self.screen_width + 280, "h": self.wallHeight}]
        self.bottom_structures = [{"x": -120, "w": self.screen_width + 280, "h": self.wallHeight}]
        self.middle_structures = []
        self._next_top_x = self.screen_width + 160
        self._next_bottom_x = self.screen_width + 160
        self._next_middle_x = self.screen_width + 420

    def _middle_band(self):
        # === ZONE DES PLATEFORMES CENTRALES ===
        # Defini la bande verticale ou les plateformes centrales peuvent apparaitre.
        # Limite haute : sous le plafond (roof_y + 80).
        # Limite basse : au-dessus du sol (floor_y - 95).
        # Cela cree une zone jouable au milieu de l'ecran.
        top_limit = self.roof_y + 80
        bottom_limit = self.floor_y - 95
        if bottom_limit <= top_limit:
            bottom_limit = top_limit + 1
        return top_limit, bottom_limit

    def _append_segment(self, lane):
        d = self.difficulty_ratio
        if lane == "top":
            min_gap = int(45 + (40 * d))
            max_gap = int(130 + (95 * d))
            min_width = int(260 - (85 * d))
            max_width = int(520 - (175 * d))
            min_height = 30
            max_height = 56
            structures = self.top_structures
            next_x = self._next_top_x
        elif lane == "bottom":
            min_gap = int(45 + (40 * d))
            max_gap = int(130 + (95 * d))
            min_width = int(260 - (85 * d))
            max_width = int(520 - (175 * d))
            min_height = 30
            max_height = 56
            structures = self.bottom_structures
            next_x = self._next_bottom_x
        else:
            min_gap = int(120 + (120 * d))
            max_gap = int(260 + (180 * d))
            min_width = int(120 - (20 * d))
            max_width = int(240 - (50 * d))
            min_height = 22
            max_height = 34
            structures = self.middle_structures
            next_x = self._next_middle_x

        if max_width <= min_width:
            max_width = min_width + 1
        if max_gap <= min_gap:
            max_gap = min_gap + 1

        gap = self._rng.randint(min_gap, max_gap)
        width = self._rng.randint(min_width, max_width)
        thickness = self._rng.randint(min_height, max_height)

        x = next_x + gap
        if lane == "middle":
            # Garde des plateformes centrales presentes, mais evite de saturer le couloir.
            if self._rng.random() < (0.45 + (0.25 * d)):
                self._next_middle_x = x + self._rng.randint(140, 300)
                return
            mid_min, mid_max = self._middle_band()
            y = self._rng.randint(mid_min, mid_max)
            structures.append({"x": x, "y": y, "w": width, "h": thickness})
        else:
            structures.append({"x": x, "w": width, "h": thickness})

        if lane == "top":
            self._next_top_x = x + width
        elif lane == "bottom":
            self._next_bottom_x = x + width
        else:
            self._next_middle_x = x + width

    def update_structures(self, speed, difficulty_ratio=0.0):
        self.difficulty_ratio = max(0.0, min(1.0, difficulty_ratio))
        self._update_ambient(speed)
        self._next_top_x -= speed
        self._next_bottom_x -= speed
        self._next_middle_x -= speed

        for seg in self.top_structures:
            seg["x"] -= speed
        for seg in self.bottom_structures:
            seg["x"] -= speed
        for seg in self.middle_structures:
            seg["x"] -= speed

        self.top_structures = [s for s in self.top_structures if s["x"] + s["w"] > -30]
        self.bottom_structures = [s for s in self.bottom_structures if s["x"] + s["w"] > -30]
        self.middle_structures = [s for s in self.middle_structures if s["x"] + s["w"] > -30]

        while self._next_top_x < self.screen_width + 300:
            self._append_segment("top")
        while self._next_bottom_x < self.screen_width + 300:
            self._append_segment("bottom")
        while self._next_middle_x < self.screen_width + 300:
            self._append_segment("middle")

    def get_middle_spawn_y(self):
        candidates = [s for s in self.middle_structures if s["x"] + s["w"] >= self.screen_width - 80]
        if not candidates:
            return None
        seg = self._rng.choice(candidates)
        return seg["y"]

    def has_support(self, lane, x, span=1):
        if lane == "top":
            structures = self.top_structures
        else:
            structures = self.bottom_structures

        left = x - (span / 2)
        right = x + (span / 2)
        for seg in structures:
            seg_left = seg["x"]
            seg_right = seg["x"] + seg["w"]
            if right >= seg_left and left <= seg_right:
                return True
        return False

    def find_floor_y(self, x, span, player_top):
        left = x - (span / 2)
        right = x + (span / 2)
        candidates = []

        for seg in self.bottom_structures:
            if right >= seg["x"] and left <= seg["x"] + seg["w"]:
                candidates.append(self.floor_y)

        for seg in self.middle_structures:
            if right >= seg["x"] and left <= seg["x"] + seg["w"] and seg["y"] >= player_top:
                candidates.append(seg["y"])

        if not candidates:
            return None
        return min(candidates)

    def find_ceiling_y(self, x, span, player_bottom):
        left = x - (span / 2)
        right = x + (span / 2)
        candidates = []

        for seg in self.top_structures:
            if right >= seg["x"] and left <= seg["x"] + seg["w"]:
                candidates.append(self.roof_y)

        for seg in self.middle_structures:
            bottom = seg["y"] + seg["h"]
            if right >= seg["x"] and left <= seg["x"] + seg["w"] and bottom <= player_bottom:
                candidates.append(bottom)

        if not candidates:
            return None
        return max(candidates)

    def drawBackGround(self, screen):
        if self.has_bg_image:
            offset = int(self.parallax_x * 0.3) % self.screen_width
            screen.blit(self.bg_image, (-offset, 0))
            screen.blit(self.bg_image, (self.screen_width - offset, 0))
        else:
            screen.blit(self.bg_image, (0, 0))

    def drawWalls(self, screen):
        for seg in self.top_structures:
            rect = pygame.Rect(int(seg["x"]), int(self.roof_y - seg["h"]), int(seg["w"]), int(seg["h"]))
            self._draw_segment(
                screen,
                rect,
                body_color=(43, 56, 89),
                inner_color=(74, 92, 132),
                edge_color=(140, 205, 255),
                glow_color=(94, 170, 245),
                contact_edge="bottom",
            )
        for seg in self.bottom_structures:
            rect = pygame.Rect(int(seg["x"]), int(self.floor_y), int(seg["w"]), int(seg["h"]))
            self._draw_segment(
                screen,
                rect,
                body_color=(82, 52, 74),
                inner_color=(120, 78, 108),
                edge_color=(255, 183, 142),
                glow_color=(255, 143, 111),
                contact_edge="top",
            )
        for seg in self.middle_structures:
            rect = pygame.Rect(int(seg["x"]), int(seg["y"]), int(seg["w"]), int(seg["h"]))
            self._draw_middle_segment(screen, rect)