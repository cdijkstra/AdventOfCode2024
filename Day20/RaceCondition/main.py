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
        # Compute the value based on the provided formula
        path_lengths_to_end[coord] = (
            path_lengths_from_start[end_coords] - path_lengths_from_start[coord]
        )
    return path_lengths_from_start, path_lengths_to_end


def find_cheat_path_length(allowed_cheats=2, min_time_save=0):
    start_coords = find_coordinates(grid, "S")[0]
    end_coords = find_coordinates(grid, "E")[0]
    path = find_coordinates(grid, ".") + [start_coords, end_coords]
    walls = find_coordinates(grid, "#")

    path_lengths_from_start, path_lengths_to_end = find_path_lengths()
    lengths = []
    times_saved = []
    normal_length = path_lengths_from_start[end_coords]
    start_end_tunnels = []

    for candidate in path:
        q = queue.Queue()
        tunnel = []
        q.put((candidate, candidate, tunnel))
        while q.qsize() > 0:
            start, candidate, tunnel = q.get()
            for dx, dy in directions:
                neighbor = Coordinate(candidate.x + dx, candidate.y + dy)
                if (
                    neighbor in walls
                    and neighbor not in tunnel
                    and len(tunnel) < allowed_cheats - 1
                ):
                    q.put((start, neighbor, tunnel + [neighbor]))
                elif (
                    neighbor in path
                    and (start, neighbor) not in start_end_tunnels
                    and start != neighbor
                    and 0 < len(tunnel) < allowed_cheats
                ):
                    # print("dug tunnel from", start, "to", neighbor, "tunnel=", tunnel)
                    start_end_tunnels.append((start, neighbor))
                    length = (
                        path_lengths_from_start[start]
                        + len(tunnel)
                        + 1
                        + path_lengths_to_end[neighbor]
                    )
                    lengths.append(length)
                    time_saved = normal_length - length
                    if time_saved > 0:
                        times_saved.append(time_saved)

    print("Time saved", sorted(times_saved))
    return sum(1 for s in times_saved if s >= min_time_save)


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    assert find_cheat_path_length() == 44
    # assert find_cheat_path_length(20, 50) == 44
    grid = process_file("data.txt")
    print("Part 1", find_cheat_path_length(2, 100))
    print("Part 12", find_cheat_path_length(20, 100))
