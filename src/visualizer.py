import pygame
import matplotlib.pyplot as plt
import math


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5
        self.max_radius = 40
        self.alpha = 255
        self.done = False

    def update(self):
        self.radius += 3
        self.alpha -= 18
        if self.radius >= self.max_radius or self.alpha <= 0:
            self.done = True

    def draw(self, screen):
        if self.done:
            return
        surf = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 180, 0, max(0, self.alpha)), (self.max_radius, self.max_radius), self.radius, 3)
        pygame.draw.circle(surf, (255, 80, 0, max(0, self.alpha // 2)), (self.max_radius, self.max_radius), self.radius // 2)
        screen.blit(surf, (self.x - self.max_radius, self.y - self.max_radius))


class Visualizer:
    def __init__(self, threats, missiles, radar, target_hp=1000):
        self.size = (800, 600)
        self.threats = threats
        self.missiles = missiles
        self.radar = radar
        self.target_hp = target_hp
        self.target_max_hp = target_hp
        self.explosions = []
        self.trails = {}  # id → [(x, y), ...]

        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("KM-SAM II / Cheongung-II Defense Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20)
        self.font_large = pygame.font.SysFont("monospace", 28, bold=True)

    def add_explosion(self, x, y):
        self.explosions.append(Explosion(int(x), int(y)))

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def _draw_grid(self):
        for x in range(0, 800, 80):
            pygame.draw.line(self.screen, (20, 40, 20), (x, 0), (x, 600))
        for y in range(0, 600, 60):
            pygame.draw.line(self.screen, (20, 40, 20), (0, y), (800, y))

    def _draw_radar_range(self):
        surf = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.circle(surf, (0, 255, 0, 25),
                           (self.radar.radar_x, self.radar.radar_y),
                           self.radar.detection_range)
        pygame.draw.circle(surf, (0, 255, 0, 80),
                           (self.radar.radar_x, self.radar.radar_y),
                           self.radar.detection_range, 1)
        self.screen.blit(surf, (0, 0))

    def _update_trails(self):
        all_objs = list(self.threats) + list(self.missiles)
        current_ids = {id(o) for o in all_objs}

        # 사라진 객체 trail 제거
        for key in list(self.trails.keys()):
            if key not in current_ids:
                del self.trails[key]

        # trail 업데이트
        for obj in all_objs:
            oid = id(obj)
            if oid not in self.trails:
                self.trails[oid] = []
            self.trails[oid].append((int(obj.x), int(obj.y)))
            if len(self.trails[oid]) > 20:
                self.trails[oid].pop(0)

    def _draw_trails(self):
        for obj in list(self.threats) + list(self.missiles):
            oid = id(obj)
            trail = self.trails.get(oid, [])
            if hasattr(obj, 'type'):  # threat
                if obj.type == "BallisticMissile":
                    base_color = (255, 0, 0)
                elif obj.type == "CruiseMissile":
                    base_color = (255, 165, 0)
                else:
                    base_color = (255, 255, 0)
            else:
                base_color = (0, 100, 255)

            for i, pos in enumerate(trail):
                alpha = int(180 * (i / len(trail))) if trail else 0
                r = max(0, min(255, base_color[0]))
                g = max(0, min(255, base_color[1]))
                b = max(0, min(255, base_color[2]))
                faded = (r * alpha // 180, g * alpha // 180, b * alpha // 180)
                pygame.draw.circle(self.screen, faded, pos, 2)

    def status_update(self):
        # 위협 카운트
        threat_counts = {"BallisticMissile": 0, "CruiseMissile": 0, "Drone": 0}
        for t in self.threats:
            threat_counts[t.type] += 1

        lines = [
            f"INTERCEPTORS : {len(self.missiles)}",
            f"BALLISTIC    : {threat_counts['BallisticMissile']}",
            f"CRUISE       : {threat_counts['CruiseMissile']}",
            f"DRONE        : {threat_counts['Drone']}",
        ]
        for i, line in enumerate(lines):
            text = self.font.render(line, True, (0, 220, 0))
            self.screen.blit(text, (10, 10 + i * 24))

        # HP 바
        hp_ratio = max(0, self.target_hp) / self.target_max_hp
        bar_color = (0, 255, 0) if hp_ratio > 0.5 else (255, 165, 0) if hp_ratio > 0.25 else (255, 0, 0)
        hp_label = self.font.render(f"BASE HP : {max(0, self.target_hp)}", True, bar_color)
        self.screen.blit(hp_label, (10, 115))
        pygame.draw.rect(self.screen, (60, 60, 60), (10, 138, 200, 12))
        pygame.draw.rect(self.screen, bar_color, (10, 138, int(200 * hp_ratio), 12))

    def rendering(self):
        self.screen.fill((0, 8, 0))
        self._draw_grid()
        self._draw_radar_range()
        self._update_trails()
        self._draw_trails()

        # 위협 렌더링
        label_map = {"BallisticMissile": "BM", "CruiseMissile": "CM", "Drone": "DR"}
        for threat in self.threats:
            if threat.type == "BallisticMissile":
                color = (255, 50, 50)
            elif threat.type == "CruiseMissile":
                color = (255, 165, 0)
            else:
                color = (255, 255, 0)
            x, y = int(threat.x), int(threat.y)
            pygame.draw.circle(self.screen, color, (x, y), 6)
            label = self.font.render(label_map[threat.type], True, color)
            self.screen.blit(label, (x + 8, y - 10))

        # 요격 미사일 렌더링
        for missile in self.missiles:
            pygame.draw.circle(self.screen, (0, 160, 255), (int(missile.x), int(missile.y)), 4)

        # 레이더/기지
        rx, ry = self.radar.radar_x, self.radar.radar_y
        hp_ratio = max(0, self.target_hp) / self.target_max_hp
        bar_color = (0, 255, 0) if hp_ratio > 0.5 else (255, 165, 0) if hp_ratio > 0.25 else (255, 0, 0)
        pygame.draw.rect(self.screen, (0, 255, 0), (rx - 8, ry - 8, 16, 16))
        label = self.font.render("KM-SAM II", True, (0, 255, 0))
        self.screen.blit(label, (rx - 30, ry + 12))
        # HP 바 (기지 위에)
        bar_w = 80
        pygame.draw.rect(self.screen, (60, 60, 60), (rx - bar_w // 2, ry - 28, bar_w, 8))
        pygame.draw.rect(self.screen, bar_color, (rx - bar_w // 2, ry - 28, int(bar_w * hp_ratio), 8))
        hp_text = self.font.render(f"{max(0, self.target_hp)}", True, bar_color)
        self.screen.blit(hp_text, (rx - bar_w // 2, ry - 46))

        # 폭발 이펙트
        for exp in self.explosions:
            exp.update()
            exp.draw(self.screen)
        self.explosions = [e for e in self.explosions if not e.done]

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.event()
            self.status_update()
            self.rendering()
            self.clock.tick(60)
        if not running:
            pygame.quit()


def show_intro(screen, font_large, font):
    lines = [
        "2026. Strait of Hormuz, UAE",
        "Iranian ballistic missile batteries are ready to launch.",
        "",
        "Cheongung-II  (KM-SAM II)",
        "Air Defense Intercept Simulation",
        "",
        "[ Press SPACE to Start ]",
    ]
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 8, 0))
        for i, line in enumerate(lines):
            f = font_large if i in (3, 4) else font
            color = (0, 255, 0) if i in (3, 4) else (180, 220, 180)
            text = f.render(line, True, color)
            screen.blit(text, (400 - text.get_width() // 2, 160 + i * 40))
        pygame.display.flip()
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return


class ResultGraph:
    def __init__(self, metrics):
        self.metrics = metrics

    def draw_graph(self):
        types = list(self.metrics.intercept_success.keys())
        success = list(self.metrics.intercept_success.values())
        fail = list(self.metrics.intercept_fail.values())

        x = range(len(types))
        plt.style.use("dark_background")
        plt.bar(x, success, width=0.4, label="Intercepted", color="#00aaff")
        plt.bar([i + 0.4 for i in x], fail, width=0.4, label="Hit Base", color="#ff4444")
        plt.xticks([i + 0.2 for i in x], types)
        plt.title("KM-SAM II — Intercept Result", color="white")
        plt.legend()
        plt.tight_layout()
        plt.show()
