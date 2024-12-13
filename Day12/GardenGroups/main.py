import queue
import random
from collections import namedtuple
from functools import reduce
from itertools import count

Coordinate = namedtuple("Coordinate", ["x", "y"])
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


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


def find_groups(coordinates):
    q = queue.Queue()
    visited = []
    groups = []
    while len(visited) < len(coordinates):
        group = []
        remaining_coordinates = [coord for coord in coordinates if coord not in visited]
        rand_val = random.choice(remaining_coordinates)
        q.put(rand_val)

        while q.qsize() > 0:
            entry = q.get()
            if entry in visited:
                continue

            visited.append(entry)
            group.append(entry)
            for dx, dy in directions:
                neighbor = Coordinate(entry.x + dx, entry.y + dy)
                if neighbor in coordinates and neighbor not in visited:
                    # print("Adding neighbor", neighbor)
                    q.put(neighbor)

        groups.append(group)

    return groups


def find_perimeter(coordinates: Coordinate):
    """Find perimeters. Every entry adds 4 - amount of same neighbors"""
    perimeter = 0
    for coordinate in coordinates:
        contribution = 4
        for dx, dy in directions:
            neighbor = Coordinate(coordinate.x + dx, coordinate.y + dy)
            if neighbor in coordinates:
                contribution -= 1
        perimeter += contribution
    return perimeter


def group(grid):
    # Find areas
    flower_dict = {}
    for flower in sorted(find_flowers(grid)):
        coordinates = find_coordinates(grid, flower)
        groups = find_groups(coordinates)
        if len(groups) > 1:
            for idx, group in enumerate(groups):
                flower_dict[flower + str(idx)] = [len(group)]
                flower_dict[flower + str(idx)].append(find_perimeter(group))
        else:
            flower_dict[flower] = [count_flowers(grid, flower)]
            flower_dict[flower].append(find_perimeter(coordinates))

    return sum(reduce(lambda x, y: x * y, group, 1) for group in flower_dict.values())


def dfs(x, y, flower_type):
    """Perform DFS to mark all connected cells of the same flower type."""
    stack = [(x, y)]
    region_cells = []
    visited[x][y] = True
    while stack:
        cx, cy = stack.pop()
        region_cells.append((cx, cy))
        # Check the 4 neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = cx + dx, cy + dy
            if (
                in_bounds(nx, ny)
                and not visited[nx][ny]
                and grid[nx][ny] == flower_type
            ):
                visited[nx][ny] = True
                stack.append((nx, ny))
    return region_cells


def count_border_sides(region_cells):
    """Count the sides on the border of a region."""
    sides = 0
    for x, y in region_cells:
        # Check 4 directions for boundaries
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if not in_bounds(nx, ny) or grid[nx][ny] != grid[x][y]:
                sides += 1
    return sides


total_sides = 0


def bulk(grid):
    # Find areas
    flower_dict = {}
    for flower in sorted(find_flowers(grid)):
        coordinates = find_coordinates(grid, flower)
        groups = find_groups(coordinates)
        if len(groups) > 1:
            for idx, group in enumerate(groups):
                flower_dict[flower + str(idx)] = [len(group)]
                flower_dict[flower + str(idx)].append(find_perimeter(group))
        else:
            flower_dict[flower] = [count_flowers(grid, flower)]
            flower_dict[flower].append(find_perimeter(coordinates))

    return sum(reduce(lambda x, y: x * y, group, 1) for group in flower_dict.values())


# Main execution
if __name__ == "__main__":
    grid = process_file("dummydata.txt")
    grid2 = process_file("dummydata2.txt")
    assert group(grid) == 140
    assert group(grid2) == 1930
    assert group(grid) == 140

    grid = process_file("data.txt")
    print("Part 1:", group(grid))
    # print("Part 2:", group(grid))