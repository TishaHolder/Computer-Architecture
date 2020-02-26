import sys

PRINT_BEEJ     = 1
HALT           = 2
PRINT_NUM      = 3
SAVE           = 4  # Save a value to a register
PRINT_REGISTER = 5  # Print the value in a register
ADD            = 6  # ADD 2 registers, store the result in 1st reg
PUSH           = 7
POP            = 8


memory = [0] * 32

register = [0] * 8

pc = 0  # Program counter

SP = 7  # Stack pointer is R7


def load_memory(filename):
    try:
        address = 0
        # Open the file
        with open(filename) as f:
            # Read all the lines
            for line in f:
                # Parse out comments
                comment_split = line.strip().split("#")

                # Cast the numbers from strings to ints
                value = comment_split[0].strip()

                # Ignore blank lines
                if value == "":
                    continue

                num = int(value)
                memory[address] = num
                address += 1

    except FileNotFoundError:
        print("File not found")
        sys.exit(2)


if len(sys.argv) != 2:
    print("ERROR: Must have file name")
    sys.exit(1)

load_memory(sys.argv[1])


while True:
    command = memory[pc]
    print(memory)
    print(register)

    if command == PRINT_BEEJ:
        print("Beej!")
        pc += 1
    elif command == PRINT_NUM:
        num = memory[pc + 1]
        print(num)
        pc += 2
    elif command == SAVE:
        # Save a value to a register
        num = memory[pc + 1]
        reg = memory[pc + 2]
        register[reg] = num
        pc += 3
    elif command == PRINT_REGISTER:
        # Print the value in a register
        reg = memory[pc + 1]
        print(register[reg])
        pc += 2
    elif command == ADD:
        # ADD 2 registers, store the result in 1st reg
        reg_a = memory[pc + 1]
        reg_b = memory[pc + 2]
        register[reg_a] += register[reg_b]
        pc += 3
    elif command == PUSH:
        # Grab the register argument
        reg = memory[pc + 1]
        val = register[reg]
        # Decrement the SP.
        register[SP] -= 1
        # Copy the value in the given register to the address pointed to by SP.
        memory[register[SP]] = val
        pc += 2
    elif command == POP:
        # Graph the value from the top of the stack
        reg = memory[pc + 1]
        val = memory[register[SP]]
        # Copy the value from the address pointed to by SP to the given register.
        register[reg] = val
        # Increment SP.
        register[SP] += 1
        pc += 2
    elif command == HALT:
        sys.exit(0)
    else:
        print(f"I did not understand that command: {command}")
        sys.exit(1)

