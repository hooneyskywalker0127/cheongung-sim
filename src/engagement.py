from radar import Radar
from threat import Threat
import numpy as np
from missile import InterceptMissile

class Engagement:
    def __init__(self, radar, remaining_missiles, fire_interval=0.8, max_simultaneous=5):
        self.radar = radar
        self.remaining_missiles = remaining_missiles
        self.missiles = []
        self.fire_interval = fire_interval      # 발사 간격 (초)
        self.fire_cooldown = 0.0               # 현재 쿨다운
        self.max_simultaneous = max_simultaneous  # 동시 교전 최대 수

    def assign_priority(self, detected_threats):
        score = []
        bx, by = self.radar.radar_x, self.radar.radar_y
        for threat in detected_threats:
            speed_score = np.sqrt(threat.vx**2 + threat.vy**2)
            dist_to_base = np.sqrt((threat.x - bx)**2 + (threat.y - by)**2) + 1
            distance_score = 1 / dist_to_base
            total_score = speed_score + distance_score
            score.append((total_score, threat))
        return sorted(score, key=lambda x: x[0], reverse=True)

    def intercept(self, prioritized_threats, dt):
        self.fire_cooldown = max(0.0, self.fire_cooldown - dt)
        if self.remaining_missiles == 0 or self.fire_cooldown > 0:
            return
        already_targeted = {id(m.threat) for m in self.missiles}
        active_intercepts = len(already_targeted)

        for score, threat in prioritized_threats:
            if self.remaining_missiles == 0:
                return
            if id(threat) in already_targeted:
                continue
            # 속도 없는 위협 스킵
            speed = np.sqrt(threat.vx**2 + threat.vy**2)
            if speed < 25:
                continue
            # 5초 궤적 예측 — 현재 위치 제외, 실제로 이동해서 기지 150px 이내 진입 시만 교전
            bx, by = self.radar.radar_x, self.radar.radar_y
            will_hit = False
            px, py = threat.x + threat.vx * 0.5, threat.y + threat.vy * 0.5
            for _ in range(45):  # 0.1초 단위 4.5초
                px += threat.vx * 0.1
                py += threat.vy * 0.1
                if np.sqrt((px - bx)**2 + (py - by)**2) < 150:
                    will_hit = True
                    break
            if not will_hit:
                continue
            # 방향 통과한 위협만 동시 교전 수 체크
            if active_intercepts >= self.max_simultaneous:
                return
            missile = InterceptMissile(self.radar.radar_x, self.radar.radar_y, threat.x, threat.y, threat)
            self.missiles.append(missile)
            self.remaining_missiles -= 1
            self.fire_cooldown = self.fire_interval
            active_intercepts += 1
            return  # 한 번에 한 발만

    def update_missiles(self, dt):
        for missile in self.missiles:
            missile.update(dt, missile.threat)