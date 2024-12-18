import heapq
from collections import namedtuple
from enum import unique

Coordinate = namedtuple("Coordinate", ["x", "y"])
Path = namedtuple("Path", ["Coordinate", "Cost", "Direction"])
Path_History = namedtuple("Path", ["Coordinate", "Cost", "Direction", "Visited"])
direction_map = {
    "N": (-1, 0),  # North: move up
    "E": (0, 1),  # East: move right
    "S": (1, 0),  # South: move down
    "W": (0, -1),  # West: move left
}

turns = {
    "N": ["E", "W"],
    "E": ["N", "S"],
    "S": ["W", "E"],
    "W": ["S", "N"],
}


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return file.read().splitlines()


def find_coordinates(grid, character):
    return [
        Coordinate(x=row_index, y=col_index)
        for row_index, row in enumerate(grid)
        for col_index, value in enumerate(row)
        if value == character
    ]


def traverse(grid, manhatton_factor=0):
    start_coor = find_coordinates(grid, "S")[0]
    end_coor = find_coordinates(grid, "E")[0]
    coordinates_with_dots = [
        Coordinate(x=row_idx, y=col_idx)
        for row_idx, row in enumerate(grid)
        for col_idx, value in enumerate(row)
        if value in [".", "S", "E"]
    ]
    path_cost = {
        (coord, direction): float("inf")
        for coord in coordinates_with_dots
        for direction in direction_map.keys()
    }
    path_cost[(start_coor, "E")] = 0
    path = Path(Coordinate=start_coor, Cost=0, Direction="E")
    path_queue = []

    # Use a priority queue with Cost and Manhttan factor as key
    heapq.heappush(path_queue, (0, path))
    while path_queue:
        entry = heapq.heappop(path_queue)[1]
        if entry.Coordinate == end_coor:
            return entry.Cost

        # Add turns
        for new_direction in turns[entry.Direction]:
            new_cost = entry.Cost + 1000  # Add 1000 for turning
            if new_cost > path_cost[(entry.Coordinate, new_direction)]:
                continue

            path_cost[(entry.Coordinate, new_direction)] = new_cost
            path = Path(entry.Coordinate, new_cost, new_direction)
            heapq.heappush(path_queue, (new_cost, path))

        (dx, dy) = direction_map[entry.Direction]
        neighbor = Coordinate(entry.Coordinate.x + dx, entry.Coordinate.y + dy)
        new_cost = entry.Cost + 1  # Add 1 for moving
        if (
            neighbor not in coordinates_with_dots
            or new_cost > path_cost[(neighbor, entry.Direction)]
        ):
            continue

        path = Path(neighbor, new_cost, entry.Direction)
        heapq.heappush(path_queue, (new_cost, path))


def traverse_with_history(grid):
    start_coor = find_coordinates(grid, "S")[0]
    end_coor = find_coordinates(grid, "E")[0]
    coordinates_with_dots = [
        Coordinate(x=row_idx, y=col_idx)
        for row_idx, row in enumerate(grid)
        for col_idx, value in enumerate(row)
        if value in [".", "S", "E"]
    ]
    path_cost = {
        (coord, direction): float("inf")
        for coord in coordinates_with_dots
        for direction in direction_map.keys()
    }
    path_cost[(start_coor, "E")] = 0

    path_queue = []
    path = Path_History(
        Coordinate=start_coor, Cost=0, Direction="E", Visited=[start_coor]
    )
    total_route = []
    finish_reached = False

    heapq.heappush(path_queue, (0, path))
    while path_queue:
        entry = heapq.heappop(path_queue)[1]
        if entry.Coordinate == end_coor:
            if entry.Cost <= path_cost[end_coor]:
                finish_reached = True
                path_cost[end_coor] = entry.Cost
                total_route.extend(entry.Visited)
        elif finish_reached and entry.Cost > path_cost[end_coor]:
            route = list(set(tuple(c) for c in total_route))
            return len(route)

        # Add turns
        for new_direction in turns[entry.Direction]:
            new_cost = entry.Cost + 1000  # Add 1000 for turning
            if new_cost > path_cost[(entry.Coordinate, new_direction)]:
                continue

            new_visited = entry.Visited.copy()
            path_cost[(entry.Coordinate, new_direction)] = new_cost
            path = Path_History(entry.Coordinate, new_cost, new_direction, new_visited)
            heapq.heappush(path_queue, (new_cost, path))

        (dx, dy) = direction_map[entry.Direction]
        neighbor = Coordinate(entry.Coordinate.x + dx, entry.Coordinate.y + dy)
        new_cost = entry.Cost + 1  # Add 1 for moving
        if (
            neighbor not in coordinates_with_dots
            or new_cost > path_cost[(neighbor, entry.Direction)]
        ):
            continue

        path_cost[neighbor] = new_cost
        new_visited = entry.Visited + [neighbor]
        path = Path_History(neighbor, new_cost, entry.Direction, new_visited)
        heapq.heappush(path_queue, (new_cost, path))


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    assert traverse(grid) == 7036
    assert traverse_with_history(grid) == 45

    grid = process_file("dummydata2.txt")
    assert traverse(grid) == 11048
    assert traverse_with_history(grid) == 64

    grid = process_file("data.txt")
    print("Part 1", traverse(grid))
    print("Part 2", traverse_with_history(grid))  # 429 is too low
