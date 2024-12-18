import re


def process_file(filename):
    """Read the file and split into list."""
    with open(filename, "r") as file:
        registers, instruction = file.read().split("\n\n")
        registers = list(map(int, re.findall(r"\d+", registers)))
        instruction = list(map(int, instruction.split()[1].split(",")))
        instruction = [
            (instruction[i], instruction[i + 1]) for i in range(0, len(instruction), 2)
        ]
        return registers, instruction


def combo_operand(operand):
    if 0 <= operand <= 3:
        return operand
    if 4 <= operand <= 6:
        return registers[operand - 4]
    else:
        raise RuntimeError("This operand should not occur", operand)


def process_instructions(instructions, registers):
    idx = 0

    output = []
    print(registers)
    while idx < len(instructions):
        opcode, operand = instructions[idx]
        print(opcode, operand)
        if opcode == 0:
            registers[0] //= 2 ** combo_operand(operand)
        elif opcode == 1:
            registers[1] ^= operand
        elif opcode == 2:
            registers[1] = combo_operand(operand) % 8
        elif opcode == 3 and registers[0] != 0:
            idx = operand - 1  # Correct for idx += 1 taking place later
        elif opcode == 4:
            registers[1] ^= registers[2]
        elif opcode == 5:
            print(combo_operand(operand))
            output.append(combo_operand(operand) % 8)
        elif opcode == 6:
            registers[1] = registers[0] // 2 ** combo_operand(operand)
        elif opcode == 7:
            registers[2] = registers[0] // 2 ** combo_operand(operand)
        idx += 1
        print(registers)

    result = ",".join(map(str, output))
    print(registers)
    return result, registers


def calculate_A_register(instructions, registers):
    # Every time A is divided by 8 (thanks to (0,3)) and we know that it should be less than 8 in the less step.
    possible_ranges = [range(0, 8), range(2, 4)]
    for possible_range in possible_ranges:
        print(possible_range)
        for num in possible_range:
            print(num)
    return 1


def find(program, ans):
    print(program, ans)
    if program == []:
        return ans
    for t in range(8):
        a = ans << 3 | t  # This is where the magic happens
        b = a % 8
        b = b ^ 3
        c = a // 2**b
        a //= 2**3
        b ^= a
        b ^= c
        if b % 8 == program[-1]:
            print("Yup:", a)
            sub = find(program[:-1], a)
            if sub is None:
                continue
            return sub


def find_test(program, ans):
    if program == []:
        return ans * 8
    for t in range(8):
        a = ans << 3 | t  # This is where the magic happens
        if a % 8 == program[-1]:
            sub = find_test(program[:-1], a)
            if sub is None:
                continue
            return sub


# Main execution
if __name__ == "__main__":
    registers, instructions = process_file("dummydata1.txt")
    output, registers = process_instructions(instructions, registers)
    assert registers[1] == 1
    registers, instructions = process_file("dummydata2.txt")
    output, registers = process_instructions(instructions, registers)
    assert output == "0,1,2"
    registers, instructions = process_file("dummydata3.txt")
    output, registers = process_instructions(instructions, registers)
    assert output == "4,2,5,6,7,7,7,7,3,1,0"
    assert registers[0] == 0
    registers, instructions = process_file("dummydata4.txt")
    output, registers = process_instructions(instructions, registers)
    assert registers[1] == 26
    registers, instructions = process_file("dummydata5.txt")
    output, registers = process_instructions(instructions, registers)
    assert registers[1] == 44354

    registers, instructions = process_file("dummydata_copy.txt")
    all_instructions = [x for tup in instructions for x in tup]
    print(all_instructions)
    ans = find_test(all_instructions, 0)
    print("Ans = ", ans)
    assert ans == 117440

    # registers, instructions = process_file("data.txt")
    # output, registers = process_instructions(instructions, registers)
    # print("Part 1:", output)

    registers, instructions = process_file("data.txt")
    all_instructions = [x for tup in instructions for x in tup]
    output = find(all_instructions, 0)
    # 130812005036816 is too low
    # 130812005036818 is too low
    print("Part 2:", output)
