# Example file showing a basic pygame "game loop"
import pygame
import ant
import numpy as np

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

my_ant = ant.Ant()
# generate 10 random coordinates for the circles
circles_positions = [(np.random.randint(20, 1260), np.random.randint(20, 700)) for _ in range(10)]
# check if the circles are not overlapping each other
for i in range(len(circles_positions)):
    for j in range(i + 1, len(circles_positions)):
        while np.linalg.norm(np.array(circles_positions[i]) - np.array(circles_positions[j])) < 40:
            circles_positions[j] = (np.random.randint(20, 1260), np.random.randint(20, 700))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    # Draw 10 circles at random positions
    for pos in circles_positions:
        pygame.draw.circle(screen, "purple", pos, 20)
    delta_time = clock.tick(60) / 1000.0  # Seconds

    # RENDER YOUR GAME HERE
    # create an instance of the Ant class
    my_ant.move(delta_time)  # Move the ant
    my_ant.draw(screen)  # Draw the ant on the screen


    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()