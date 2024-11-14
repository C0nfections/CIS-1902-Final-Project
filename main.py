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
TILE_SIZE = 200
TILE_PADDING = 4
TILE_COLORS = {
    'background': (156, 139, 124),
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
FONT = pygame.font.Font(None, 80)

grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
game_won = False

def draw_grid():
    screen.fill(TILE_COLORS['background'])
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = grid[row][col]
            color = TILE_COLORS.get(value, TILE_COLORS['blank'])
            rect = pygame.Rect(
                col * TILE_SIZE + TILE_PADDING,
                row * TILE_SIZE + TILE_PADDING,
                TILE_SIZE - 2 * TILE_PADDING,
                TILE_SIZE - 2 * TILE_PADDING
            )
            pygame.draw.rect(screen, color, rect)
            
            if value != 0:
                text = FONT.render(str(value), True, (0, 0, 0))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def add_random_tile():
    empty_tiles = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if grid[r][c] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        grid[row][col] = 4 if random.random() > 0.9 else 2

def slide(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (GRID_SIZE - len(new_row))
    return new_row

def combine(row):
    global game_won
    for i in range(len(row) - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
            if row[i] == 2048: # win condition!
                game_won = True 
    return row

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def move_left():
    global grid
    for i in range(GRID_SIZE):
        grid[i] = slide(grid[i])
        grid[i] = combine(grid[i])
        grid[i] = slide(grid[i])

def move_right():
    global grid
    for i in range(GRID_SIZE):
        grid[i] = slide(grid[i][::-1])
        grid[i] = combine(grid[i])
        grid[i] = slide(grid[i])
        grid[i] = grid[i][::-1]

def move_up():
    global grid
    grid = transpose(grid)
    move_left()
    grid = transpose(grid)

def move_down():
    global grid
    grid = transpose(grid)
    move_right()
    grid = transpose(grid)

def direction_handler():
    if event.type == pygame.KEYDOWN:
        moved = False
        if event.key == pygame.K_LEFT:
            move_left()
            moved = True
        elif event.key == pygame.K_RIGHT:
            move_right()
            moved = True
        elif event.key == pygame.K_UP:
            move_up()
            moved = True
        elif event.key == pygame.K_DOWN:
            move_down()
            moved = True

        if moved:
            add_random_tile()
            if game_won:
                print("You win!") # need to display win message
            if check_game_over():
                print("Game Over") # need to display lose message

def check_game_over():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return False
            if j < GRID_SIZE - 1 and grid[i][j] == grid[i][j + 1]:
                return False
            if i < GRID_SIZE - 1 and grid[i][j] == grid[i + 1][j]:
                return False
    return True

# adding two random tiles to start the game
add_random_tile()
add_random_tile()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # user clicked the close button
            running = False

        direction_handler()
    
    draw_grid()

    pygame.display.flip()

pygame.quit()
