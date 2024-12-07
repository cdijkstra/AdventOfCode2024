import itertools


def process_file(filename):
    """Read the file and split into list."""
    parsed_data = []
    with open(filename, "r") as data:
        # Split the data into lines and process each line
        for line in data:
            # Split the line into result and the rest using the ':' delimiter
            result_part, numbers_part = line.split(":")
            result = int(result_part.strip())
            numbers = list(map(int, numbers_part.strip().split()))

            # Combine result and numbers into a single list and add to the parsed data
            parsed_data.append([result] + numbers)
        return parsed_data


def add_valid_options(equations, operators=["+", "*"]):
    answer = 0
    for equation in equations:
        result = equation[0]
        nums = equation[1:]
        if contains_valid_combination(result, nums, operators) is not None:
            answer += result
    return answer


operations = {
    "||": lambda a, b: int(str(a) + str(b)),  # Concatenate
    "+": lambda a, b: a + b,  # Addition
    "*": lambda a, b: a * b,  # Multiplication
}


def contains_valid_combination(result, numbers, operators=["+", "*"]):
    n = len(numbers) - 1  # Number of operators needed
    all_combinations = itertools.product(
        operators, repeat=n
    )  # Generate all combinations of operators

    for ops in all_combinations:
        current_val = numbers[0]
        for num, op in zip(numbers[1:], ops):
            current_val = operations[op](current_val, num)

        if current_val == result:
            return True  # Return the first valid expression that matches

    return None  # No valid combination found


# Main execution
if __name__ == "__main__":
    equations = process_file("dummydata.txt")
    assert add_valid_options(equations) == 3749
    assert add_valid_options(equations, operators=["+", "*", "||"]) == 11387

    equations = process_file("data.txt")
    print("Part 1;", add_valid_options(equations))
    print("Part 2;", add_valid_options(equations, operators=["+", "*", "||"]))
