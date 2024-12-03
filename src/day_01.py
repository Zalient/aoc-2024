from collections import Counter


def parse(lines):
    return zip(*[map(int, line.split("   ")) for line in lines])


def part_1(list_1, list_2):
    return sum(abs(loc_id_1 - loc_id_2) for loc_id_1, loc_id_2 in zip(sorted(list_1), sorted(list_2)))


def part_2(list_1, list_2):
    return sum(loc_id_1 * Counter(list_2)[loc_id_1] for loc_id_1 in list_1)
