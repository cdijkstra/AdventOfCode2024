import heapq
import math
import re
import time

button_pattern = r"Button (\w): X\+(\d+), Y\+(\d+)"
prize_pattern = r"Prize: X=(\d+), Y=(\d+)"


def process_file(filename):
    """Read the file and split into list."""
    parsed_data = []
    with open(filename, "r") as file:
        current_entry = {}  # Temporary storage for one group of data

        for line in file:
            line = line.strip()

            # Match Button entries
            button_match = re.match(button_pattern, line)
            if re.match(button_pattern, line):
                button, x_offset, y_offset = button_match.groups()
                current_entry[button] = {
                    "X_offset": int(x_offset),
                    "Y_offset": int(y_offset),
                }

            # Match Prize entry
            prize_match = re.match(prize_pattern, line)
            if prize_match:
                x_prize, y_prize = map(int, prize_match.groups())
                current_entry["Prize"] = {"X": x_prize, "Y": y_prize}

            # If the line is empty, it means a new block starts
            if not line and current_entry:
                # if current_entry:
                parsed_data.append(current_entry)
                current_entry = {}

        # Add the last entry if exists
        if current_entry:
            parsed_data.append(current_entry)

    return parsed_data


def calculate_prizes(contraptions):
    tokens_spent = 0
    for contraption in contraptions:
        # Find combinations to win, and calulcate the cheapest one
        bounds_a = [
            math.ceil(contraption["Prize"]["X"] / contraption["A"]["X_offset"]),
            math.ceil(contraption["Prize"]["Y"] / contraption["A"]["Y_offset"]),
        ]
        bounds_b = [
            math.ceil(contraption["Prize"]["X"] / contraption["B"]["X_offset"]),
            math.ceil(contraption["Prize"]["Y"] / contraption["B"]["Y_offset"]),
        ]

        lower_bound = int(
            min(min(bounds_a), min(bounds_b)) / 2
        )  # Save lower bound. Ensure we can at least apply A and B lower_bound times and stay below price

        matches = []
        for a in range(lower_bound, max(bounds_a)):
            for b in range(lower_bound, max(bounds_b)):
                if not (
                    a * contraption["A"]["X_offset"] + b * contraption["B"]["X_offset"]
                    == contraption["Prize"]["X"]
                    and a * contraption["A"]["Y_offset"]
                    + b * contraption["B"]["Y_offset"]
                    == contraption["Prize"]["Y"]
                ):
                    continue
                matches.append((a, b))

        if matches:
            best_combo = min(matches, key=lambda combo: combo[0] * 3 + combo[1] * 1)
            tokens_spent += best_combo[0] * 3 + best_combo[1] * 1
    return tokens_spent


def solve_solutions(contraptions):
    tokens_spent = 0
    for contraption in contraptions:
        # Justification of solution can be found in Solution.md
        A = (
            contraption["Prize"]["X"] * contraption["B"]["Y_offset"]
            - contraption["Prize"]["Y"] * contraption["B"]["X_offset"]
        ) / (
            contraption["A"]["X_offset"] * contraption["B"]["Y_offset"]
            - contraption["A"]["Y_offset"] * contraption["B"]["X_offset"]
        )
        B = (
            contraption["Prize"]["X"] - contraption["A"]["X_offset"] * A
        ) / contraption["B"]["X_offset"]

        if not (A.is_integer() and B.is_integer()):
            continue
        tokens_spent += A * 3 + B * 1
    return tokens_spent


# Main execution
if __name__ == "__main__":
    contraptions = process_file("dummydata.txt")
    assert calculate_prizes(contraptions) == 480
    assert solve_solutions(contraptions) == 480
    contraptions = process_file("data.txt")
    print("Part 1 =", calculate_prizes(contraptions))

    for contraption in contraptions:
        contraption["Prize"]["X"] += 10_000_000_000_000
        contraption["Prize"]["Y"] += 10_000_000_000_000
    print("Part 2 =", solve_solutions(contraptions))
