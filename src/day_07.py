from operator import mul, add
from math import log10, floor


def parse(lines):
    return ((int(line.split(": ")[0]), 
             list(map(int, line.split(": ")[1].split()))) for line in lines)


# Apply operators and return list of results
def apply_operators(target, lhs, rhs, operators):
    for operator in operators:
        new_lhs = operator(lhs, rhs[0])
        # Go down feasible branches in application tree 
        if new_lhs > target:  # Early exit if result exceeds target
            continue
        elif new_rhs := rhs[1:]:  # If more numbers remain
            yield from apply_operators(target, new_lhs, new_rhs, operators)
        else:  # Base case: No more numbers remain
            yield new_lhs


# Sum target values for equations where the target value can be reached
def valid_target_sum(equations, operators):
    return sum(target for target, numbers in equations if target in 
               apply_operators(target, numbers[0], numbers[1:], operators))


# Determine what power of 10 to multiply left by to concatenate it with right
def concat(left, right):
    return left * 10 ** floor(log10(right) + 1) + right


def part_1(equations):
    return valid_target_sum(equations, (mul, add))


def part_2(equations):
    return valid_target_sum(equations, (concat, mul, add))

