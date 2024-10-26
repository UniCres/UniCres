import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Rocket on Planet Simulator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (150, 150, 150)

# Planet and atmosphere settings
planet_radius = 100
planet_center = (WIDTH // 2, HEIGHT // 2)
max_atmosphere_radius = 300  # Max radius for the visible atmosphere effect

# Starry background setup
star_background = pygame.Surface((WIDTH, HEIGHT))
star_background.fill(BLACK)
num_stars = 100  # Number of stars
for _ in range(num_stars):
    star_x = random.randint(0, WIDTH)
    star_y = random.randint(0, HEIGHT)
    pygame.draw.circle(star_background, WHITE, (star_x, star_y), 2)  # Small white dots for stars

# Text Input Parameters
font = pygame.font.Font(None, 36)
label_gap = 20  # Gap between label and input box
input_boxes = []
y_position = 100  # Initial y position for the first label and input box

# Define labels and values
labels_and_values = [
    ("Thrust (N):", "800"),  # Reduced thrust for added challenge
    ("Burn Time (s):", "5"),
    ("Launch Angle:", "45"),
    ("Gravity Strength:", "10"),
    ("Rocket Mass (kg):", "40"),  # Increased mass for additional challenge
    ("Drag Coefficient:", "1.0"),  # Increased drag coefficient
    ("Air Density (kg/m³):", "2.5"),  # Increased air density
    ("Atmosphere Scale Height:", "80")
]

# Create input boxes dynamically based on labels and values
for label_text, default_value in labels_and_values:
    label_surface = font.render(label_text, True, BLACK)
    label_width = label_surface.get_width()
    
    # Set label position
    label_pos = (300, y_position)
    screen.blit(label_surface, label_pos)
    
    # Set input box position based on label width + fixed gap
    box_rect = pygame.Rect(300 + label_width + label_gap, y_position, 140, 32)
    
    # Append to input_boxes list
    input_boxes.append({
        "label": label_text,
        "value": default_value,
        "rect": box_rect,
        "active": False
    })
    
    # Update y_position for next row
    y_position += 50

launch_button_rect = pygame.Rect(300, y_position, 140, 40)
restart_button_rect = pygame.Rect(700, 10, 80, 30)
launch_screen = True

# Simulation main loop
running = True
while running:
    if launch_screen:
        # Draw input screen with a background
        screen.fill(WHITE)
        
        for box in input_boxes:
            # Render label and display next to the input box
            label_surface = font.render(box["label"], True, BLACK)
            screen.blit(label_surface, (box["rect"].x - label_surface.get_width() - label_gap, box["rect"].y + 5))

            # Draw the input box with background and border
            pygame.draw.rect(screen, LIGHT_GRAY if not box["active"] else DARK_GRAY, box["rect"])
            pygame.draw.rect(screen, BLACK, box["rect"], 2)  # Border

            # Display the value in the input box
            text_surface = font.render(box["value"], True, BLACK)
            screen.blit(text_surface, (box["rect"].x + 5, box["rect"].y + 4))

        # Draw the launch button
        pygame.draw.rect(screen, RED, launch_button_rect)
        launch_text = font.render("Launch", True, WHITE)
        screen.blit(launch_text, (launch_button_rect.x + 20, launch_button_rect.y + 5))

        # Input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if launch_button_rect.collidepoint(event.pos):
                    # Capture all input values
                    thrust = float(input_boxes[0]["value"])
                    burn_time = float(input_boxes[1]["value"])
                    launch_angle = float(input_boxes[2]["value"])
                    gravity_strength = float(input_boxes[3]["value"])
                    mass = float(input_boxes[4]["value"])
                    drag_coefficient = float(input_boxes[5]["value"])
                    sea_level_density = float(input_boxes[6]["value"])
                    atmosphere_scale_height = float(input_boxes[7]["value"])

                    # Derived and initial settings
                    angle_rad = math.radians(launch_angle)
                    initial_mass = mass
                    launch_screen = False  # Switch to simulation screen
                for box in input_boxes:
                    box["active"] = box["rect"].collidepoint(event.pos)
            elif event.type == pygame.KEYDOWN:
                for box in input_boxes:
                    if box["active"]:
                        if event.key == pygame.K_BACKSPACE:
                            box["value"] = box["value"][:-1]
                        else:
                            box["value"] += event.unicode
        pygame.display.flip()

    else:
        # Rocket setup based on inputs
        rocket_width, rocket_height = 25, 50  # Rectangle dimensions for the rocket
        cross_sectional_area = rocket_width * rocket_height / 1000  # Cross-sectional area for drag calculations
        rocket_launched = False
        rocket_landed = False
        vx = thrust * math.cos(angle_rad) / mass
        vy = -thrust * math.sin(angle_rad) / mass

        # Starting position on the surface of the planet
        x = planet_center[0] + (planet_radius + rocket_height // 2) * math.cos(angle_rad)
        y = planet_center[1] - (planet_radius + rocket_height // 2) * math.sin(angle_rad)
        time = 0
        dt = 0.01  # Time step

        # Rocket surface
        rocket_surface = pygame.Surface((rocket_width, rocket_height), pygame.SRCALPHA)
        rocket_surface.fill(RED)
        angle = -launch_angle  # Initial angle for rotation

        # Set max boundary for position values
        max_position = 10 * max(WIDTH, HEIGHT)

        # Simulation loop
        while not launch_screen and running:
            screen.blit(star_background, (0, 0))  # Draw the starry background

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    launch_screen = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        rocket_launched = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button_rect.collidepoint(event.pos):
                        launch_screen = True  # Return to input screen
                        break

            # Calculate distance from rocket to planet center
            distance_x = planet_center[0] - x
            distance_y = planet_center[1] - y
            distance = math.sqrt(distance_x**2 + distance_y**2)
            altitude = distance - planet_radius

            # Draw the planet
            pygame.draw.circle(screen, BLUE, planet_center, planet_radius)

            # Draw atmosphere as a semi-transparent circle
            atmosphere_alpha = max(0, int(255 * (1 - altitude / max_atmosphere_radius)))  # Fade with altitude
            atmosphere_color = (135, 206, 250, atmosphere_alpha)  # Light blue with variable transparency
            atmosphere_surface = pygame.Surface((max_atmosphere_radius * 2, max_atmosphere_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(atmosphere_surface, atmosphere_color, (max_atmosphere_radius, max_atmosphere_radius), max_atmosphere_radius)
            screen.blit(atmosphere_surface, (planet_center[0] - max_atmosphere_radius, planet_center[1] - max_atmosphere_radius))

            # Draw the restart button
            pygame.draw.rect(screen, GRAY, restart_button_rect)
            restart_text = font.render("Restart", True, BLACK)
            screen.blit(restart_text, (restart_button_rect.x + 5, restart_button_rect.y + 5))

            # Check if rocket has landed back on the planet
            if distance <= planet_radius + rocket_height // 2:
                rocket_landed = True

            # Apply forces if rocket is launched and hasn't landed
            if rocket_launched and not rocket_landed:
                # Apply thrust during burn time and decrease mass
                if time < burn_time:
                    thrust_force = thrust / mass  # Thrust per unit mass
                    vx += thrust_force * math.cos(angle_rad) * dt
                    vy += thrust_force * math.sin(angle_rad) * dt
                    mass -= initial_mass * (dt / burn_time)  # Linear fuel consumption

                # Calculate air density for drag
                air_density = sea_level_density * math.exp(-altitude / atmosphere_scale_height)

                # Calculate drag force
                speed = math.sqrt(vx**2 + vy**2)
                drag_force = 0.5 * drag_coefficient * air_density * cross_sectional_area * speed**2
                drag_ax = -drag_force * (vx / speed) / mass  # Drag in x
                drag_ay = -drag_force * (vy / speed) / mass  # Drag in y
                vx += drag_ax * dt
                vy += drag_ay * dt

                # Apply gravity towards the planet center
                gravity_force = gravity_strength * (planet_radius / distance) ** 2
                ax = gravity_force * (distance_x / distance)
                ay = gravity_force * (distance_y / distance)

                # Update velocities with gravity
                vx += ax * dt
                vy += ay * dt

                # Update position
                x += vx * dt * 10
                y += vy * dt * 10

                # Limit x and y to stay within the max boundary
                x = max(-max_position, min(x, max_position))
                y = max(-max_position, min(y, max_position))

                # Update angle based on velocity and adjust by -90 degrees
                angle = math.degrees(math.atan2(-vy, vx)) - 90
                time += dt

            # Rotate and draw the rocket as a rectangle
            rotated_rocket = pygame.transform.rotate(rocket_surface, angle)
            rocket_rect = rotated_rocket.get_rect(center=(int(x), int(y)))
            screen.blit(rotated_rocket, rocket_rect.topleft)

            pygame.display.flip()
            pygame.time.delay(int(dt * 1000))

        pygame.display.flip()

# Exit pygame
pygame.quit()
