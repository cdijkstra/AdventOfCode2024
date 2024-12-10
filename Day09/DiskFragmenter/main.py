import itertools
from collections import namedtuple


def process_file(filename):
    with open(filename, "r") as file:
        return file.readline()


Coordinate = namedtuple("Coordinate", ["min", "max"])


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
    unique_files = sorted(set(grid) - {"."}, reverse=True)
    file_indices = {
        file_id: Coordinate(min=min(indices), max=max(indices))
        for file_id in unique_files
        if (indices := [idx for idx, value in enumerate(grid) if value == file_id])
    }

    # Find all free spans and put in array that will be updated
    free_spans = []
    start = None
    for i, char in enumerate(grid):
        if char == "." and start is None:
            start = i
        elif char != "." and start is not None:
            free_spans.append(Coordinate(min=start, max=i - 1))
            start = None

    # Loop through files in reversed file ID order
    for file_id, file_indices in file_indices.items():
        file_size = file_indices.max - file_indices.min + 1
        # Find first free span that is large enough

        filtered_span = next(
            (
                span
                for span in free_spans
                if span.min < file_indices.min and span.max - span.min + 1 >= file_size
            ),
            None,
        )

        if filtered_span is None:  # Continue if not found
            continue

        # Update grid by moving file
        for i in range(file_indices.max - file_indices.min + 1):
            grid[filtered_span.min + i] = file_id
            grid[file_indices.min + i] = "."

        # Update free_spans; remove dots that are filled by file
        if (
            filtered_span.max - filtered_span.min + 1 == file_size
        ):  # Remove if it fits exactly
            free_spans.remove(filtered_span)
        else:  # Otherwise update min coordinate of free span
            free_spans[free_spans.index(filtered_span)] = Coordinate(
                min=filtered_span.min + file_size, max=filtered_span.max
            )

        # Update free_spans; add dots where file used to be
        lhs_span = next(
            (span for span in free_spans if span.max == (file_indices.min - 1)), None
        )
        rhs_span = next(
            (span for span in free_spans if span.min == (file_indices.max + 1)), None
        )
        if lhs_span and rhs_span:
            free_spans.remove(lhs_span)
            free_spans.remove(rhs_span)
            free_spans.append(Coordinate(min=lhs_span.min, max=rhs_span.max))
        elif lhs_span:
            free_spans[free_spans.index(lhs_span)] = Coordinate(
                min=lhs_span.min, max=file_indices.max
            )
        elif rhs_span:
            free_spans[free_spans.index(rhs_span)] = Coordinate(
                min=file_indices.min, max=rhs_span.max
            )
        else:  # No adjacent spans, add a new span
            free_spans.append(Coordinate(min=file_indices.min, max=file_indices.max))

        free_spans.sort(key=lambda span: span.min)
    return sum(int(grid[idx]) * idx for idx in range(len(grid)) if grid[idx] != ".")


if __name__ == "__main__":
    instructions = process_file("dummydata.txt")
    assert calculate(instructions) == 1928
    assert calculate2(instructions) == 2858

    instructions = process_file("data.txt")
    print("Part 1", calculate(instructions))
    # 6510130564589 is too high
    print("Part 2", calculate2(instructions))
