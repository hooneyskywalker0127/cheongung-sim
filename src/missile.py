import math

class InterceptMissile:
    def __init__(self,x,y,target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.battery_x = x
        self.battery_y = y
        self.speed = 300
        distance = math.sqrt((target_x-x)**2 + (target_y-y)**2)
        self.vx = (target_x-x) / distance * self.speed
        self.vy = (target_y-y) / distance * self.speed
        self.phase = 1


    def update(self, dt, threat):
        self.x += self.vx*dt
        self.y += self.vy*dt
        distance = math.sqrt((self.target_x-self.x)**2 + (self.target_y-self.y)**2)
        if distance > 700 :
            self.phase = 1
        elif 700 > distance > 200:
            self.phase = 2
            self.vx = (self.target_x-self.x) / distance * self.speed
            self.vy = (self.target_y-self.y) / distance * self.speed
        elif distance < 200:
            self.phase = 3
            self.target_x = threat.x
            self.target_y = threat.y
            self.vx = (self.target_x-self.x) / distance * self.speed
            self.vy = (self.target_y-self.y) / distance * self.speed



