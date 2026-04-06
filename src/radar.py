

class Radar:
    def __init__(self,detection_range,detection_prob,radar_x, radar_y):
        self.detection_range = detection_range
        self.detection_prob = detection_prob
        self.radar_x = radar_x
        self.radar_y = radar_y
    
    def scan(self):
        pass
