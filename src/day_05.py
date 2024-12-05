from collections import defaultdict


# Split the input into rules and updates
def parse(lines):
    split_index = lines.index("")
    rules = defaultdict(set)
    for rule in lines[:split_index]:
        key_page, page_after = map(int, rule.split('|'))
        rules[key_page].add(page_after)
    # Updates - list of lists (uses generator for lazy evaluation)
    updates = (map(int, line.split(',')) for line in lines[split_index + 1:])
    return rules, updates


# Check whether a single page is in correct position (based on rules)
def is_ordered_page(rules, page, pages_after):
    return all(page_after in rules[page] for page_after in pages_after)


# Check whether a single update is valid
def is_valid_update(rules, update):     
    return all(
        is_ordered_page(rules, key_page, update[i + 1:])
        for i, key_page in enumerate(update)
    )


# Sum the middle page value of all valid updates
def part_1(rules, updates):
    middles_sum = 0
    for update in updates:
        update = list(update)
        if is_valid_update(rules, update):
            middles_sum += update[len(update) // 2]
    return middles_sum


# Fix incorrectly-ordered updates
def part_2(rules, updates):
    fixed_updates = []
    for update in updates:
        update = list(update)
        if is_valid_update(rules, update):
            continue
        fixed_update = []
        while update:
            for i, page in enumerate(update):
                # Only add the page if all its dependencies are satisfied
                if is_ordered_page(rules, page, update[i + 1:]):
                    fixed_update.append(page)
                    update.remove(page)
                    break
        fixed_updates.append(fixed_update)
    return part_1(rules, fixed_updates)
        