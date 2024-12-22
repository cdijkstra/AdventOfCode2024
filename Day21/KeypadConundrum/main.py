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

# Main execution
if __name__ == "__main__":
    sequences = process_file("dummydata.txt")

    instructions = []
    # Numpad instructions
    for sequence in sequences:
        instruction = ""
        position = deepcopy(numpad_positions["A"])
        for char in sequence:
            next_position = numpad_positions[char]
            while position.y != next_position.y:
                print(position, next_position)
                if next_position.y > position.y:
                    instruction += ">"
                    position.y += 1
                else:
                    instruction += "<"
                    position.y -= 1
            while position.x != next_position.x:
                if next_position.x < position.x:
                    instruction += "^"
                    position.x -= 1
                else:
                    instruction += "v"
                    position.x += 1
            instruction += "A"
        instructions.append(instruction)

    for extra_robots in range(2):
        # Directional instructions
        for i, instruction in enumerate(instructions):  # Iterate with index
            new_instruction = ""
            position = deepcopy(directional_positions["A"])
            for char in instruction:
                next_position = directional_positions[char]
                while position.y != next_position.y:
                    print(position, next_position)
                    if next_position.y > position.y:
                        new_instruction += ">"
                        position.y += 1
                    else:
                        new_instruction += "<"
                        position.y -= 1
                while position.x != next_position.x:
                    if next_position.x < position.x:
                        new_instruction += "^"
                        position.x -= 1
                    else:
                        new_instruction += "v"
                        position.x += 1
                new_instruction += "A"
            instructions[i] = new_instruction
            # Replace entry by new_instruction in array

    print(instructions)
    for i in range(len(sequences)):
        sequence_len = int(re.search(r"\d+", sequences[i]).group())
        path_len = len(instructions[i])
        print(sequence_len, path_len)
