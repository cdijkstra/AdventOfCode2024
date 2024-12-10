from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y", "value"])


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        grid = [
            [
                Coordinate(x=row_index, y=col_index, value=int(value))
                for col_index, value in enumerate(line.strip())
            ]
            for row_index, line in enumerate(file)
        ]
    return grid


def find_zeroes(grid):
    return [coord for row in grid for coord in row if coord.value == 0]


def find_neighbors(coordinate: Coordinate) -> Coordinate:
    neighbors = []
    if coordinate.x > 0:
        neighbors.append(grid[coordinate.x - 1][coordinate.y])
    if coordinate.x < len(grid) - 1:
        neighbors.append(grid[coordinate.x + 1][coordinate.y])
    if coordinate.y > 0:
        neighbors.append(grid[coordinate.x][coordinate.y - 1])
    if coordinate.y < len(grid[0]) - 1:
        neighbors.append(grid[coordinate.x][coordinate.y + 1])

    return neighbors


def traverse_path(coordinate: Coordinate, return_paths=True):
    """
    Recursively traverse paths.

    :param coordinate: The current Coordinate to process.
    :param return_paths: Whether to return full paths (list of coordinates) or just path counts (integer).
    :return: A list of valid paths or a path count based on `return_paths`.
    """
    if coordinate.value == 9:
        return [coordinate] if return_paths else 1

    destinations = [] if return_paths else 0  # Initialize path count
    for neighbor in find_neighbors(coordinate):
        if neighbor.value == coordinate.value + 1:
            destinations += traverse_path(neighbor, return_paths)

    return destinations


def calculate_trailheads(grid):
    return sum(
        len(
            set(
                traverse_path(zero_coordinates)
            )  # Use len(set)) to remove duplicates and find amount of destinations
        )
        for zero_coordinates in find_zeroes(grid)
    )


def calculate_rating(grid):
    return sum(
        traverse_path(zero_coordinates, return_paths=False)
        for zero_coordinates in find_zeroes(grid)
    )


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    assert calculate_trailheads(grid) == 1
    grid = process_file("dummydata2.txt")
    assert calculate_trailheads(grid) == 36
    assert calculate_rating(grid) == 81

    grid = process_file("data.txt")
    print("Part 1:", calculate_trailheads(grid))
    print("Part 2:", calculate_rating(grid))
