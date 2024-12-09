import itertools


def process_file(filename):
    with open(filename, "r") as file:
        return file.readline()


def calculate(instructions):
    grid = ""
    for idx in range(len(instructions)):
        if idx % 2 == 0:
            grid += "".join(itertools.repeat(str(int(idx / 2)), int(instructions[idx])))
        else:
            grid += "".join(itertools.repeat(".", int(instructions[idx])))

    # Now move stones to the left
    while grid.count(".") > 0:
        idx = grid.find(".")
        # Move last character to index idx
        grid = grid[:idx] + grid[-1] + grid[idx + 1 : -1]

    sum = 0
    for idx in range(len(grid)):
        sum += int(grid[idx]) * idx
    return sum


# Main execution
if __name__ == "__main__":
    instructions = process_file("dummydata.txt")
    assert calculate(instructions) == 1928

    # 91411296588 is too low
    instructions = process_file("data.txt")
    print("Part 1", calculate(instructions))
