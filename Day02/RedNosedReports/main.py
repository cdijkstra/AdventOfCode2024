def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return [list(map(int, line.strip().split())) for line in file]


def calculate_generic_safety_score(report):
    """
    Public function to determine the amount of generic safe reports.
    """
    safety_score = sum(int(_is_sequence_safe(line)) for line in report)
    return safety_score


def calculate_dampened_safety_score(report):
    """
    Public function to determine the amount of dampened safe reports.
    """
    safety_score = sum(int(_is_sequence_dampened_safe(line)) for line in report)
    return safety_score


def _is_sequence_dampened_safe(arr):
    if _is_sequence_safe(arr):
        return True

    for i in range(len(arr)):
        # Simulate removal by slicing the array. Not smartest solution, but performance is quite good
        modified_arr = arr[:i] + arr[i + 1 :]
        if _is_sequence_safe(modified_arr):
            return True

    # If no single removal makes the sequence safe, it's unsafe
    return False


def _is_sequence_safe(arr):
    """
    Private helper function to determine if an array satisfies the safety condition.
    """
    # First determine if all entries should be increasing or decreasing
    increasing = arr[1] - arr[0] > 0

    # Check if they all satsisfy this condition and have allowed diffs of 1,2,3
    for i in range(1, len(arr)):
        diff = arr[i] - arr[i - 1]
        if (increasing and diff not in [1, 2, 3]) or (
            not increasing and diff not in [-1, -2, -3]
        ):
            return False
    return True  # All pairs satisfy the safety condition


# Main execution
if __name__ == "__main__":
    report = process_file("dummydata.txt")
    assert calculate_generic_safety_score(report) == 2
    assert calculate_dampened_safety_score(report) == 4

    # Process the file once
    report = process_file("data.txt")

    # Part 1: Calculate generic safety
    print("Safety score:", calculate_generic_safety_score(report))

    # # Part 2: Calculate dampened safety
    print("Safety score:", calculate_dampened_safety_score(report))
