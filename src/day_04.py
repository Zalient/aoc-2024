DIRS = [
    (1, 0),   # Down
    (0, 1),   # Right
    (1, 1),   # Down-Right
    (1, -1)  # Down-Left
]


def parse(lines):
    return lines


# Check that given a location and direction, the line created is in bounds
def in_bounds(start_pos, stop_pos, scale):
    if 0 <= start_pos[0] < scale[0] and 0 <= start_pos[1] < scale[1]:
        return (0 <= stop_pos[0] < scale[0] and 0 <= stop_pos[1] < scale[1])


def is_match(word_search, current_pos, dir, target_word):
    scale = (len(word_search), len(word_search[0]))
    stop_index = len(target_word) - 1
    stop_pos = (current_pos[0] + stop_index * dir[0], 
                    current_pos[1] + stop_index * dir[1])
    
    if in_bounds(current_pos, stop_pos, scale):
        word = ''.join([word_search[current_pos[0] + i * dir[0]]
                        [current_pos[1] + i * dir[1]] 
                        for i in range(len(target_word))])
        return word == target_word or word == target_word[::-1]


def part_1(word_search, target_word="XMAS", dirs=DIRS):
    count = 0
    rows, cols = len(word_search), len(word_search[0])

    for r in range(rows):
        for c in range(cols):
            for dir in dirs:
                if is_match(word_search, (r, c), dir, target_word):
                    count += 1
    return count


def part_2(word_search, target_word="MAS", dirs=DIRS[2:]):
    count = 0
    rows, cols = len(word_search), len(word_search[0])

    for r in range(rows):
        for c in range(cols):
            diagonal_count = 0
            for dir in dirs:
                opposite_dir = (-dir[0], -dir[1])
                starting_pos = (r + opposite_dir[0], c + opposite_dir[1])
                if is_match(word_search, starting_pos, dir, target_word):
                    diagonal_count += 1
            if diagonal_count == 2:
                count += 1
    return count