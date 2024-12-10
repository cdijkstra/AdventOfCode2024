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


def traverse_path(coordinate: Coordinate, history=[]):
    history.append(coordinate)

    if coordinate.value == 9:
        print("Made it, with history", history)
        return coordinate

    destinations = []  # Initialize path count
    for neighbor in find_neighbors(coordinate):
        if neighbor.value == coordinate.value + 1:
            destinations += traverse_path(neighbor, history[:])
    return destinations


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata2.txt")

    trailhead = 0
    for zero_coordinates in find_zeroes(grid):
        destinations = traverse_path(zero_coordinates)

        print("Destinations", destinations)
        trailhead += len(set(destinations)) / 3
    print(trailhead)
