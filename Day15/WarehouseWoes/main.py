from collections import namedtuple

Coordinate = namedtuple("Coordinate", ["x", "y"])


def process_file(filename, translate=False):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        grid, instructions = file.read().split("\n\n")
        if translate:
            trans_table = str.maketrans({"#": "##", "O": "[]", ".": "..", "@": "@."})
            grid = grid.translate(trans_table)
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
            if grid[new_x][new_y] in ["O", "[", "]"]:
                subarray = []
                while (
                    grid[new_x][new_y] in ["O", "[", "]"]
                    and grid[new_x][new_y - 1] != "#"
                ):
                    subarray.append(Coordinate(x=new_x, y=new_y))
                    new_y -= 1
                    if grid[new_x][new_y] != ".":
                        continue
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
            if grid[new_x][new_y] in ["O", "[", "]"]:
                subarray = []
                while (
                    grid[new_x][new_y] in ["O", "[", "]"]
                    and grid[new_x][new_y + 1] != "#"
                ):
                    subarray.append(Coordinate(x=new_x, y=new_y))
                    new_y += 1
                    if grid[new_x][new_y] != ".":
                        continue
                    o_coords = sorted(subarray, key=lambda coord: coord.y, reverse=True)
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
            subarray = []
            coordinates_to_consider = [Coordinate(x=coords.x - 1, y=coords.y)]
            move_allowed = True
            while coordinates_to_consider:
                new_coordinates_to_consider = []
                if any(
                    grid[coord.x][coord.y] == "#" for coord in coordinates_to_consider
                ):
                    coordinates_to_consider = []
                    move_allowed = False
                else:
                    for coord in coordinates_to_consider:
                        if grid[coord.x][coord.y] == "O":
                            subarray.append(coord)
                            new_coordinates_to_consider.append(
                                Coordinate(x=coord.x - 1, y=coord.y)
                            )
                        elif grid[coord.x][coord.y] == "[":
                            subarray.append(coord)
                            subarray.append(Coordinate(x=coord.x, y=coord.y + 1))
                            new_coordinates_to_consider.extend(
                                [
                                    Coordinate(x=coord.x - 1, y=coord.y),
                                    Coordinate(x=coord.x - 1, y=coord.y + 1),
                                ]
                            )
                        elif grid[coord.x][coord.y] == "]":
                            subarray.append(coord)
                            subarray.append(Coordinate(x=coord.x, y=coord.y - 1))
                            new_coordinates_to_consider.extend(
                                [
                                    Coordinate(x=coord.x - 1, y=coord.y),
                                    Coordinate(x=coord.x - 1, y=coord.y - 1),
                                ]
                            )
                    coordinates_to_consider = list(set(new_coordinates_to_consider))
            if not move_allowed:
                continue

            subarray = list(set(subarray))
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

        elif instruction == "v" and grid[coords.x + 1][coords.y] not in ["#"]:
            subarray = []
            coordinates_to_consider = [Coordinate(x=coords.x + 1, y=coords.y)]
            move_allowed = True
            while coordinates_to_consider:
                new_coordinates_to_consider = []
                if any(
                    grid[coord.x][coord.y] == "#" for coord in coordinates_to_consider
                ):
                    coordinates_to_consider = []
                    move_allowed = False
                else:
                    for coord in coordinates_to_consider:
                        if grid[coord.x][coord.y] == "O":
                            subarray.append(coord)
                            new_coordinates_to_consider.append(
                                Coordinate(x=coord.x + 1, y=coord.y)
                            )
                        elif grid[coord.x][coord.y] == "[":
                            subarray.append(coord)
                            subarray.append(Coordinate(x=coord.x, y=coord.y + 1))
                            new_coordinates_to_consider.extend(
                                [
                                    Coordinate(x=coord.x + 1, y=coord.y),
                                    Coordinate(x=coord.x + 1, y=coord.y + 1),
                                ]
                            )
                        elif grid[coord.x][coord.y] == "]":
                            subarray.append(coord)
                            subarray.append(Coordinate(x=coord.x, y=coord.y - 1))
                            new_coordinates_to_consider.extend(
                                [
                                    Coordinate(x=coord.x + 1, y=coord.y),
                                    Coordinate(x=coord.x + 1, y=coord.y - 1),
                                ]
                            )
                    coordinates_to_consider = list(set(new_coordinates_to_consider))

            if not move_allowed:
                continue

            subarray = list(set(subarray))
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

    sum = 0
    for coords in find_coordinates(grid, "O"):
        sum += 100 * coords.x + coords.y
    for coords in find_coordinates(grid, "["):
        sum += 100 * coords.x + coords.y
    return sum


# Main execution
if __name__ == "__main__":
    grid, instructions = process_file("dummydata.txt")
    assert traverse(grid, instructions) == 2028
    grid, instructions = process_file("dummydata2.txt")
    assert traverse(grid, instructions) == 10092
    grid, instructions = process_file("dummydata3.txt", translate=True)
    assert traverse(grid, instructions) == 618
    grid, instructions = process_file("dummydata3.txt", translate=True)
    assert traverse(grid, instructions) == 618
    grid, instructions = process_file("dummydata2.txt", translate=True)
    assert traverse(grid, instructions) == 9021

    grid, instructions = process_file("data.txt")
    print("Part 1", traverse(grid, instructions))
    grid, instructions = process_file("data.txt", translate=True)
    print("Part 2", traverse(grid, instructions))
