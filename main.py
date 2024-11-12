import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 800))
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

GRID_SIZE = 4
TILE_COLORS = {
    'blank': (189, 175, 160),
    2: (238, 227, 218),
    4: (238, 225, 206),
    8: (243, 178, 126),
    16: (246, 150, 107),
    32: (246, 125, 103),
    64: (246, 97, 71),
    128: (239, 207, 106),
    256: (237, 204, 97),
    512: (237, 210, 119),
    1024: (238, 207, 107),
    2048: (238, 205, 94)
}

grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def draw_grid():
    screen.fill(TILE_COLORS['blank'])
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            pygame.draw.rect(screen, (156, 139, 125), (i * 200, j * 200, 200, 200), 2)

def add_random_tile():
    empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        grid[row][col] = 4 if random.random() > 0.9 else 2

# adding two random tiles to start the game
add_random_tile()
add_random_tile()

running = True
while running:
    for event in pygame.event.get():
        # do shit here like draw stuff
        if event.type == pygame.QUIT: # user clicked the close button
            running = False

        direction_handler() # handles the key pressed
    
    draw_grid()

    pygame.display.flip()

pygame.quit()
