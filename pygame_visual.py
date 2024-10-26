import pygame
import numpy as np

# Load the solution data (assuming you've saved theta_km and altitude)
data = np.load("solution_data.npz")
theta_km = data["y"][2] * 6378.137  # Convert to kilometers
altitude = data["y"][3] / 1000  # Convert altitude to kilometers
t = data["t"]

# Initialize Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rocket Position")

# Set scaling based on maximum values
scale_x = width / 6000  # Width of 6000 km
scale_y = height / 1500  # Height of 1500 km

# Colors and control
blue = (0, 0, 255)
white = (255, 255, 255)
font = pygame.font.SysFont(None, 24)
running = True

# Main loop
for i in range(len(t)):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Draw x-axis and y-axis labels
    for j in range(0, width, 100):
        x_label = font.render(str(int(j / scale_x)), True, white)
        screen.blit(x_label, (j, height - 20))

    for j in range(0, height, 100):
        y_label = font.render(str(int(j / scale_y)), True, white)
        screen.blit(y_label, (0, height - j - 20))

    # Convert position
    x_pos = (theta_km[i] - theta_km[0]) * scale_x
    y_pos = height - (altitude[i] - altitude[0]) * scale_y

    pygame.draw.circle(screen, blue, (int(x_pos), int(y_pos)), 10)
    pygame.display.flip()
    pygame.time.delay(1)

    if not running:
        break

pygame.quit()
