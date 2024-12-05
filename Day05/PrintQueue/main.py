class SequenceProcessor:
    def __init__(self):
        # Initialize instance attributes
        self.data_dict = {}
        self.sequences = []

    def process_file(self, filename):
        """Read the file and split into list."""
        self.data_dict = {}
        self.sequences = []

        with open(filename, "r") as file:
            sequence = False
            for line in file:
                line = line.strip()
                if not line:
                    sequence = True
                    continue

                if not sequence:
                    nums = list(map(int, line.split("|")))
                    if nums[0] in self.data_dict:
                        self.data_dict[nums[0]].append(nums[1])
                    else:
                        self.data_dict[nums[0]] = [nums[1]]
                else:
                    seq = list(map(int, line.split(",")))
                    self.sequences.append(seq)

    def calculate_score(self):
        return sum(
            sequence[(len(sequence) - 1) // 2]
            for sequence in self.sequences
            if self.is_valid_move(sequence)
        )

    def calculate_shuffle_score(self):
        for sequence in self.sequences:
            if not self.is_valid_move(sequence):
                print("Invalid move", sequence)
                for i in range(0, len(sequence) - 1):
                    current_value = sequence[i]
                    vars = self.find_keys_with_value(current_value)

                    print("Entry", current_value, "Vars: ", vars)
                    for j in range(i + 1, len(sequence)):
                        el = sequence[j]
                        if el in vars:
                            sequence.pop(j)
                            print("Pop index", j, "El: ", el, "Insert at ", i)
                            sequence.insert(i, el)
                            print(sequence)

                            # Restart loop since the sequence has changed
                            break
                print("succes", sequence)

    def find_keys_with_value(self, target_value):
        return [key for key, value in self.data_dict.items() if target_value in value]

    def is_valid_move(self, sequence):
        for i in range(1, len(sequence)):
            current_value = sequence[i]

            if current_value in self.data_dict:
                associated_elements = self.data_dict[current_value]
                if any(el in associated_elements for el in sequence[:i]):
                    return False
        return True

    def display_results(self):
        """Display the contents of the dictionary and sequences."""
        print("Dictionary:", self.data_dict)
        print("Sequences:", self.sequences)


# Main execution
if __name__ == "__main__":
    processor = SequenceProcessor()
    processor.process_file("dummydata.txt")
    assert processor.calculate_score() == 143
    assert processor.calculate_shuffle_score() == 143

    processor.process_file("data.txt")
    print("Part 1", processor.calculate_score())
    print("Part 2", processor.calculate_shuffle_score())
