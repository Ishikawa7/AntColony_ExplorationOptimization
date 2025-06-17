import pygame

class Pheromone:
    def __init__(self, pheromone_type, position):
        self.type = None  # Type of pheromone (0 for explore, 1 for food)
        self.position = None  # Position of the pheromone
        self.intensity = 1.0  # Initial intensity of the pheromone
        self.radius = 2.5  # Radius of the pheromone effect

        self.type = pheromone_type
        self.position = position + (15, 15)  # Ensure position is a copy of the input tuple
        self.intensity = 1.0
        self.color = (255, 0, 0) if self.type == 0 else (0, 255, 0)
        # create a rect for the pheromone
        self.rect = pygame.Rect(position[0] - self.radius, position[1] - self.radius, self.radius * 2, self.radius * 2)

    def draw_update(self, screen, delta_time, evaporation_rate=0.1):
        # Decrease the intensity of the pheromone over time
        self.intensity -= evaporation_rate * delta_time
        if self.intensity < 0:
            self.intensity = 0
        # Update the color based on intensity
        self.color = (
            int(self.color[0] * (1 + self.intensity ** 0.5)),
            int(self.color[1] * (1 + self.intensity ** 0.5)),
            int(self.color[2] * (1 + self.intensity ** 0.5)),
        )
        # if color values exceed 255, cap them at 255
        self.color = tuple(min(255, c) for c in self.color)
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

    def is_active(self):
        # Check if the pheromone is still active based on its intensity
        return self.intensity > 0
