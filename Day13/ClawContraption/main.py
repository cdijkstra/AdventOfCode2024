import math
import re
from collections import namedtuple

button_pattern = r"Button (\w): X\+(\d+), Y\+(\d+)"
prize_pattern = r"Prize: X=(\d+), Y=(\d+)"
Contraption = namedtuple("Contraption", ["ax", "ay", "bx", "by", "px", "py"])


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return [
            Contraption(*list(map(int, re.findall(r"\d+", contraption))))
            for contraption in file.read().split("\n\n")
        ]


# Brute-force solution
def calculate_prizes(contraptions):
    tokens_spent = 0
    for contraption in contraptions:
        # Find combinations to win, and calulcate the cheapest one
        bounds_a = [
            math.ceil(contraption.px / contraption.ax),
            math.ceil(contraption.py / contraption.ay),
        ]
        bounds_b = [
            math.ceil(contraption.px / contraption.bx),
            math.ceil(contraption.py / contraption.by),
        ]

        lower_bound = int(
            min(min(bounds_a), min(bounds_b)) / 2
        )  # Save lower bound. Ensure we can at least apply A and B lower_bound times and stay below price

        matches = []
        for a in range(lower_bound, max(bounds_a)):
            for b in range(lower_bound, max(bounds_b)):
                if not (
                    a * contraption.ax + b * contraption.bx == contraption.px
                    and a * contraption.ay + b * contraption.by == contraption.py
                ):
                    continue
                matches.append((a, b))

        if matches:
            best_combo = min(matches, key=lambda combo: combo[0] * 3 + combo[1] * 1)
            tokens_spent += best_combo[0] * 3 + best_combo[1] * 1
    return tokens_spent


# Elegant methematical solution
def solve_solutions(contraptions):
    tokens_spent = 0
    for contraption in contraptions:
        # Justification of solution can be found in Solution.md
        A = (contraption.px * contraption.by - contraption.py * contraption.bx) / (
            contraption.ax * contraption.by - contraption.ay * contraption.bx
        )
        B = (contraption.px - contraption.ax * A) / contraption.bx

        if not (A.is_integer() and B.is_integer()):
            continue
        tokens_spent += int(A) * 3 + int(B) * 1
    return tokens_spent


# Main execution
if __name__ == "__main__":
    contraptions = process_file("dummydata.txt")
    assert calculate_prizes(contraptions) == 480
    assert solve_solutions(contraptions) == 480
    contraptions = process_file("data.txt")
    print("Part 1 =", calculate_prizes(contraptions))

    for i, contraption in enumerate(contraptions):
        # Replace the contraption in the list with the updated one
        contraptions[i] = contraption._replace(
            px=contraption.px + 10_000_000_000_000,
            py=contraption.py + 10_000_000_000_000,
        )
    print("Part 2 =", solve_solutions(contraptions))
