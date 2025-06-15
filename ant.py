import pygame
import numpy as np

class Ant:
    def __init__(self):
        # randomly generate a position for the ant
        self.position_x = 600.0 #np.random.uniform(0, 1175)
        self.position_y = 340.0 #np.random.uniform(0, 675)
        self.position = np.array([self.position_x, self.position_y])
        self.angle = 0 #np.random.randint(0, 360)
        self.feromone_type = None
        self.objects_found = {}

    def move(self, delta_time, speed=200):  # speed = pixels per second
        # Movement direction based on angle
        direction_vector = np.array([np.cos(np.radians(self.angle)), np.sin(np.radians(self.angle))])

        # Movement in pixels
        movement = direction_vector * speed * delta_time
        old_position = self.position.copy()
        self.position += movement
        if self.position[0] < 0 or self.position[0] > 1175 or self.position[1] < 0 or self.position[1] > 675:
            # If the ant goes out of bounds, revert to old position
            self.position = old_position
            # Reverse direction
            self.angle = (self.angle + 180) % 360

        # Random change in angle
        self.angle += np.random.randint(-5, 6)
        self.angle %= 360  # Keep angle in range

    def update_pheromones(ants, evaporation=0.5, Q=100.0):
        pass

    def draw(self, screen):
        # create an ant from the sprite that i downloaded
        # and draw it to the screen at position (100, 100)
        ant_image = pygame.image.load("ant.png").convert_alpha()  # Load the ant image
        ant_image = pygame.transform.scale(ant_image, (50, 50))  # Scale the image to a suitable size
        ant_image = pygame.transform.rotate(ant_image, (self.angle - 90) % 360)  # Rotate the image based on the ant's angle
        ant_rect = ant_image.get_rect(topleft=self.position)  # Create a rect for positioning

        screen.blit(ant_image, ant_rect)  # Draw the ant image to the screen