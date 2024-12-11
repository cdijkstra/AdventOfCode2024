def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return list(map(int, file.readline().split()))


def blink(rocks, blinks):
    for blink in range(blinks):
        rock_index = 0
        print(rocks)
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

    print(rocks)
    return len(rocks)


# Main execution
if __name__ == "__main__":
    rocks = process_file("dummydata.txt")
    assert blink(rocks, 1) == 7

    rocks = process_file("dummydata2.txt")
    assert blink(rocks, 25) == 55312

    rocks = process_file("data.txt")
    print("Part 1:", blink(rocks, 25))
    rocks = process_file("data.txt")
    print("Part 2:", blink(rocks, 75))
