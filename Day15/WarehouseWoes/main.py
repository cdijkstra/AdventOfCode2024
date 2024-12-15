from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        grid, instructions = file.read().split("\n\n")
        grid = [list(line) for line in grid.strip().split("\n")]
        instructions = instructions.replace("\n", "").strip()
        return grid, instructions


def find_coordinates(grid, character):
    return [
        Coordinate(x=row_index, y=col_index)
        for row_index, row in enumerate(grid)
        for col_index, value in enumerate(row)
        if value == character
    ]


def print_grid(grid):
    for row in grid:
        print(" ".join(row))


def traverse(grid, instructions):
    coords = find_coordinates(grid, "@")[0]
    for instruction in instructions:
        if instruction == "<" and grid[coords.x][coords.y - 1] not in ["#"]:
            new_x, new_y = coords.x, coords.y - 1
            if grid[new_x][new_y] == "O":
                subarray = []
                while grid[new_x][new_y] == "O" and grid[new_x][new_y - 1] != "#":
                    subarray.append(Coordinate(x=new_x, y=new_y))
                    new_y -= 1
                    if grid[new_x][new_y] != ".":
                        continue
                    print("Move array to the left", subarray)
                    o_coords = sorted(subarray, key=lambda coord: coord.y)
                    for o_coord in o_coords:
                        (
                            grid[o_coord.x][o_coord.y - 1],
                            grid[o_coord.x][o_coord.y],
                        ) = (grid[o_coord.x][o_coord.y], ".")
                    # Swap coordinates '.' and '@' in array at Coordinate(x=coords.x, y=coords.y - 1) and Coordinate(x=coords.x, y=coords.y)
                    grid[coords.x][coords.y], grid[coords.x][coords.y - 1] = (
                        grid[coords.x][coords.y - 1],
                        grid[coords.x][coords.y],
                    )
                    coords = Coordinate(x=coords.x, y=coords.y - 1)
                    break
            else:
                grid[coords.x][coords.y], grid[new_x][new_y] = (
                    grid[new_x][new_y],
                    grid[coords.x][coords.y],
                )
                coords = Coordinate(x=new_x, y=new_y)
        elif instruction == ">" and grid[coords.x][coords.y + 1] not in ["#"]:
            new_x = coords.x
            new_y = coords.y + 1
            if grid[new_x][new_y] == "O":
                subarray = []
                while grid[new_x][new_y] == "O" and grid[new_x][new_y + 1] != "#":
                    subarray.append(Coordinate(x=new_x, y=new_y))
                    new_y += 1
                    if grid[new_x][new_y] != ".":
                        continue
                    print("Move array to the right", subarray)
                    o_coords = sorted(subarray, key=lambda coord: coord.y, reverse=True)
                    print(o_coords)
                    for o_coord in o_coords:
                        (
                            grid[o_coord.x][o_coord.y + 1],
                            grid[o_coord.x][o_coord.y],
                        ) = (grid[o_coord.x][o_coord.y], ".")

                    # Swap coordinates '.' and '@' in array at Coordinate(x=coords.x, y=coords.y - 1) and Coordinate(x=coords.x, y=coords.y)
                    grid[coords.x][coords.y], grid[coords.x][coords.y + 1] = (
                        grid[coords.x][coords.y + 1],
                        grid[coords.x][coords.y],
                    )
                    coords = Coordinate(x=coords.x, y=coords.y + 1)
                    break
            else:
                grid[coords.x][coords.y], grid[new_x][new_y] = (
                    grid[new_x][new_y],
                    grid[coords.x][coords.y],
                )
                coords = Coordinate(x=new_x, y=new_y)
        elif instruction == "^" and grid[coords.x - 1][coords.y] not in ["#"]:
            new_x = coords.x - 1
            new_y = coords.y
            if grid[new_x][new_y] == "O":
                subarray = []
                while grid[new_x][new_y] == "O" and grid[new_x - 1][new_y] != "#":
                    subarray.append(Coordinate(x=new_x, y=new_y))
                    new_x -= 1
                    if grid[new_x][new_y] != ".":
                        continue
                    print("Move array up", subarray)
                    o_coords = sorted(subarray, key=lambda coord: coord.x)
                    for o_coord in o_coords:
                        (
                            grid[o_coord.x - 1][o_coord.y],
                            grid[o_coord.x][o_coord.y],
                        ) = (grid[o_coord.x][o_coord.y], ".")
                    # Swap coordinates '.' and '@' in array at Coordinate(x=coords.x, y=coords.y - 1) and Coordinate(x=coords.x, y=coords.y)
                    grid[coords.x][coords.y], grid[coords.x - 1][coords.y] = (
                        grid[coords.x - 1][coords.y],
                        grid[coords.x][coords.y],
                    )
                    coords = Coordinate(x=coords.x - 1, y=coords.y)
                    break
            else:
                grid[coords.x][coords.y], grid[new_x][new_y] = (
                    grid[new_x][new_y],
                    grid[coords.x][coords.y],
                )
                coords = Coordinate(x=new_x, y=new_y)
        elif instruction == "v" and grid[coords.x + 1][coords.y] not in ["#"]:
            print("performing down from", coords)
            new_x = coords.x + 1
            new_y = coords.y
            if grid[new_x][new_y] == "O":
                subarray = []
                while grid[new_x][new_y] == "O" and grid[new_x + 1][new_y] != "#":
                    subarray.append(Coordinate(x=new_x, y=new_y))
                    new_x += 1
                    if grid[new_x][new_y] != ".":
                        continue
                    print("Move array down", subarray)
                    o_coords = sorted(subarray, key=lambda coord: coord.x, reverse=True)
                    for o_coord in o_coords:
                        (
                            grid[o_coord.x + 1][o_coord.y],
                            grid[o_coord.x][o_coord.y],
                        ) = (grid[o_coord.x][o_coord.y], ".")
                    # Swap coordinates '.' and '@' in array at Coordinate(x=coords.x, y=coords.y - 1) and Coordinate(x=coords.x, y=coords.y)
                    grid[coords.x][coords.y], grid[coords.x + 1][coords.y] = (
                        grid[coords.x + 1][coords.y],
                        grid[coords.x][coords.y],
                    )
                    coords = Coordinate(x=coords.x + 1, y=coords.y)
                    break
            else:
                grid[coords.x][coords.y], grid[new_x][new_y] = (
                    grid[new_x][new_y],
                    grid[coords.x][coords.y],
                )
                coords = Coordinate(x=new_x, y=new_y)

    sum = 0
    for coords in find_coordinates(grid, "O"):
        sum += 100 * coords.x + coords.y
    return sum


# Main execution
if __name__ == "__main__":
    grid, instructions = process_file("dummydata.txt")
    assert traverse(grid, instructions) == 2028

    grid, instructions = process_file("dummydata2.txt")
    assert traverse(grid, instructions) == 10092

    grid, instructions = process_file("data.txt")
    print("Part 1", traverse(grid, instructions))
