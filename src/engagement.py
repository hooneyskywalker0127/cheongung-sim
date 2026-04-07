from radar import Radar
from threat import Threat
import numpy as np


class Engagement:
    def __init__(self,radar,remaining_missiles):
        self.radar = radar
        self.remaining_missiles = remaining_missiles
        self.missiles = []
        

    def assign_priority(self,detected_threats):
        score = []
        for threat in detected_threats:
            speed_score = np.sqrt(threat.vx**2+threat.vy**2)
            altitude_score = 1/threat.y
            distance_score = 1/np.sqrt(threat.x**2+threat.y**2)
            total_score = speed_score + altitude_score + distance_score
            score.append((total_score,threat))

        return sorted(score, key=lambda x:x[0], reverse=True)
    
    def intercept(self,prioritized_threats):
        if self.remaining_missiles == 0:
            return False