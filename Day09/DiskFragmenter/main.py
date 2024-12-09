import itertools


def process_file(filename):
    with open(filename, "r") as file:
        return file.readline()


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

    free_spans = []
    start = None
    for i, char in enumerate(grid):
        if char == "." and start is None:
            start = i
        elif char != "." and start is not None:
            free_spans.append((start, i - 1))
            start = None
    print("Free spans", free_spans)

    unique_files = sorted(
        set(grid) - {"."}, reverse=True
    )  # File IDs in decreasing order

    print("Unique files", unique_files)
    for file_id in unique_files:
        indices = [idx for idx, value in enumerate(grid) if value == file_id]
        file_size = len(indices)
        if not any(start < indices[0] for start, _ in free_spans):
            break

        print("Unique file", file_id)
        for i, (start, end) in enumerate(free_spans):
            print("Start", start, "End", end)
            if not (file_size <= (end - start + 1)):
                continue

            for i, idx in enumerate(indices):
                grid[start + i] = file_id
                grid[idx] = "."

            if file_size == (end - start + 1):
                free_spans.pop(i)
                print("Pop entry with start", start)
                break
            else:
                print(free_spans)
                free_spans[i] = (start + file_size, end)
                print(
                    "added file_size ",
                    file_size,
                    " to start",
                    start,
                    "and index: ",  # Update free_spans after breaking out of the inner loop
                    i,
                )
                print(free_spans)
            break
    print(grid)
    return sum(int(grid[idx]) * idx for idx in range(len(grid)))


if __name__ == "__main__":
    instructions = process_file("dummydata.txt")
    assert calculate(instructions) == 1928
    assert calculate2(instructions) == 2858

    # instructions = process_file("data.txt")
    # print("Part 1", calculate(instructions))
