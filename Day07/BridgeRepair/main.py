import itertools


def process_file(filename):
    """Read the file and split into list."""
    parsed_data = []
    with open(filename, "r") as data:
        # Split the data into lines and process each line
        for line in data:
            # Split the line into result and the rest using the ':' delimiter
            result_part, numbers_part = line.split(":")

            # Parse the result as an integer
            result = int(result_part.strip())

            # Parse the rest of the numbers as integers
            numbers = list(map(int, numbers_part.strip().split()))

            # Combine result and numbers into a single list and add to the parsed data
            parsed_data.append([result] + numbers)
        return parsed_data


def add_valid_options(equations):
    answer = 0
    for equation in equations:
        result = equation[0]
        nums = equation[1:]
        if check_combinations(result, nums) != None:
            answer += result
    return answer


def check_combinations(result, numbers):
    operators = ["+", "*"]
    n = len(numbers) - 1  # Number of operators needed
    all_combinations = itertools.product(
        operators, repeat=n
    )  # Generate all combinations of + and *

    for ops in all_combinations:
        # Build the expression as a string
        expression = str(numbers[0])
        for num, op in zip(numbers[1:], ops):
            expression += f" {op} {num}"

        print(expression, "==", result, "and", eval(expression))
        # Evaluate the expression and check if it equals the result
        if eval(expression) == result:
            print("Yep", result, numbers)
            return expression  # Return the first valid expression that matches

    print("Nope", result, numbers)
    return None  # No valid combination found


# Main execution
if __name__ == "__main__":
    equations = process_file("dummydata.txt")
    print(equations)
    result = add_valid_options(equations)
    print(result)
