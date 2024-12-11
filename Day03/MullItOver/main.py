import re


def process_file(filename):
    """Read the file as single string"""
    with open(filename, "r") as file:
        return file.read()


def calculate_multiplication(jibberish):
    instructions = re.findall(r"mul\(\d+,\d+\)", jibberish)
    return sum(
        int(left) * int(right)
        for instruction in instructions
        for left, right in [instruction.strip("mul()").split(",")]
    )


def calculate_dos_multiplication(jibberish):
    pattern = r"(do\(\)|don't\(\)|mul\(\d+,\d+\))"
    instructions = re.findall(pattern, jibberish)
    result = 0
    do = True
    for instruction in instructions:
        if instruction == "do()":
            do = True
        elif instruction == "don't()":
            do = False
        elif do:
            left, right = map(int, instruction.strip("mul()").split(","))
            result += left * right
    return result


# Main execution
if __name__ == "__main__":
    instructions = process_file("dummydata.txt")
    assert calculate_multiplication(instructions) == 161
    instructions = process_file("dummydata2.txt")
    assert calculate_dos_multiplication(instructions) == 48

    # # Process the file once
    instructions = process_file("data.txt")
    # # Part 1: Calculate generic safety
    print("Part 1:", calculate_multiplication(instructions))
    print("Part 2:", calculate_dos_multiplication(instructions))
