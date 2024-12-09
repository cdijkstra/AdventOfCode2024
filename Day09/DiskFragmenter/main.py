import itertools


def process_file(filename):
    with open(filename, "r") as file:
        return file.readline()


def calculate(instructions):
    grid = []
    for idx, instruction in enumerate(instructions):
        if idx % 2 == 0:
            entry = str(idx // 2)
            grid.extend(itertools.repeat(entry, int(instruction)))
        else:
            entry = "".join(".", instruction)
            grid.extend(entry)
        print(grid)

    while "." in grid:
        grid[grid.index(".")] = grid.pop()

    return sum(int(grid[idx]) * idx for idx in range(len(grid)))


if __name__ == "__main__":
    instructions = process_file("dummydata.txt")
    assert calculate(instructions) == 1928

    # instructions = process_file("data.txt")
    # print("Part 1", calculate(instructions))
