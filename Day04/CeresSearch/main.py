def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return file.read().splitlines()


def find_word(grid, word):
    """Find the word in the grid."""
    return (
        find_horizontal_word(grid, word)
        + find_vertical_word(grid, word)
        + find_diagonal_word(grid, word)
    )


def find_horizontal_word(grid, word):
    result = [row.count(word) + row.count(word[::-1]) for row in grid]
    return sum(result)


def find_vertical_word(grid, word):
    transposed = ["".join(col) for col in zip(*grid)]
    result = [col.count(word) + col.count(word[::-1]) for col in transposed]
    return sum(result)


def find_diagonal_word(grid, word):
    """Find the word in the grid."""
    rows = len(grid)
    cols = len(grid[0])
    occurrences = 0
    word_len = len(word)

    # Check diagonals (top-left to bottom-right)
    for row in range(rows):
        for col in range(cols):
            if not (row + word_len <= rows and col + word_len <= cols):
                continue

            diagonal = [grid[row + i][col + i] for i in range(word_len)]
            if "".join(diagonal) not in {word, word[::-1]}:
                continue
            occurrences += 1

    # Check diagonals (top-right to bottom-left)
    for row in range(rows):
        for col in range(cols):
            if not (row + word_len <= rows and col - word_len + 1 >= 0):
                continue

            diagonal = [grid[row + i][col - i] for i in range(word_len)]
            if "".join(diagonal) not in {word, word[::-1]}:
                continue
            occurrences += 1

    return occurrences


def find_mas_occurrence(grid):
    occurrences = 0
    for row in range(len(grid) - 2):
        for col in range(len(grid[0]) - 2):
            if (
                grid[row][col] in {"M", "S"}
                and grid[row][col + 2] in {"M", "S"}
                and grid[row + 1][col + 1] == "A"
                and grid[row + 2][col] in {"M", "S"}
                and grid[row + 2][col + 2] in {"M", "S"}
            ):
                # Possible match found, now check if it contains M and S twice
                chars = [
                    grid[row][col],
                    grid[row][col + 2],
                    grid[row + 2][col],
                    grid[row + 2][col + 2],
                ]
                # And that M and S are diagonally adjacent
                if chars.count("M") == 2 and {
                    "M",
                    "S",
                }.issubset([chars[0], chars[3]]):
                    occurrences += 1
    return occurrences


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    assert find_word(grid, "XMAS") == 18
    assert find_mas_occurrence(grid) == 9

    # Process the file once
    grid = process_file("data.txt")

    # Part 1: Count XMAS
    print("Xmas part 1:", find_word(grid, "XMAS"))
    print("Xmas part 2:", find_mas_occurrence(grid))
