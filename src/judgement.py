import math

class HitJudgement:
    def __init__(self, kill_radius=50, target_x, target_y):
        self.kill_radius = kill_radius
        self.target_x = target_x
        self.target_y= target_y




    def check_intercept(self, missile, threat):
        dx = missile.x - threat.x
        dy = missile.y - threat.y
        distance = math.sqrt(dx**2 + dy**2)
        return distance  <= self.kill_radius
            
    def check_hit(self,threat):
        dx = self.target_x - threat.x
        dy = self.target_y - threat.y
        distance = math.sqrt(dx**2 + dy**2)
        return distance <= self.kill_radius
