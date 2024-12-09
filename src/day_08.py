from collections import defaultdict
from itertools import combinations


def parse(lines):
    antennas = defaultdict(set)  # Map signal frequency to positions
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            # Only consider valid antenna signal frequencies (letters/digits)
            if char.isalnum(): 
                antennas[char].add(complex(r, c))
    bounds = complex(len(lines), len(lines[0]))
    return antennas, bounds


def in_bounds(bounds, pos):
    hi = 1
    return 0 <= pos.real < bounds.real and 0 <= pos.imag < bounds.imag


# Look through positions of coherent signal pairs to find antinodes
def find_antinodes(coherent_signals, bounds, start_step, max_step):
    for pos_1, pos_2 in combinations(coherent_signals, 2):
        dist = pos_1 - pos_2
        for pos, dir in [(pos_1, 1), (pos_2, -1)]:
            step = start_step
            while (in_bounds(bounds, antinode := pos + dist * dir * step)
                            and step <= max_step):
                step += 1
                yield antinode


def part_1(antennas, bounds):
    return len({antinode for coherent_signals in antennas.values() 
               for antinode in 
               find_antinodes(coherent_signals, bounds, 1, 1)})


def part_2(antennas, bounds):
    return len({antinode for coherent_signals in antennas.values() 
               for antinode in 
               find_antinodes(coherent_signals, bounds, 0, float('inf'))})