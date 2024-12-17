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


def get_valid_directions(current_direction):
    # Define the order of directions for left/right turns
    direction_order = ["N", "E", "S", "W"]

    # Get the index of the current direction
    current_index = direction_order.index(current_direction)

    # Calculate new directions
    forward = current_direction
    left = direction_order[(current_index - 1) % 4]  # Turn left
    right = direction_order[(current_index + 1) % 4]  # Turn right

    # Return the directions and their (dx, dy) movements
    return [
        [forward, direction_map[forward]],
        [left, direction_map[left]],
        [right, direction_map[right]],
    ]


def direction_changed(dir1, dir2):
    return dir1 != dir2


def manhattan_distance_factor(coord, goal, manhatton_factor):
    return manhatton_factor * (abs(coord.x - goal.x) + abs(coord.y - goal.y))


def traverse(grid, manhatton_factor=0):
    start_coor = find_coordinates(grid, "S")[0]
    end_coor = find_coordinates(grid, "E")[0]
    path = Path(Coordinate=start_coor, Cost=0, Direction="E")
    path_queue = []

    # Use a priority queue with Cost and Manhttan factor as key
    heapq.heappush(path_queue, (0, path))
    while path_queue:
        entry = heapq.heappop(path_queue)[1]
        if entry.Coordinate == end_coor:
            return entry.Cost

        directions = get_valid_directions(entry.Direction)
        for dir, (dx, dy) in directions:
            neighbor = Coordinate(entry.Coordinate.x + dx, entry.Coordinate.y + dy)
            if (
                0 <= neighbor.x < len(grid)
                and 0 <= neighbor.y < len(grid[0])  # Within bounds
                and grid[neighbor.x][neighbor.y] != "#"  # And can move there
            ):
                cost_increase = 1001 if direction_changed(entry.Direction, dir) else 1
                new_cost = entry.Cost + cost_increase
                path = Path(neighbor, new_cost, dir)
                heapq.heappush(
                    path_queue,
                    (
                        new_cost
                        + manhattan_distance_factor(
                            neighbor, end_coor, manhatton_factor
                        ),
                        path,
                    ),
                    # Add a Manhattan factor so entries closer to end are more likely
                )


def traverse_with_history(grid, manhatton_factor=0, error_fault=0):
    start_coor = find_coordinates(grid, "S")[0]
    end_coor = find_coordinates(grid, "E")[0]
    path = Path_History(
        Coordinate=start_coor, Cost=0, Direction="E", Visited=[start_coor]
    )
    path_queue = []
    min_cost = float("inf")
    total_route = []
    other_exits = 0

    # Use a priority queue with Cost and Manhttan factor as key
    heapq.heappush(path_queue, (0, path))
    while path_queue:
        entry = heapq.heappop(path_queue)[1]
        if entry.Coordinate == end_coor:
            if entry.Cost <= min_cost:
                min_cost = entry.Cost
                total_route.extend(entry.Visited)
                print("Added new entry at", other_exits)
            elif other_exits <= error_fault:
                other_exits += 1
                if (other_exits % 20) == 0:
                    print(other_exits)
            else:
                route = list(set(tuple(c) for c in total_route))
                return len(route)
        directions = get_valid_directions(entry.Direction)
        for dir, (dx, dy) in directions:
            neighbor = Coordinate(entry.Coordinate.x + dx, entry.Coordinate.y + dy)
            if (
                0 <= neighbor.x < len(grid)
                and 0 <= neighbor.y < len(grid[0])  # Within bounds
                and grid[neighbor.x][neighbor.y] != "#"  # And can move there
            ):
                cost_increase = 1001 if direction_changed(entry.Direction, dir) else 1
                new_cost = entry.Cost + cost_increase
                new_visited = entry.Visited.copy()
                new_visited.append(neighbor)
                path = Path_History(neighbor, new_cost, dir, new_visited)
                heapq.heappush(
                    path_queue,
                    (
                        new_cost
                        + manhattan_distance_factor(
                            neighbor, end_coor, manhatton_factor
                        ),
                        path,
                    ),
                    # Add a Manhattan factor so entries closer to end are more likely
                )


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    assert traverse(grid) == 7036
    # assert traverse_with_history(grid, manhatton_factor=0) == 45

    grid = process_file("dummydata2.txt")
    assert traverse(grid) == 11048
    # assert traverse_with_history(grid) == 64

    grid = process_file("data.txt")
    # print("Part 1", traverse(grid, manhatton_factor=300))
    print(
        "Part 2", traverse_with_history(grid, manhatton_factor=300, error_fault=500)
    )  # 429 is too low
