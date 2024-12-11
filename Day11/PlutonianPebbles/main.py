import copy


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return list(map(int, file.readline().split()))


def blink(rocks, blinks):
    # Create a copy of the rocks list to avoid modifying the original list
    rocks = rocks[:]
    for blink in range(blinks):
        rock_index = 0
        while rock_index < len(rocks):
            # Apply rules
            if rocks[rock_index] == 0:
                rocks[rock_index] = 1
            elif len(str(rocks[rock_index])) % 2 == 0:
                # Left half
                rock = str(rocks[rock_index])
                left_rock = int(rock[: len(rock) // 2])
                right_rock = int(rock[len(rock) // 2 :])

                rocks[rock_index] = left_rock
                rocks.insert(rock_index + 1, right_rock)

                rock_index += 1
            else:
                rocks[rock_index] *= 2024
            rock_index += 1

    return len(rocks)


def blink_memoization(rocks, blinks):
    rocks_occurrences = {}
    memo = {}  # Memoization dictionary
    for rock in rocks:
        rocks_occurrences[rock] = 1

    for blink in range(blinks):
        new_dict = copy.deepcopy(rocks_occurrences)
        for rock, occurrence in rocks_occurrences.items():
            if rock in memo.keys():
                for val in memo[rock]:
                    new_dict[val] = new_dict.get(val, 0) + occurrence
            else:
                # Apply rules
                if rock == 0:
                    new_entry = 1
                    memo[0] = [new_entry]
                    new_dict[new_entry] = new_dict.get(new_entry, 0) + occurrence
                elif len(str(rock)) % 2 == 0:
                    rock = str(rock)
                    left_rock = int(rock[: len(rock) // 2])
                    right_rock = int(rock[len(rock) // 2 :])

                    memo[rock] = [left_rock, right_rock]

                    new_dict[left_rock] = new_dict.get(left_rock, 0) + occurrence
                    new_dict[right_rock] = new_dict.get(right_rock, 0) + occurrence
                else:
                    new_entry = rock * 2024
                    memo[rock] = [new_entry]
                    new_dict[new_entry] = new_dict.get(new_entry, 0) + occurrence

            new_dict[int(rock)] = new_dict.get(int(rock), occurrence) - occurrence
            if new_dict[int(rock)] == 0:
                del new_dict[int(rock)]

        rocks_occurrences = new_dict

    return sum(rocks_occurrences.values())


# Main execution
if __name__ == "__main__":
    rocks = process_file("dummydata.txt")
    rocks2 = process_file("dummydata2.txt")

    assert blink(rocks, 1) == 7
    assert blink(rocks2, 6) == 22
    assert blink_memoization(rocks, 1) == 7
    assert blink_memoization(rocks2, 6) == 22
    assert blink_memoization(rocks2, 25) == 55312

    rocks = process_file("data.txt")
    print("Part 1:", blink(rocks, 25))
    print("Part 2:", blink_memoization(rocks, 75))
