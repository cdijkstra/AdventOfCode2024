import queue
from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])
Explorer = namedtuple("Explorer", ["coordinate", "cheated"])
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def process_file(filename):
    with open(filename, "r") as file:
        return file.read().splitlines()


def find_coordinates(grid, character):
    """Find all coordinates of a specific value in the 2D array."""
    return [
        Coordinate(x=row_idx, y=col_idx)
        for row_idx, row in enumerate(grid)
        for col_idx, value in enumerate(row)
        if value == character
    ]


def find_path_lengths():
    start_coords = find_coordinates(grid, "S")[0]
    end_coords = find_coordinates(grid, "E")[0]
    path = find_coordinates(grid, ".") + [start_coords, end_coords]
    # Traverse through maze normally, so we know the distance to the end from all points
    path_lengths_from_start = {}
    path_lengths_to_end = {}
    path_length = 0
    visited = []

    q = queue.Queue()

    q.put(start_coords)
    while q:
        coord = q.get()
        path_lengths_from_start[coord] = path_length

        visited.append(coord)
        path_length += 1
        if coord == end_coords:
            break

        for dx, dy in directions:
            new_coord = Coordinate(coord.x + dx, coord.y + dy)
            if new_coord in visited or new_coord not in path:
                continue
            q.put(new_coord)

    # Fill path_lengths_from_end dictionary with same keys as path_lengths_to_end and values
    # path_lengths_to_end[start_coord] - path_lengths_from_end[coord]
    for coord in path_lengths_from_start:
        path_lengths_to_end[coord] = (
            path_lengths_from_start[end_coords] - path_lengths_from_start[coord]
        )
    return path_lengths_from_start, path_lengths_to_end


def manhattan_distance(first_coord: Coordinate, second_coord: Coordinate):
    return abs(second_coord.x - first_coord.x) + abs(second_coord.y - first_coord.y)


def find_cheat_path_length(allowed_cheats=2, min_time_save=1):
    start_coords = find_coordinates(grid, "S")[0]
    end_coords = find_coordinates(grid, "E")[0]
    path = find_coordinates(grid, ".") + [start_coords, end_coords]

    path_lengths_from_start, path_lengths_to_end = find_path_lengths()
    times_saved = []
    normal_time = path_lengths_from_start[end_coords]

    for candidate in path:
        # Find all coordinates '.' that are located witin allowed_cheats distance from candidate
        end_tunnel = [
            coord
            for coord in path
            if manhattan_distance(candidate, coord) <= allowed_cheats
        ]
        for coord in end_tunnel:
            tunnel_distance = manhattan_distance(candidate, coord)
            total_time = (
                path_lengths_from_start[candidate]
                + tunnel_distance
                + path_lengths_to_end[coord]
            )
            if total_time <= normal_time - min_time_save:
                times_saved.append(normal_time - total_time)

    return len(times_saved)


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    assert find_cheat_path_length() == 44
    assert find_cheat_path_length(20, 50) == 285
    grid = process_file("data.txt")
    print("Part 1", find_cheat_path_length(2, 100))
    print("Part 2", find_cheat_path_length(20, 100))
