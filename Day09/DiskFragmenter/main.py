import itertools
from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["min", "max"])


def process_file(filename):
    with open(filename, "r") as file:
        return file.readline()


def calculate(instructions):
    grid = []
    for idx, instruction in enumerate(instructions):
        entry = str(idx // 2) if idx % 2 == 0 else "."
        grid.extend(itertools.repeat(entry, int(instruction)))

    while "." in grid:
        grid[grid.index(".")] = grid.pop()

    return sum(int(grid[idx]) * idx for idx in range(len(grid)))


def calculate2(instructions):
    grid = []
    for idx, instruction in enumerate(instructions):
        entry = str(idx // 2) if idx % 2 == 0 else "."
        grid.extend(itertools.repeat(entry, int(instruction)))

    # File IDs in decreasing order
    unique_files = sorted(
        set(int(value) for value in grid if value != "."), reverse=True
    )
    file_indices = {
        file_id: Coordinate(min=min(indices), max=max(indices))
        for file_id in unique_files
        if (indices := [idx for idx, value in enumerate(grid) if value == str(file_id)])
    }

    # Loop through files in reversed file ID order
    for file_id, file_indices in file_indices.items():
        file_size = file_indices.max - file_indices.min + 1

        for i in range(file_indices.max):
            if not all(grid[j] == "." for j in range(i, i + file_size)):
                continue

            # Move file using slicing
            grid[i : i + file_size] = [str(file_id)] * file_size
            grid[file_indices.min : file_indices.min + file_size] = ["."] * file_size
            break

    return sum(int(grid[idx]) * idx for idx in range(len(grid)) if grid[idx] != ".")


if __name__ == "__main__":
    instructions = process_file("dummydata.txt")
    assert calculate(instructions) == 1928
    assert calculate2(instructions) == 2858

    instructions = process_file("data.txt")
    print("Part 1", calculate(instructions))
    print("Part 2", calculate2(instructions))
