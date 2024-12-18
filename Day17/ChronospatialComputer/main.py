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
    switch_dict = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: registers[0],  # Map to value of register A
        5: registers[1],  # Map to value of register B
        6: registers[2],  # Map to value of register C
    }
    return switch_dict.get(operand, "Default case")


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
    all_values = [x for tup in instructions for x in tup]
    value = 0
    for mod in all_values[::-1]:
        for N in range(value * 8, value * 8 + 8):
            if N % 8 != mod:
                continue
            print(range(value * 8, value * 8 + 8), mod, N)
            value = N  # Add an exclude range due to truncation
    return value * 8


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
    assert calculate_A_register(instructions, registers) == 117440

    registers, instructions = process_file("data.txt")
    output, registers = process_instructions(instructions, registers)
    print("Part 1:", output)

    registers, instructions = process_file("data.txt")
    output = calculate_A_register(instructions, registers)
    # 130812005036816 is too low
    # 130812005036818 is too low
    print("Part 2:", output)
