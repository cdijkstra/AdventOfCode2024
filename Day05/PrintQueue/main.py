class SequenceProcessor:
    def __init__(self):
        # Initialize instance attributes
        self.data_dict = {}
        self.sequences = []
        self.score = 0

    def process_file(self, filename):
        """Read the file and split into list."""
        self.data_dict = {}
        self.sequences = []
        self.score = 0
        with open(filename, "r") as file:
            sequence = False
            for line in file:
                line = line.strip()
                if not line:
                    sequence = True
                    continue

                if not sequence:
                    nums = list(map(int, line.split("|")))
                    print(nums)
                    if nums[0] in self.data_dict:
                        print("Append", nums[1], "to", nums[0])
                        self.data_dict[nums[0]].append(nums[1])
                    else:
                        print("Add", nums[1], "to", nums[0])
                        self.data_dict[nums[0]] = [nums[1]]
                else:
                    seq = list(map(int, line.split(",")))
                    self.sequences.append(seq)

    def calculate_score(self):
        for sequence in self.sequences:
            if self.is_valid_move(sequence):
                print(sequence)
                self.score += sequence[(len(sequence) - 1) // 2]

        print(self.score)
        return self.score

    def is_valid_move(self, sequence):
        for i in range(1, len(sequence)):
            if sequence[i] in self.data_dict:
                for el in self.data_dict[sequence[i]]:
                    if el in sequence[:i]:
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
    processor.display_results()
    assert processor.calculate_score() == 143
