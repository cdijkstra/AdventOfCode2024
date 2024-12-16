import copy
import heapq
import queue
from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])
Path = namedtuple("Path", ["Coordinate", "Cost", "Direction"])
direction_map = {
    "N": (0, -1),  # North: move up
    "E": (1, 0),  # East: move right
    "S": (0, 1),  # South: move down
    "W": (-1, 0),  # West: move left
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
    if current_direction == None:
        print([[key, value] for key, value in direction_map.items()])
        return [[key, value] for key, value in direction_map.items()]

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
    if dir1 == None:
        print(dir2)
        return dir2 != "E"  # Implcit assumption we are facing east
    return dir1 != dir2


def manhattan_distance_factor(coord, goal):
    return 350 * (abs(coord.x - goal.x) + abs(coord.y - goal.y))


def traverse(grid):
    start_coor = find_coordinates(grid, "S")[0]
    end_coor = find_coordinates(grid, "E")[0]

    path = Path(Coordinate=start_coor, Cost=0, Direction=None)
    path_queue = []
    heapq.heappush(path_queue, (0, path))
    while path_queue:
        entry = heapq.heappop(path_queue)[1]
        if entry.Coordinate == end_coor:
            print("found", entry.Cost)
            return entry.Cost
        directions = get_valid_directions(entry.Direction)
        for dir, (dx, dy) in directions:
            neighbor = Coordinate(entry.Coordinate.x + dx, entry.Coordinate.y + dy)
            if (
                0 <= neighbor.x < len(grid)
                and 0 <= neighbor.y < len(grid[0])
                and grid[neighbor.x][neighbor.y] != "#"
            ):
                cost_increase = 1001 if direction_changed(entry.Direction, dir) else 1
                new_cost = entry.Cost + cost_increase
                path = Path(neighbor, new_cost, dir)
                heapq.heappush(
                    path_queue,
                    (new_cost + manhattan_distance_factor(neighbor, end_coor), path),
                    # Add a Manhattan factor so entries closer to end are more likely
                )


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    print(grid)
    assert traverse(grid) == 7036

    grid = process_file("dummydata2.txt")
    assert traverse(grid) == 11048

    grid = process_file("data.txt")
    print("Part 1", traverse(grid))
