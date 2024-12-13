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


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def minimize_cost(contraptions):
    for contraption in contraptions:
        # Extract values
        X_prize, Y_prize = contraption["Prize"]["X"], contraption["Prize"]["Y"]
        X_A, Y_A = contraption["A"]["X_offset"], contraption["A"]["Y_offset"]
        X_B, Y_B = contraption["B"]["X_offset"], contraption["B"]["Y_offset"]

        # Step 1: Calculate the GCD of the X and Y offsets for both buttons
        gcd_X = gcd(X_A, X_B)
        gcd_Y = gcd(Y_A, Y_B)

        # Step 2: Check if the prize's X and Y are divisible by the respective GCDs
        if X_prize % gcd_X != 0 or Y_prize % gcd_Y != 0:
            print("No solution exists")
            return None, float("inf")

        # Step 3: Find a reasonable range for n_A and n_B by checking multiples of GCD
        max_n_A = X_prize // X_A + 1
        max_n_B = Y_prize // Y_B + 1

        # Step 4: Use a better traversal strategy (explore in steps based on the GCDs)
        best_cost = float("inf")
        best_combo = None
        start_time = time.time()

        for n_A in range(0, max_n_A + 1):
            for n_B in range(0, max_n_B + 1):
                # Check if the current n_A and n_B satisfy the X and Y prize conditions
                cost = 3 * n_A + n_B  # 3 for pressing A, 1 for pressing B
                if (
                    n_A * X_A + n_B * X_B == X_prize
                    and n_A * Y_A + n_B * Y_B == Y_prize
                ):
                    if cost < best_cost:
                        best_cost = cost
                        best_combo = (n_A, n_B)

                # Print debug every 5 seconds to see progress
                if time.time() - start_time >= 5:
                    print(f"Investigating: n_A={n_A}, n_B={n_B}, cost={cost}")
                    start_time = time.time()  # Reset the timer

        if best_combo:
            print(f"Best combo: {best_combo}, Best cost: {best_cost}")
        else:
            print("No valid combination found")

        return best_combo, best_cost

    # If no solution is found
    return None, float("inf")


# Main execution
if __name__ == "__main__":
    contraptions = process_file("dummydata.txt")
    assert calculate_prizes(contraptions) == 480
    contraptions = process_file("data.txt")
    # print("Part 1 =", calculate_prizes(contraptions))

    for contraption in contraptions:
        contraption["Prize"]["X"] += 10_000_000_000_000
        contraption["Prize"]["Y"] += 10_000_000_000_000
    print("Part 2 =", minimize_cost(contraptions))
