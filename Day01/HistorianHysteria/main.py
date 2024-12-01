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


# Part 1
with open("data.txt", "r") as file:
    left_entries = []
    right_entries = []

    # Iterate through each line in the file
    for line in file:
        # Split the line into two numbers and convert them to integers
        left, right = map(int, line.split())
        left_entries.append(left)
        right_entries.append(right)

sorted_left_entries = sorted(left_entries)
sorted_right_entries = sorted(right_entries)
sum = 0
for i in range(len(left_entries)):
    sum += abs(sorted_left_entries[i] - sorted_right_entries[i])

print(sum)

# Part 2
with open("data.txt", "r") as file:
    left_entries = []
    right_entries = []

    # Iterate through each line in the file
    for line in file:
        # Split the line into two numbers and convert them to integers
        left, right = map(int, line.split())
        left_entries.append(left)
        right_entries.append(right)

sorted_left_entries = sorted(left_entries)
sorted_right_entries = sorted(right_entries)
similarity_score = 0
for i in range(len(left_entries)):
    similarity_score += right_entries.count(left_entries[i]) * left_entries[i]

print(similarity_score)
