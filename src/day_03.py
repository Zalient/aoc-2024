import re
from enum import StrEnum


class Conditional(StrEnum):
    DO = "do"
    DONT = "don't"


def parse(lines):
    return "".join(lines)


def find_mul_pairs(corrupted_memory, conditional=False):
    if not conditional:
        return re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", corrupted_memory)
    
    data = re.findall(r"(do|don't)\(\)|mul\((\d{1,3}),(\d{1,3})\)", corrupted_memory)
    mul_pairs = []
    for flag, n, m in data:
        if flag == Conditional.DO:
            conditional = True
        elif flag == Conditional.DONT:
            conditional = False
        if conditional and n and m:
            mul_pairs.append((n, m))
    return mul_pairs


def part_1(corrupted_memory):
    return sum(int(n) * int(m) for n, m in find_mul_pairs(corrupted_memory))


def part_2(corrupted_memory):
    return sum(int(n) * int(m) for n, m in find_mul_pairs(corrupted_memory, True))
