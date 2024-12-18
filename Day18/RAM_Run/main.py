import heapq
from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def fill_grid(filename, grid_size, falling_bytes):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        falling_memory = [list(map(int, line.strip().split(","))) for line in file]
        grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
        for idx in range(falling_bytes):
            grid[falling_memory[idx][1]][falling_memory[idx][0]] = "#"
        return grid


def print_grid(grid):
    for row in grid:
        print(" ".join(row))


def find_shortest_path(grid, grid_size):
    coordinates_with_dots = [
        Coordinate(x=col, y=row)
        for row in range(grid_size)
        for col in range(grid_size)
        if grid[row][col] == "."
    ]
    path_cost = {}
    for row in range(grid_size):
        for col in range(grid_size):
            if grid[row][col] == ".":
                coord = Coordinate(x=col, y=row)
                coordinates_with_dots.append(coord)
                # Initialize each path with infinite cost, except for the start point
                path_cost[coord] = 0 if coord == Coordinate(0, 0) else float("inf")

    path = Coordinate(x=0, y=0)

    path_queue = []
    heapq.heappush(path_queue, (path_cost[path], path))
    while path_queue:
        entry = heapq.heappop(path_queue)[1]
        for dx, dy in directions:
            neighbor = Coordinate(entry.x + dx, entry.y + dy)
            if neighbor not in coordinates_with_dots:
                continue

            new_cost = path_cost[entry] + 1
            if path_cost[neighbor] <= new_cost:
                continue

            path_cost[neighbor] = new_cost
            heapq.heappush(path_queue, (new_cost, neighbor))

    return path_cost[Coordinate(grid_size - 1, grid_size - 1)]


def find_blocking_byte(filename, grid_size):
    with open(filename, "r") as file:
        lines = file.readlines()
        length = len(lines)

    def find_idx_step(idx, step_size):
        """Helper function to find the index using a step size."""
        inf_found = False
        while not inf_found:
            grid = fill_grid(filename, grid_size, idx)
            if find_shortest_path(grid, grid_size) == float("inf"):
                inf_found = True
            else:
                idx += step_size
        idx -= step_size  # We know its in between this idx and idx + step_size
        return idx

    idx = length // 5
    # First block search with length // 5 step size, then 5**2. Then Make more fine-grained for larger data-sets
    idx = find_idx_step(idx, length // 5)
    idx = find_idx_step(idx, length // 5**2)
    if length >= 500:
        idx = find_idx_step(idx, length // 5**3)
        if length >= 2500:
            idx = find_idx_step(idx, length // 5**4)

    idx = find_idx_step(idx, 1)
    return lines[idx].strip()


# Main execution
if __name__ == "__main__":
    grid = fill_grid("dummydata.txt", 7, 12)
    assert find_shortest_path(grid, 7) == 22
    assert find_blocking_byte("dummydata.txt", 7) == "6,1"

    grid = fill_grid("data.txt", 71, 1024)
    print("Part 1", find_shortest_path(grid, 71))
    print("Part 2", find_blocking_byte("data.txt", 71))
