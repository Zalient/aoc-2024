from collections import defaultdict


TURN_RIGHT = {
    (-1, 0): (0, 1),
    (0, 1): (1, 0),
    (1, 0): (0, -1),
    (0, -1): (-1, 0)
}
OBSTACLE = '#'
EMPTY = '.'


class Dir:
    N = (-1, 0)  # North
    E = (0, 1)   # East
    S = (1, 0)   # South
    W = (0, -1)  # West


def parse(lines):
    map_grid = []
    direction_dict = {'^': Dir.N, '>': Dir.E, 'v': Dir.S, '<': Dir.W}
    
    for r, line in enumerate(lines):
        row = []
        for c, char in enumerate(line):
            if char in direction_dict:
                start_pos = (r, c)
                start_dir = direction_dict[char]
                # Replace guard's position with an empty space
                row.append(EMPTY)
            else:
                row.append(char)
        map_grid.append(row)
    return map_grid, start_pos, start_dir


# Check for repeated configuration
def in_loop(configurations, pos, dir):
    return dir in configurations[pos]


def simulate_patrol(map_grid, pos, dir):
    configurations = defaultdict(set)
    
    # Stop only when next position will take guard out of grid
    while in_bounds(map_grid, next_pos := (pos[0] + dir[0], pos[1] + dir[1])):
        # Change configuration (either position or direction)
        if (map_grid[next_pos[0]][next_pos[1]] != OBSTACLE):
            pos = next_pos
        else:
            dir = TURN_RIGHT[dir]
        # After moving, check if in repeated configuration 
        if in_loop(configurations, pos, dir):
            return None  # Stop if a configuration repeats
        configurations[pos].add(dir)
    return configurations


def in_bounds(map_grid, pos):
    rows, cols = len(map_grid), len(map_grid[0])
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols


# Count number of distinct positions visited
def part_1(map_grid, start_pos, start_dir):
    return len(simulate_patrol(map_grid, start_pos, start_dir).keys())


# Count all possible positions for adding a new obstacle that causes a loop
def part_2(map_grid, start_pos, start_dir):
    configurations = simulate_patrol(map_grid, start_pos, start_dir)
    possible_positions = 0

    # Only positions in configurations need to be considered
    for position in configurations.keys():
        r, c = position[0], position[1]
        if (map_grid[r][c] == EMPTY and (r, c) != start_pos):
                # Temporarily place an obstacle at (r, c) and do simulation
                map_grid[r][c] = OBSTACLE
                if simulate_patrol(map_grid, start_pos, start_dir) == None:
                    possible_positions += 1
                map_grid[r][c] = EMPTY  # Restore original state
    return possible_positions


