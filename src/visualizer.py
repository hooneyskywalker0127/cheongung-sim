import pygame


class Visualizer:
    def __init__(self,threats,missiles,radar):
        self.size = (800,600)
        self.threats = threats
        self.missiles = missiles
        self.radar = radar
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()


    def event(self):
        for event in pygame.event.get():                                              
            if event.type == pygame.QUIT:                                             
                return False                                                          
        return True 


    def status_update(self):
        pass

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
    def __init__(self):
        pass