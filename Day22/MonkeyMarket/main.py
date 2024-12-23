import re
from collections import namedtuple
from copy import deepcopy


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return list(map(int, re.findall(r"\d+", file.read())))


def transform_secret(secret, secret_number):
    for _ in range(secret_number):
        secret ^= (secret * 64) % 16777216
        secret ^= secret // 32
        secret ^= (secret * 2048) % 16777216
    return secret


def calculate(secrets, secret_number):
    return sum(transform_secret(secret, secret_number) for secret in secrets)


def calculate_max_bananas(secrets):
    seq_total = {}

    for secret in secrets:
        sequence = [secret % 10]
        for _ in range(2000):
            secret = transform_secret(secret, 1)
            sequence.append(secret % 10)
        seen = set()
        for idx in range(len(sequence) - 4):
            a, b, c, d, bananas = sequence[idx : idx + 5]
            seq = (b - a, c - b, d - c, bananas - d)
            if seq in seen:
                continue  # Otherwise we increase the dict value repeatedly

            seen.add(seq)
            seq_total[seq] = seq_total.get(seq, 0) + bananas

    return max(seq_total.values())


# Main execution
if __name__ == "__main__":
    secrets = process_file("dummydata.txt")
    assert calculate(secrets, 2000) == 37327623
    secrets = process_file("dummydata2.txt")
    assert calculate_max_bananas(secrets) == 23
    secrets = process_file("data.txt")
    print("Part 1", calculate(secrets, 2000))
    print("Part 2", calculate_max_bananas(secrets))
