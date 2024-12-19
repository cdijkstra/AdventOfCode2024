import re


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
        print("Possible", original_design)
        return True

    print(patterns)
    for pattern in patterns:
        print(design, pattern, design[len(pattern) :])
        if not design.startswith(pattern):
            continue
        return can_construct(design[len(pattern) :], original_design, patterns)

    # If no matches work, return False
    return False


# Main execution
if __name__ == "__main__":
    patterns, designs = process_file("dummydata.txt")
    count = 0
    for design in designs:
        patterns_contained = [s for s in patterns if s in design]
        print(design, patterns_contained)
        if not can_construct(design, design, patterns_contained):
            continue
        count += 1
    print(count)
