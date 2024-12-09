import itertools
from collections import namedtuple


def process_file(filename):
    with open(filename, "r") as file:
        return file.readline()


Coordinate = namedtuple("Coordinate", ["min", "max"])


def calculate(instructions):
    grid = []
    for idx, instruction in enumerate(instructions):
        print(idx, instruction)
        entry = str(idx // 2) if idx % 2 == 0 else "."
        grid.extend(itertools.repeat(entry, int(instruction)))

    print(grid)
    while "." in grid:
        grid[grid.index(".")] = grid.pop()

    return sum(int(grid[idx]) * idx for idx in range(len(grid)))


def calculate2(instructions):
    grid = []
    for idx, instruction in enumerate(instructions):
        print(idx, instruction)
        entry = str(idx // 2) if idx % 2 == 0 else "."
        grid.extend(itertools.repeat(entry, int(instruction)))

    # File IDs in decreasing order
    unique_files = sorted(set(grid) - {"."}, reverse=True)

    print("Unique files", unique_files)
    file_indices = {
        file_id: Coordinate(min=min(indices), max=max(indices))
        for file_id in unique_files
        if (indices := [idx for idx, value in enumerate(grid) if value == file_id])
    }

    print("File indices", file_indices)

    free_spans = []
    start = None
    for i, char in enumerate(grid):
        if char == "." and start is None:
            start = i
        elif char != "." and start is not None:
            free_spans.append(Coordinate(min=start, max=i - 1))
            start = None

    print("Free spans", free_spans)
    for file_id, file_indices in file_indices.items():
        file_size = file_indices.max - file_indices.min + 1
        filtered_span = next(
            (
                span
                for span in free_spans
                if span.min <= file_indices.min and span.max - span.min + 1 >= file_size
            ),
            None,
        )

        print(
            "Filted span",
            filtered_span,
            "for file indices",
            file_indices,
            "and file size",
            file_size,
        )
        if filtered_span is None:
            continue

        for i in range(filtered_span.min, filtered_span.max):
            grid[i] = file_id
        for i in range(file_indices.min, file_indices.max + 1):
            grid[i] = "."

        if filtered_span.max - filtered_span.min == file_size:
            free_spans.remove(filtered_span)
        else:
            print("Before updating", free_spans)
            free_spans[free_spans.index(filtered_span)] = Coordinate(
                min=filtered_span.min + file_size - 1, max=filtered_span.max
            )
            print("After updating", free_spans)

        print(grid)

    return 5


if __name__ == "__main__":
    instructions = process_file("dummydata.txt")
    assert calculate(instructions) == 1928
    assert calculate2(instructions) == 2858

    # instructions = process_file("data.txt")
    # print("Part 1", calculate(instructions))
