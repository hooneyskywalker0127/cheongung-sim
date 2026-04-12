import pygame
import matplotlib.pyplot as plt

class Visualizer:
    def __init__(self,threats,missiles,radar, target_hp=1000):
        self.size = (800,600)
        self.threats = threats
        self.missiles = missiles
        self.radar = radar
        self.target_hp = target_hp
        self.target_max_hp = target_hp
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

    def event(self):
        for event in pygame.event.get():                                              
            if event.type == pygame.QUIT:                                             
                return False                                                          
        return True 


    def status_update(self):
        text = self.font.render(f"Missiles: {len(self.missiles)}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

    def rendering(self):
        self.screen.fill((0, 0, 0))
        for threat in self.threats:
            if threat.type == "BallisticMissile":                                       
                color = (255, 0, 0)         
            elif threat.type == "CruiseMissile":                                        
                color = (255, 165, 0)
            else:                                                                         
                color = (255, 255, 0)
            
            pygame.draw.circle(self.screen, color, (threat.x, threat.y), 5)
        for missile in self.missiles:
            color = (0,0,255)
            pygame.draw.circle(self.screen, color, (missile.x, missile.y), 5)
        
        color = (0, 255, 0)
        pygame.draw.rect(self.screen, color,(self.radar.radar_x, self.radar.radar_y, 10, 10))
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



class ResultGraph:
    def __init__(self,metrics):
        self.metrics = metrics

    def draw_graph(self):
        types = list(self.metrics.intercept_success.keys())
        success = list(self.metrics.intercept_success.values())
        fail = list(self.metrics.intercept_fail.values())

        x = range(len(types))
        plt.bar(x, success, width=0.4, label="Success", color="blue")
        plt.bar([i + 0.4 for i in x], fail, width=0.4, label="Fail", color="red")
        plt.xticks([i + 0.2 for i in x], types)
        plt.title("Intercept Result")
        plt.legend()
        plt.show()
