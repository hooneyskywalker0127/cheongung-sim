from threat import Threat
import math
import random


class Radar:
    def __init__(self,detection_range,radar_x, radar_y):
        self.detection_range = detection_range
        self.detection_prob = {"BallisticMissile": 0.95, "CruiseMissile": 0.75, "Drone": 0.40} 
        self.radar_x = radar_x
        self.radar_y = radar_y
    
    def scan(self,threats):
        detected = []
        for threat in threats:
            dx = self.radar_x - threat.x
            dy = self.radar_y - threat.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance <= self.detection_range:
                if random.random() <= self.detection_prob[threat.type]:
                    detected.append(threat)
        return detected