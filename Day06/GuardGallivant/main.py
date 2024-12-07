from collections import namedtuple


def process_file(filename):
    """Read the file and split into list."""
    parsed_data = []
    with open(filename, "r") as data:
        for line in data.strip().split("\n"):
            # Split the line into result and the rest using the ':' delimiter
            result_part, numbers_part = line.split(":")

            # Parse the result as an integer
            result = int(result_part.strip())

            # Parse the rest of the numbers as integers
            numbers = list(map(int, numbers_part.strip().split()))

            # Combine result and numbers into a single list and add to the parsed data
            parsed_data.append([result] + numbers)
        return parsed_data


# Main execution
if __name__ == "__main__":
    equations = process_file("dummydata.txt")
    print(equations)
