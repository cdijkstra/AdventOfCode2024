def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        patterns, designs = file.read().split("\n\n")
        patterns = [pattern.strip() for pattern in patterns.split(",")]
        designs = designs.split("\n")
        return patterns, designs


def can_construct(design, patterns):
    """
    Recursive function to find out if string can be constructed from patterns
    """
    if len(design) == 0:
        return True

    for pattern in patterns:
        if design.startswith(pattern) and can_construct(
            design[len(pattern) :], patterns
        ):
            return True

    # If no matches work, return False
    return False


def construct_possibilities(design, patterns):
    """
    Recursive function to find out in how many ways the design can be created
    We use memoization to ensure we don't calculate the same thing twice
    """
    if design in memo:
        return memo[design]

    if len(design) == 0:
        return 1

    count = 0
    for pattern in patterns:
        if design.startswith(pattern):
            count += construct_possibilities(design[len(pattern) :], patterns)

    memo[design] = count
    # If no matches work, return False
    return count


def find_designs(patterns, designs):
    return sum(
        1
        for design in designs
        if can_construct(
            design, [s for s in patterns if s in design]
        )  # [s for s in patterns if s in design] gives all substring that occur in design
    )


def find_combinatorics(patterns, designs):
    count = sum(
        construct_possibilities(design, [s for s in patterns if s in design])
        for design in designs
    )
    return count


# Main execution
if __name__ == "__main__":
    memo = {}
    patterns, designs = process_file("dummydata.txt")
    assert find_designs(patterns, designs) == 6
    assert find_combinatorics(patterns, designs) == 16

    patterns, designs = process_file("data.txt")
    print("Part 1:", find_designs(patterns, designs))
    memo = {}
    print("Part 2:", find_combinatorics(patterns, designs))
