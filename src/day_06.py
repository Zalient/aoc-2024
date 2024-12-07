from numpy import array
from collections import defaultdict


TURN_RIGHT = array([[0, 1], [-1, 0]])
OBSTACLE = '#'
EMPTY = '.'


class Dir:
    N = array((-1, 0))  # North
    E = array((0, 1))   # East
    S = array((1, 0))   # South
    W = array((0, -1))  # West


def parse(lines):
    map_grid = []
    start_pos = None
    start_dir = None
    direction_dict = {'^': Dir.N, '>': Dir.E, 'v': Dir.S, '<': Dir.W}
    
    for r, line in enumerate(lines):
        row = []
        for c, char in enumerate(line):
            if char in direction_dict:
                start_pos = array((r, c))
                start_dir = direction_dict[char]
                # Replace guard's position with an empty space
                row.append('.')
            else:
                row.append(char)
        map_grid.append(row)
    return map_grid, start_pos, start_dir


def turn_right(dir):
    return TURN_RIGHT @ dir


# Check for repeated configuration
def in_loop(configurations, pos, dir):
    return tuple(dir) in configurations[tuple(pos)]


def simulate_patrol(map_grid, pos, dir):
    configurations = defaultdict(set)
    
    # Stop only when next position will take guard out of grid
    while in_bounds(map_grid, next_pos := pos + dir):
        # Change configuration (either position or direction)
        if (map_grid[next_pos[0]][next_pos[1]] != OBSTACLE):
            pos = next_pos
        else:
            dir = turn_right(dir)
        # After moving, check if in repeated configuration 
        if in_loop(configurations, pos, dir):
            return None  # Stop if a configuration repeats
        configurations[tuple(pos)].add(tuple(dir))
    return configurations


def in_bounds(map_grid, pos):
    rows, cols = len(map_grid), len(map_grid[0])
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols


# Count number of distinct positions visited
def part_1(map_grid, start_pos, start_dir):
    configurations = simulate_patrol(map_grid, start_pos, start_dir)
    if configurations == None:
        return None
    return len(configurations.keys())


# Count all possible positions for adding a new obstacle that causes a loop
def part_2(map_grid, start_pos, start_dir):
    configurations = simulate_patrol(map_grid, start_pos, start_dir)
    if configurations is None:
        return 0  # If there is already a loop don't add any obstacles
    possible_positions = 0

    # Check all empty positions for where obstacles can be added
    for r in range(len(map_grid)):
        for c in range(len(map_grid[0])):
            if (map_grid[r][c] == EMPTY 
            and (r, c) in configurations.keys()
            and (r, c) != tuple(start_pos)):
                # Temporarily place an obstacle at (r, c) and do simulation
                map_grid[r][c] = OBSTACLE
                if simulate_patrol(map_grid, start_pos, start_dir) == None:
                    possible_positions += 1
                map_grid[r][c] = EMPTY  # Restore original state
    return possible_positions


