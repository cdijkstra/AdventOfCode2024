import re
from collections import namedtuple
from itertools import combinations


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return [line.strip() for line in file]


Coordinate = namedtuple("Coordinate", ["x", "y"])


def find_antennas_and_locations(grid):
    # Dictionary to hold the antennas and their locations
    antenna_dict = {}

    # Regex pattern to match all alphanumerical antennas
    pattern = r"[a-zA-Z0-9]"

    # Iterate over each row in the grid and process regex matches
    for row_index, row in enumerate(grid):
        for match in re.finditer(pattern, row):
            col_index = match.start()  # Extract the index of the match
            # Add the antenna symbol and its location (1-indexed) to the dictionary
            if match.group() not in antenna_dict:
                antenna_dict[match.group()] = []
            antenna_dict[match.group()].append(Coordinate(x=row_index, y=col_index))

    return antenna_dict


def find_antinodes(grid):
    antenna_locs = find_antennas_and_locations(grid)
    antinodes = []
    for antenna, locations in antenna_locs.items():
        all_pairs = list(combinations(locations, 2))

        for pair in all_pairs:
            # LHS
            low_x = pair[1].x - 2 * (pair[1].x - pair[0].x)
            low_y = pair[1].y - 2 * (pair[1].y - pair[0].y)
            # print("Low", low_x, low_y)
            if low_x >= 0 and low_y >= 0 and low_x < len(grid) and low_y < len(grid[0]):
                antinodes.append(Coordinate(x=low_x, y=low_y))

            # RHS
            high_x = pair[0].x - 2 * (pair[0].x - pair[1].x)
            high_y = pair[0].y - 2 * (pair[0].y - pair[1].y)
            # print("High", pair, high_x, high_y)

            if (
                high_x >= 0
                and high_y >= 0
                and high_x < len(grid)
                and high_y < len(grid[0])
            ):
                antinodes.append(Coordinate(x=high_x, y=high_y))

    unique_antinodes = set(antinodes)
    return len(unique_antinodes)


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    assert find_antinodes(grid) == 14

    grid = process_file("data.txt")
    print("Part 1:", find_antinodes(grid))
