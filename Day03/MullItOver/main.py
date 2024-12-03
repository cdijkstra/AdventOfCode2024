import re


def process_file(filename):
    """Read the file as single string"""
    with open(filename, "r") as file:
        return file.read()


def calculate_multiplication(instruction):
    matches = re.findall(r"mul\(\d+,\d+\)", instruction)
    return sum(
        int(left) * int(right)
        for match in matches
        for left, right in [match.strip("mul()").split(",")]
    )


# Main execution
if __name__ == "__main__":
    instructions = process_file("dummydata.txt")
    assert calculate_multiplication(instructions) == 161
    # # assert calculate_dampened_safety_score(report) == 4

    # # Process the file once
    instructions = process_file("data.txt")
    print(instructions)
    # # Part 1: Calculate generic safety
    print("Part 1:", calculate_multiplication(instructions))
