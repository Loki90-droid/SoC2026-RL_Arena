from constants import *
from utils import *

# Create empty grid

grid = []

for _ in range(ROWS):
    row = [EMPTY_CELL] * COLS
    grid.append(row)


# Player starting position
player_row = 5
player_col = 5


# Obstacles
obstacles = [(2,3),(4,4),(6,7),(8,2),(5,1)]

running = True
clear_screen()
for (obs_row, obs_col) in obstacles:
    grid[obs_row-1][obs_col-1] = OBSTACLE_CELL
grid[player_row-1][player_col-1] = PLAYER_CELL
print_grid(grid)
while running:
    # Reset grid
    direction = ""
    for row in range(ROWS):
        for col in range(COLS):
            grid[row][col] = EMPTY_CELL
    # Add obstacles
    for (obs_row, obs_col) in obstacles:
        grid[obs_row-1][obs_col-1] = OBSTACLE_CELL
    # Add player
    grid[player_row-1][player_col-1] = PLAYER_CELL

    # Take input and update position
    direction = input("Enter direction (w/a/s/d/exit): ")
    if direction not in ["w", "a", "s", "d", "exit"]:
        print("Invalid input. Please enter w/a/s/d/exit.")
        continue
    if direction == "exit":
        running = False
        break
    new_row, new_col = player_row, player_col
    if direction == "w":
        new_row -= 1
    elif direction == "s":
        new_row += 1
    elif direction == "a":
        new_col -= 1
    elif direction == "d":
        new_col += 1

    # Boundary checking
    if new_row < 1 or new_row > ROWS or new_col < 1 or new_col > COLS:
        print("Invalid Move: Out of bounds")
        continue
    # Obstacle collision
    if (new_row, new_col) in obstacles:
        print("Invalid Move: Obstacle")
        continue
    grid[player_row-1][player_col-1] = EMPTY_CELL
    player_row = new_row
    player_col = new_col
    grid[player_row-1][player_col-1] = PLAYER_CELL
    print_grid(grid)
