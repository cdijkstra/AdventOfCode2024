import re
from collections import namedtuple
from copy import deepcopy


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        return list(map(int, re.findall(r"\d+", file.read())))


def calculate(secrets, secret_number):
    def transform_secret(secret):
        for _ in range(secret_number):
            secret ^= (secret * 64) % 16777216
            secret ^= secret // 32
            secret ^= (secret * 2048) % 16777216
        return secret

    return sum(transform_secret(secret) for secret in secrets)


# Main execution
if __name__ == "__main__":
    secrets = process_file("dummydata.txt")
    assert calculate(secrets, 2000) == 37327623
    secrets = process_file("data.txt")
    print("Part 1", calculate(secrets, 2000))
