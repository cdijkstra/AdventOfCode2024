import copy
from collections import namedtuple
from itertools import count

Coordinate = namedtuple("Coordinate", ["x", "y"])


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return [list(line.strip()) for line in file]


def find_flowers(grid):
    return set(value for row in grid for value in row)


def count_flowers(grid, flower):
    return [value for row in grid for value in row].count(flower)


def find_coordinates(grid, flower):
    """Find all coordinates of a specific value in the 2D array."""
    coordinates = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == flower:
                coordinates.append(Coordinate(x=row_idx, y=col_idx))
    return coordinates


def find_perimeter(coordinates: Coordinate):
    """Find perimeters. Every entry adds 4 - amount of same neighbors"""
    perimeter = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for coordinate in coordinates:
        contribution = 4
        for dx, dy in directions:
            neighbor = Coordinate(coordinate.x + dx, coordinate.y + dy)
            if neighbor in coordinates:
                contribution -= 1
        perimeter += contribution
    print("Found perimeter", perimeter)
    return perimeter


def group(grid):
    # Find areas
    flower_dict = {}
    for flower in find_flowers(grid):
        flower_dict[flower] = [count_flowers(grid, flower)]
        coordinates = find_coordinates(grid, flower)
        flower_dict[flower].append(find_perimeter(coordinates))

    print(flower_dict)
    perimeter = 0
    for value in flower_dict.values():
        contribution = 1
        for val in value:
            contribution *= val
        perimeter += contribution
    return perimeter


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    assert group(grid) == 140
    grid = process_file("dummydata2.txt")
    assert group(grid) == 772

    rocks = process_file("data.txt")
    print("Part 1:", group(grid))
    print("Part 2:", group(grid))
