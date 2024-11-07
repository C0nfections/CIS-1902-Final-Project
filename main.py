import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("2048")

def direction_handler():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            print("Left arrow key pressed")
        if event.key == pygame.K_RIGHT:
            print("Right arrow key pressed")
        if event.key == pygame.K_UP:
            print("Up arrow key pressed")
        if event.key == pygame.K_DOWN:
            print("Down arrow key pressed")

running = True
while running:
    for event in pygame.event.get():
        # do shit here like draw stuff
        if event.type == pygame.QUIT: # user clicked the close button
            running = False

        direction_handler() # handles the key pressed

        pygame.display.flip()


