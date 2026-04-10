import pygame


class Visualizer:
    def __init__(self,threats,missiles,radar):
        self.size = (800,600)
        self.threats = threats
        self.missiles = missiles
        self.radar = radar
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

    def event(self):
        pass

    def status_update(self):
        pass

    def rendering(self):
        pass

    def run(self):
        running = True
        while running:
            self.event()
            self.status_update()
            self.rendering()
            if running = self.event()

        if not running:
            pygame.quit()







class ResultGraph:
    def __init__(self):
        pass