import math

class InterceptMissile:
    def __init__(self,x,y,target_x, target_y):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = 300
        distance = math.sqrt((target_x-x)**2 + (target_y-y)**2)
        self.vx = (target_x-x) / distance * self.speed
        self.vy = (target_y-y) / distance * self.speed
        self.phase = 1


    def update(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt
