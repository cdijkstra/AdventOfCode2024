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
        # Compute the value based on the provided formula
        path_lengths_to_end[coord] = (
            path_lengths_from_start[end_coords] - path_lengths_from_start[coord]
        )
    return path_lengths_from_start, path_lengths_to_end


def find_cheat_path_length(allowed_cheats=2, min_time_save=0):
    path_lengths_from_start, path_lengths_to_end = find_path_lengths()
    lengths = []
    times_saved = []
    normal_length = path_lengths_from_start[find_coordinates(grid, "E")[0]]
    print(normal_length)

    for candidate in path:
        for dx, dy in directions:
            neighbor = Coordinate(candidate.x + dx, candidate.y + dy)
            if grid[neighbor.x][neighbor.y] != "#":
                continue

            skip_one_wall = Coordinate(candidate.x + 2 * dx, candidate.y + 2 * dy)
            skip_two_walls = Coordinate(candidate.x + 3 * dx, candidate.y + 3 * dy)
            if skip_one_wall in path:
                length = (
                    path_lengths_from_start[candidate]
                    + path_lengths_to_end[skip_one_wall]
                    + 2
                )
                lengths.append(length)
                time_saved = normal_length - length
                if time_saved > 0:
                    times_saved.append(time_saved)
            elif skip_two_walls in path and grid[neighbor.x][neighbor.y] == "#":
                length = (
                    path_lengths_from_start[candidate]
                    + path_lengths_to_end[skip_two_walls]
                    + 3
                )
                lengths.append(length)
                time_saved = normal_length - length
                if time_saved > 0:
                    times_saved.append(time_saved)

    return sum(1 for s in times_saved if s >= min_time_save)


def find_cheat_path_length2(allowed_cheats=2, min_time_save=0):
    path_lengths_from_start, path_lengths_to_end = find_path_lengths()
    lengths = []
    times_saved = []
    normal_length = path_lengths_from_start[find_coordinates(grid, "E")[0]]
    print(normal_length)

    for candidate in path:
        for dx, dy in directions:
            neighbor = Coordinate(candidate.x + dx, candidate.y + dy)
            if grid[neighbor.x][neighbor.y] != "#":
                continue

            for skip_wall_number in range(1, allowed_cheats + 1):
                tunnel = []
                coord_after_cheat = Coordinate(
                    candidate.x + (skip_wall_number) * dx,
                    candidate.y + (skip_wall_number) * dy,
                )

                print("Before", candidate, "After", coord_after_cheat)
                for t in range(1, skip_wall_number + 1):
                    print(t)
                    new_x = candidate.x + (1 + t) * dx
                    new_y = candidate.y + (1 + t) * dy
                    if 0 <= new_x < len(grid) and 0 <= new_y < len(grid[0]):
                        tunnel.append(grid[new_x][new_y])

                print(
                    coord_after_cheat,
                    tunnel,
                    all(entry == "#" for entry in tunnel),
                    coord_after_cheat in path,
                )
                if not len(tunnel) == skip_wall_number:
                    continue

                if all(entry == "#" for entry in tunnel) and coord_after_cheat in path:
                    length = (
                        path_lengths_from_start[candidate]
                        + path_lengths_to_end[coord_after_cheat]
                        + len(tunnel)
                    )
                    lengths.append(length)
                    time_saved = normal_length - length
                    print("hello")
                    if time_saved > 0:
                        times_saved.append(time_saved)

    print("Time saved", times_saved)
    return sum(1 for s in times_saved if s >= min_time_save)


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    start_coords = find_coordinates(grid, "S")[0]
    end_coords = find_coordinates(grid, "E")[0]
    path = find_coordinates(grid, ".") + [start_coords, end_coords]

    assert find_cheat_path_length2() == 44
    grid = process_file("data.txt")
    start_coords = find_coordinates(grid, "S")[0]
    end_coords = find_coordinates(grid, "E")[0]
    path = find_coordinates(grid, ".") + [start_coords, end_coords]
    print("Part 1", find_cheat_path_length(100))
    # print("Part 12", find_cheat_path_length(100))
