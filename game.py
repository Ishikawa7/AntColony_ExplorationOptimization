# Example file showing a basic pygame "game loop"
import pygame
import ant

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

my_ant = ant.Ant()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    delta_time = clock.tick(60) / 1000.0  # Seconds

    # RENDER YOUR GAME HERE
    # create an instance of the Ant class
    my_ant.move(delta_time)  # Move the ant
    my_ant.draw(screen)  # Draw the ant on the screen


    # flip() the display to put your work on screen
    pygame.display.flip()

pygame.quit()