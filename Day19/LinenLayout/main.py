def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        patterns, designs = file.read().split("\n\n")
        patterns = [pattern.strip() for pattern in patterns.split(",")]
        designs = designs.split("\n")
        return patterns, designs


def can_construct(design, original_design, patterns):
    """
    Recursive function to find out if string can be constructed from patterns
    """
    if len(design) == 0:
        return True

    for pattern in patterns:
        if design.startswith(pattern) and can_construct(
            design[len(pattern) :], original_design, patterns
        ):
            return True

    # If no matches work, return False
    return False


def find_designs(patterns, designs):
    count = 0
    for design in designs:
        patterns_contained = [s for s in patterns if s in design]
        if not can_construct(design, design, patterns_contained):
            continue
        count += 1
    return count


# Main execution
if __name__ == "__main__":
    patterns, designs = process_file("dummydata.txt")
    assert find_designs(patterns, designs) == 6

    patterns, designs = process_file("data.txt")
    print("Part 1:", find_designs(patterns, designs))
