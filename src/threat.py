class Threat:
    def __init__(self, type, location, velocity, direction, power):
        self.type = type
        self.location = location
        self.velocity = velocity
        self.direction = direction
        self.power = power

    def location_update(self):
        pass



class BallisticMissile(Threat):
    def location_update(self,location, velocity, direction, power):
        super().__init__("allisticMissile",location, velocity, direction, power)
        self.x, self.y = location 
        self.vx, self.vy = velocity
    def location_update(self):
        self.x = self.x + self.vx * dt
        self.vy = self.vy - 9.8 * dt                                              
        self.y = self.y + self.vy * dt


class CruiseMissile(Threat):
    pass


class Drone(Threat):
    pass