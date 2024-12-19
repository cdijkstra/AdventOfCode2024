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


def process_instructions(instructions, registers):
    idx = 0
    output = []

    def combo_operand(operand):
        if 0 <= operand <= 3:
            return operand
        if 4 <= operand <= 6:
            return registers[operand - 4]
        else:
            raise RuntimeError("This operand should not occur", operand)

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


def calculate_A_register(program):
    candidates = [0]
    count = 0
    for expected_output in program[::-1]:
        next_candidates = []
        for val in candidates:
            for i in range(8):
                target = (val << 3) + i
                output = computer(program, a=target)
                if output == expected_output:
                    next_candidates.append(target)
        count += 1
        candidates = next_candidates
    return min(candidates)


def computer(program, a: int, b: int = 0, c: int = 0) -> list[int]:

    def combo(val: int) -> int:
        assert val != 7, "Invalid combo value"
        if val <= 3:
            return val
        reg_map = {4: a, 5: b, 6: c}
        return reg_map[val]

    output = []
    ip = 0
    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]
        if opcode == 0:
            a = a >> combo(operand)
        elif opcode == 1:
            b = b ^ operand
        elif opcode == 2:
            b = combo(operand) % 8
        elif opcode == 4:
            b = b ^ c
        elif opcode == 5:
            output = combo(operand) % 8
        elif opcode == 6:
            b = a >> combo(operand)
        elif opcode == 7:
            c = a >> combo(operand)
        ip += 2
    return output


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
    flattened_instructions = [x for tup in instructions for x in tup]
    output, registers = process_instructions(instructions, registers)
    print("Part 1:", output)

    output = calculate_A_register(flattened_instructions)
    print("Part 2:", output)
