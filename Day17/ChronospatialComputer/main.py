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
    while idx < len(instructions):
        opcode, operand = instructions[idx]
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
            output.append(combo_operand(operand) % 8)
        elif opcode == 6:
            registers[1] = registers[0] // 2 ** combo_operand(operand)
        elif opcode == 7:
            registers[2] = registers[0] // 2 ** combo_operand(operand)
        idx += 1

    result = ",".join(map(str, output))
    return result, registers


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

    registers, instructions = process_file("data.txt")
    output, registers = process_instructions(instructions, registers)
    print("Part 1:", output)
    # 3,5,3,4,6,3,0,7,0 is wrong
    # 6,2,7,6,4,3,1,5,7 is wrong
