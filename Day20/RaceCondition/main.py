import queue
from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])
Explorer = namedtuple("Explorer", ["coordinate", "cheated"])
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return file.read().splitlines()


def find_coordinates(grid, character):
    """Find all coordinates of a specific value in the 2D array."""
    coordinates = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value == character:
                coordinates.append(Coordinate(x=row_idx, y=col_idx))
    return coordinates


def find_path_lengths():
    path_length = 0
    visited = []

    q = queue.Queue()

    q.put(end_coords)
    while q:
        coord = q.get()
        path_lengths_to_end[coord] = path_length

        visited.append(coord)
        path_length += 1
        if coord == start_coords:
            break

        for dx, dy in directions:
            new_coord = Coordinate(coord.x + dx, coord.y + dy)
            if new_coord in visited or new_coord not in path:
                continue
            q.put(new_coord)

    # Fill path_lengths_from_end dictionary with same keys as path_lengths_to_end and values
    # path_lengths_to_end[start_coord] - path_lengths_from_end[coord]
    for coord in path_lengths_to_end:
        # Compute the value based on the provided formula
        path_lengths_from_start[coord] = (
            path_lengths_to_end[start_coords] - path_lengths_to_end[coord]
        )


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    start_coords = find_coordinates(grid, "S")[0]
    end_coords = find_coordinates(grid, "E")[0]
    path = find_coordinates(grid, ".") + [start_coords, end_coords]

    # Traverse through maze in reverse, so we know the distance to the end from all points
    path_lengths_from_start = {}
    path_lengths_to_end = {}
    find_path_lengths()
    print(path_lengths_from_start)
    print(path_lengths_from_start[Coordinate(1, 1)])
    print(path_lengths_from_start[Coordinate(7, 4)])
    # Now go from start to finish and cut one or two paths
