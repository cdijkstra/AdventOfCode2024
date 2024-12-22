import queue
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
    all_instructions = []
    generate_routes(sequence, deepcopy(numpad_positions["A"]), "", all_instructions)
    return all_instructions


def generate_routes(sequence, position, current_instruction, all_instructions):
    if not sequence:
        # Base case: If no more characters in the sequence, add the current instruction to the list
        all_instructions.append(current_instruction)
        return all_instructions

    current_position = deepcopy(position)
    char = sequence[0]
    next_position = numpad_positions[char]

    # Option 1: Move x first, then y
    x_first = []
    while current_position.x != next_position.x:
        if next_position.x < current_position.x:
            x_first.append("^")
            current_position.x -= 1
        else:
            x_first.append("v")
            current_position.x += 1
    while current_position.y != next_position.y:
        if next_position.y > current_position.y:
            x_first.append(">")
            current_position.y += 1
        else:
            x_first.append("<")
            current_position.y -= 1
    x_first.append("A")

    # Save the position before modifying for option 2 (y-first)
    current_position = deepcopy(position)

    # Option 2: Move y first, then x
    y_first = []
    while current_position.y != next_position.y:
        if next_position.y > current_position.y:
            y_first.append(">")
            current_position.y += 1
        else:
            y_first.append("<")
            current_position.y -= 1
    while current_position.x != next_position.x:
        if next_position.x < current_position.x:
            y_first.append("^")
            current_position.x -= 1
        else:
            y_first.append("v")
            current_position.x += 1
    y_first.append("A")

    # Recurse with both options (x-first and y-first) and the remaining sequence
    generate_routes(
        sequence[1:],
        deepcopy(next_position),
        current_instruction + "".join(x_first),
        all_instructions,
    )

    generate_routes(
        sequence[1:],
        deepcopy(next_position),
        current_instruction + "".join(y_first),
        all_instructions,
    )


def calculate_length(sequences):
    instructions = []
    # Numpad instructions
    for sequence in sequences:
        instruction = ""
        position = deepcopy(numpad_positions["A"])
        for char in sequence:
            next_position = numpad_positions[char]
            while position.x != next_position.x:
                if next_position.x < position.x:
                    instruction += "^"
                    position.x -= 1
                else:
                    instruction += "v"
                    position.x += 1
            while position.y != next_position.y:
                if next_position.y > position.y:
                    instruction += ">"
                    position.y += 1
                else:
                    instruction += "<"
                    position.y -= 1
            instruction += "A"
        print("Robot 0", instruction)

        for extra_robots in range(2):
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
                    print(position, next_position)
                    if next_position.y > position.y:
                        new_instruction += ">"
                        position.y += 1
                    else:
                        new_instruction += "<"
                        position.y -= 1
                new_instruction += "A"
            print(f"Robot  {extra_robots} with {instruction}")
            instruction = new_instruction
        instructions.append(instruction)
        print(instruction)
        # Replace entry by new_instruction in array

    print("Instruction = ", instructions)
    total_complexity = 0
    for sequence, instruction in zip(sequences, instructions):
        sequence_len = int(re.search(r"\d+", sequence).group())
        path_len = len(instruction)
        print(sequence_len, path_len)
        total_complexity += sequence_len * path_len
    return total_complexity


# Main execution
if __name__ == "__main__":
    sequences = process_file("dummydata.txt")
    print(calculate_length(sequences))
    # sequences = process_file("data.txt")
    # print("Part 1:", calculate_length(sequences))
    # 160800 is too high
