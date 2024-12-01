def process_file(filename):
    """Read the file and split into left and right entries."""
    left_entries = []
    right_entries = []
    with open(filename, "r") as file:
        for line in file:
            left, right = map(int, line.split())
            left_entries.append(left)
            right_entries.append(right)
    return left_entries, right_entries


def calculate_total_distance(left_entries, right_entries):
    sorted_left = sorted(left_entries)
    sorted_right = sorted(right_entries)
    distance = sum(
        abs(sorted_left[i] - sorted_right[i]) for i in range(len(left_entries))
    )
    return distance


def calculate_similarity_score(left_entries, right_entries):
    similarity_score = sum(right_entries.count(left) * left for left in left_entries)
    return similarity_score


# Main execution
if __name__ == "__main__":
    test_left_entries, test_right_entries = process_file("dummydata.txt")
    assert calculate_total_distance(test_left_entries, test_right_entries) == 11
    assert calculate_similarity_score(test_left_entries, test_right_entries) == 31

    # Process the file once
    left_entries, right_entries = process_file("data.txt")

    # Part 1: Calculate total distance
    total_distance = calculate_total_distance(left_entries, right_entries)
    print("Total Distance:", total_distance)

    # Part 2: Calculate similarity score
    similarity_score = calculate_similarity_score(left_entries, right_entries)
    print("Similarity Score:", similarity_score)
