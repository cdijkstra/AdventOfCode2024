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


def traverse_trailhead_path(coordinate: Coordinate):
    if coordinate.value == 9:
        return [coordinate]

    destinations = []  # Initialize path count
    for neighbor in find_neighbors(coordinate):
        if neighbor.value == coordinate.value + 1:
            destinations += traverse_trailhead_path(neighbor)

    return destinations


def traverse_rating_path(coordinate: Coordinate):
    if coordinate.value == 9:
        return 1

    destinations = 0  # Initialize path count
    for neighbor in find_neighbors(coordinate):
        if neighbor.value == coordinate.value + 1:
            destinations += traverse_rating_path(neighbor)

    return destinations


def calculate_trailheads(grid):
    trailhead = 0
    for zero_coordinates in find_zeroes(grid):
        destinations = traverse_trailhead_path(zero_coordinates)
        trailhead += len(set(destinations))
    return trailhead


def calculate_rating(grid):
    rating = 0
    for zero_coordinates in find_zeroes(grid):
        destinations = traverse_rating_path(zero_coordinates)
        rating += destinations
    return rating


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
