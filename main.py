import pygame
import math
import simulator

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


scaleFactor = min(WIDTH//10, HEIGHT//10) / 378137.0
Re = 378137.0 # m

class drawnEarth():
    def __init__(self):
        self.surface = screen
        self.center = (WIDTH//2, HEIGHT//2)
        self.radius = 378137.0 
        self.drawnRadius = self.radius * scaleFactor
        self.color = (0, 0, 255)

    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.center, self.drawnRadius)

earth = drawnEarth()

def main():
    dTime = simulator.t_max / 100000
    running = True
    step = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False



            screen.fill((0, 0, 0))
            earth.draw()


            x = earth.center[0] + (earth.radius + list(simulator.altitude)[step]) * math.cos(list(simulator.psi)[step]) * scaleFactor
            y = earth.center[1] + (earth.radius + list(simulator.altitude)[step]) * math.sin(list(simulator.psi)[step]) * scaleFactor
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)


            pygame.display.update()
            step += 1

if __name__ == "__main__":
    main()
pygame.quit()