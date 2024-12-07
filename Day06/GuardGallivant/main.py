from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return [line.strip() for line in file]


def obtain_new_coordinates(coord, dir):
    if dir == "N":
        return Coordinate(coord.x - 1, coord.y)
    elif dir == "E":
        return Coordinate(coord.x, coord.y + 1)
    elif dir == "S":
        return Coordinate(coord.x + 1, coord.y)
    elif dir == "W":
        return Coordinate(coord.x, coord.y - 1)


def invalid_coordinates(coord, max_x, max_y):
    return coord.x < 0 or coord.y < 0 or coord.x >= max_x or coord.y >= max_y


def make_turn(dir):
    return {
        "N": "E",
        "E": "S",
        "S": "W",
        "W": "N",
    }[dir]


def find_path(grid):
    coordinates = next(
        Coordinate(x, y)
        for x, row in enumerate(grid)
        for y, char in enumerate(row)
        if char == "^"
    )
    dir = "N"
    visited = [coordinates]
    while True:
        new_coordinates = obtain_new_coordinates(coordinates, dir)
        if invalid_coordinates(new_coordinates, len(grid), len(grid[0])):
            break

        if grid[new_coordinates.x][new_coordinates.y] == "#":
            dir = make_turn(dir)
        else:
            coordinates = new_coordinates
            if coordinates not in visited:
                visited.append(coordinates)

    return len(visited)


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    assert find_path(grid) == 41

    grid = process_file("data.txt")
    print("Part 1", find_path(grid))
