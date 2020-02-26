"""CPU functionality."""

import sys

#Add the HLT instruction definition to cpu.py so that you can refer to it by name instead of by numeric value.
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 #8 general purpose registers
        self.pc = 0 #also add properties for any internal registers you need, e.g. PC.
        self.ram = [0] * 256 #hold 256 bytes of memory (values 0 to 255)

    #In CPU, add method ram_read() and ram_write() that access the RAM inside the CPU object.
    #ram_read() should accept the address to read and return the value stored there.
    #Inside the CPU, there are two internal registers used for memory operations: 
    # the Memory Address Register (MAR) and the Memory Data Register (MDR).
    #The MAR contains the address that is being read or written to.
    def ram_read(self, MAR):
        return self.ram[MAR]

    #raw_write() should accept a value to write, and the address to write it to.
    #The MDR contains the data that was read or the data to write.
    def ram_write(self, MDR, MAR):
        self.ram[MDR] = MAR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b10000010, # LDI R1,9
            0b00000001,
            0b00001001,
            0b10100010, # MUL R0,R1
            0b00000000,
            0b00000001,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    #This is the workhorse function of the entire processor. It's the most difficult part to write.
    def run(self):
        """Run the CPU."""        
        running = True

        while True:
            #It needs to read the memory address that's stored in register PC, and store that result in IR, 
            # the Instruction Register. This can just be a local variable in run().
            IR = self.ram[self.pc]
            
            opcode = IR
            #Using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and 
            #operand_b in case the instruction needs them.

            #Some instructions requires up to the next one byte of data after the PC in memory to 
            #perform operations on.
            operand_a = self.ram_read(self.pc + 1) 

            #Some instructions requires up to the next two bytes of data after the PC in memory to 
            #perform operations on.
            operand_b = self.ram_read(self.pc + 2) 

            #Then, depending on the value of the opcode, perform the actions needed for the instruction 
            #per the LS-8 spec. Maybe an if-elif cascade...? There are other options, too.

            #We can consider HLT to be similar to Python's exit() in that we stop whatever we are doing, 
            # wherever we are.
            if opcode == HLT:
                sys.exit(0)
                self.pc += 1

            #LDI sets the value of a register to an 
            #address is self.ram[self.pc + 1]
            #value is self.ram[self.pc + 2]
            #so self.reg[operand_a] = operand_b is technically self.reg[address] = value
            elif opcode == LDI: 
                self.reg[operand_a] = operand_b
                self.pc += 3

            #Print numeric value stored in the given register. 
            #Print to the console the decimal integer value that is stored in the given register.
            elif opcode == PRN: 
                #at this point value is in self.reg[operand_a] as a result of line 119
                print(self.reg[operand_a])
                self.pc +=2

            #Multiply the values in two registers together and store the result in registerA.
            elif opcode == MUL: 
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3

            