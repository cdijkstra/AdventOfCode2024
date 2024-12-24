def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        output = file.read().split("\n\n")

        gates = {
            key.strip(): int(value.strip())
            for key, value in (item.split(":") for item in output[0].split("\n"))
        }

        # Parsing instructions as tuples of (lhs, rhs)
        instructions = [
            (lhs.strip(), rhs.strip())  # Add instruction as a tuple (lhs, rhs)
            for instruction in output[1].split("\n")
            if " -> " in instruction  # Only process valid instructions
            for lhs, rhs in [instruction.split(" -> ")]
        ]
        return gates, instructions


def run_instructions(filename):
    gates, instructions = process_file(filename)
    processed_instructions = []
    while len(processed_instructions) < len(instructions):
        for key, value in instructions:
            if (key, value) in processed_instructions:
                continue

            entries = key.split()
            if not (entries[0] in gates and entries[2] in gates):
                continue

            # Values are know of first and second gate, so we can compute
            if entries[1] == "AND":
                gates[value] = gates[entries[0]] & gates[entries[2]]
            elif entries[1] == "OR":
                gates[value] = gates[entries[0]] | gates[entries[2]]
            elif entries[1] == "XOR":
                gates[value] = gates[entries[0]] ^ gates[entries[2]]
            else:
                raise Exception("Unknown operation")

            processed_instructions.append((key, value))

    filtered_instructions = dict(
        sorted(
            ((key, value) for key, value in gates.items() if key.startswith("z")),
            reverse=True,
        )
    )

    binary_string = "".join(str(value) for value in filtered_instructions.values())

    decimal_value = int(binary_string, 2)
    return decimal_value


# Main execution
if __name__ == "__main__":
    assert run_instructions("dummydata.txt") == 4
    assert run_instructions("dummydata2.txt") == 2024
    print("Part 1", run_instructions("data.txt"))
