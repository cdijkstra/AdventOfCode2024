import re
from collections import namedtuple
from copy import deepcopy


# Coordinate = namedtuple("Coordinate", ["x", "y"])
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"Coordinate(x={self.x}, y={self.y})"


Explorer = namedtuple("Explorer", ["coordinate", "cheated"])
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return file.read().splitlines()


numpad_positions = {
    "7": Coordinate(x=0, y=0),
    "8": Coordinate(x=0, y=1),
    "9": Coordinate(x=0, y=2),
    "4": Coordinate(x=1, y=0),
    "5": Coordinate(x=1, y=1),
    "6": Coordinate(x=1, y=2),
    "1": Coordinate(x=2, y=0),
    "2": Coordinate(x=2, y=1),
    "3": Coordinate(x=2, y=2),
    "0": Coordinate(x=3, y=1),
    "A": Coordinate(x=3, y=2),
}

directional_positions = {
    "^": Coordinate(x=0, y=1),
    "A": Coordinate(x=0, y=2),
    "<": Coordinate(x=1, y=0),
    "v": Coordinate(x=1, y=1),
    ">": Coordinate(x=1, y=2),
}


def get_all_routes(sequence):
    instructions = generate_routes(sequence, deepcopy(numpad_positions["A"]))
    return instructions


def generate_routes(sequence, position, instructions=[""]):
    if not sequence:
        # Base case: If no more characters in the sequence, add the current instruction to the list
        return instructions

    next_position = numpad_positions[sequence[0]]

    current_position = deepcopy(position)
    print("1 current pos", current_position, next_position)
    new_instructions = []
    # Option 1: Move x first, then y
    x_first = ""
    if not (current_position.y == 0 and next_position.x == 3):
        while current_position.x != next_position.x:
            if next_position.x < current_position.x:
                x_first += "^"
                current_position.x -= 1
            else:
                x_first += "v"
                current_position.x += 1
        while current_position.y != next_position.y:
            if next_position.y > current_position.y:
                x_first += ">"
                current_position.y += 1
            else:
                x_first += "<"
                current_position.y -= 1
        x_first += "A"
        print("x_first", x_first)
        if not instructions or instructions == [""]:
            new_instructions.append(x_first)
        else:
            for instruction in instructions:
                new_instructions.append(instruction + x_first)

    # Save the position before modifying for option 2 (y-first)
    current_position = deepcopy(position)
    print("2 current pos", current_position, next_position)

    # Option 2: Move y first, then x
    y_first = ""
    if not (current_position.x == 3 and next_position.y == 0):
        while current_position.y != next_position.y:
            if next_position.y > current_position.y:
                y_first += ">"
                current_position.y += 1
            else:
                y_first += "<"
                current_position.y -= 1
        while current_position.x != next_position.x:
            if next_position.x < current_position.x:
                y_first += "^"
                current_position.x -= 1
            else:
                y_first += "v"
                current_position.x += 1
        y_first += "A"
        print("y_first", y_first)
        if not instructions or instructions == [""]:
            new_instructions.append(y_first)
        else:
            for instruction in instructions:
                new_instructions.append(instruction + y_first)

    instructions = new_instructions
    print("Current instructions", instructions)
    # Recurse with both options (x-first and y-first) and the remaining sequence
    return generate_routes(
        sequence[1:],
        deepcopy(next_position),
        instructions,
    )


def calculate_length(sequences, num_robots):
    instructions = []
    # Numpad instructions
    for sequence in sequences:
        routes = get_all_routes(sequence)
        for extra_robots in range(num_robots):
            for i, instruction in enumerate(routes):
                # Directional instructions
                new_instruction = ""
                position = deepcopy(directional_positions["A"])
                for char in instruction:
                    next_position = directional_positions[char]
                    while position.x != next_position.x:
                        if next_position.x > position.x:
                            new_instruction += "v"
                            position.x += 1
                        else:
                            new_instruction += "^"
                            position.x -= 1
                    while position.y != next_position.y:
                        if next_position.y > position.y:
                            new_instruction += ">"
                            position.y += 1
                        else:
                            new_instruction += "<"
                            position.y -= 1
                    new_instruction += "A"
                routes[i] = new_instruction
        instructions.append(routes)
        # Replace entry by new_instruction in array

    print("Instructions = ", instructions)
    total_complexity = 0
    for sequence, instruction in zip(sequences, instructions):
        sequence_len = int(re.search(r"\d+", sequence).group())
        path_len = len(min(instruction, key=len))
        print(sequence_len, path_len)
        total_complexity += sequence_len * path_len
    return total_complexity


# Main execution
if __name__ == "__main__":
    sequences = process_file("dummydata.txt")
    assert calculate_length(sequences, num_robots=2) == 126384
    sequences = process_file("data.txt")
    print("Part 1:", calculate_length(sequences, num_robots=2))
