import random


class Threat:
    def __init__(self, type, location, velocity, power):
        self.type = type
        self.location = location
        self.velocity = velocity
        self.power = power

    def location_update(self):
        pass



class BallisticMissile(Threat):
    def __init__(self, location, velocity, power):
        super().__init__("BallisticMissile", location, velocity, power)
        self.x, self.y = location 
        self.vx, self.vy = velocity
    
    def location_update(self, dt):
        self.x = self.x + self.vx * dt
        self.vy = self.vy - 9.8 * dt                                              
        self.y = self.y + self.vy * dt


class CruiseMissile(Threat):
    def __init__(self, location, velocity, power):
        super().__init__("CruiseMissile", location, velocity, power)
        self.x, self.y = location 
        self.vx, self.vy = velocity

    def location_update(self, dt):
        self.x = self.x + self.vx * dt

class Drone(Threat):
    def __init__(self, location, velocity, power):
        super().__init__("Drone", location, velocity, power)
        self.x, self.y = location 
        self.vx, self.vy = velocity

    def location_update(self,dt):
        self.vx = self.vx + random.uniform(-0.5, 0.5)                                           
        self.vy = self.vy + random.uniform(-0.5, 0.5)
        self.x = self.x + self.vx * dt                                                               
        self.y = self.y + self.vy * dt 