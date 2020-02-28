"""CPU functionality."""

import sys

#Add the HLT instruction definition to cpu.py so that you can refer to it by name instead of by numeric value.
HLT = 0b00000001 #HLT: halt the CPU and exit the emulator.
LDI = 0b10000010 #Set the value of a register to an integer.

#Print numeric value stored in the given register.
#Print to the console the decimal integer value that is stored in the given register.
PRN = 0b01000111

#MUL registerA registerB
#Multiply the values in two registers together and store the result in registerA.
MUL = 0b10100010

#Push the value in the given register on the stack.
#Decrement the SP.
#Copy the value in the given register to the address pointed to by SP.
PUSH = 0b01000101

#Pop the value at the top of the stack into the given register.
#Copy the value from the address pointed to by SP to the given register.
#Increment SP.
POP = 0b01000110

# R7 is reserved as the stack pointer (SP)
# The SP points at the value at the top of the stack (most recently pushed), 
# or at address F4 (0xF4) (Key pressed) F4 Holds the most recent key pressed on the keyboard if the stack is empty.
# Keyboard interrupt. This interrupt triggers when a key is pressed. The value of the key pressed 
# is stored in address 0xF4.
SP = 7  # Stack pointer is R7


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        """
        8 general-purpose 8-bit numeric registers R0-R7.
            R5 is reserved as the interrupt mask (IM)
            R6 is reserved as the interrupt status (IS)
            R7 is reserved as the stack pointer (SP)
        These registers only hold values between 0-255. After performing math on registers in the emulator, 
        bitwise-AND the result with 0xFF (255) to keep the register values in that range.
        """        

        #8 general purpose registers
        #start counting from 0: R0 - R7
        self.reg = [0] * 8 

        #also add properties for any internal registers you need, e.g. PC (program counter) 
        #lives at address 00
        self.pc = 0 

        self.ram = [0] * 256 #hold 256 bytes of memory (values 0 to 255)


    #In CPU, add method ram_read() and ram_write() that access the RAM inside the CPU object.
    #ram_read() should accept the address to read and return the value stored there.
    #Inside the CPU, there are two internal registers used for memory operations: 
    #the Memory Address Register (MAR) and the Memory Data Register (MDR).
    #The MAR contains the address that is being read or written to.
    def ram_read(self, MAR):
        #The MAR contains the address that is being read from
        return self.ram[MAR]

    #raw_write() should accept a value to write, and the address to write it to.
    #The MDR contains the data that was read or the data to write.
    def ram_write(self, MDR, MAR):
        #MDR holds the value to write
        #MAR holds the memory address we are writing to
        self.ram[MDR] = MAR

    """
    In load(), you will now want to use those command line arguments to open a file, read in its 
    contents line by line, and save appropriate data into RAM.
    """
    def load(self, file):
        """Load a program into memory."""

        try:
            address = 0

            with open(file) as f:
                for line in f:
                    #As you process lines from the file, you should be on the lookout for blank lines 
                    # (ignore them), and you should ignore everything after a #, since that's a comment.
                    # Parse out comments
                    comment_split = line.strip().split("#")

                    # Cast the numbers from strings to ints
                    value = comment_split[0].strip()

                    # Ignore blank lines
                    if value == "":
                        continue

                    #You'll have to convert the binary strings to integer values to store in RAM. 
                    #The built-in int() function can do that when you specify a number base as the 
                    #second argument:
                    int_value = int(value, 2)

                    #store int value in RAM
                    self.ram[address] = int_value
                    address += 1
                    
        
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {file} not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:
        """unhardcode the program
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
            address += 1"""

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

            #LDI sets the value of a register to an integer
            #address or operand_a is self.ram[self.pc + 1]
            #value or operand_b is self.ram[self.pc + 2]
            #so self.reg[operand_a] = operand_b is technically self.reg[address] = value
            elif opcode == LDI: 
                self.reg[operand_a] = operand_b
                #+ 3 because operand_a has the bytes at PC+1 and operand_b has the bytes at PC+2 
                self.pc += 3

            #Print numeric value stored in the given register. 
            #Print to the console the decimal integer value that is stored in the given register.
            elif opcode == PRN:                
                print(self.reg[operand_a])
                self.pc +=2

            #Multiply the values in two registers together and store the result in registerA.
            elif opcode == MUL: 
                self.reg[operand_a] *= self.reg[operand_b]
                #+ 3 because operand_a has the bytes at PC+1 and operand_b has the bytes at PC+2 
                self.pc += 3

            #Step 10: Implement System Stack
            #R7 is reserved for the Stack Pointer
            #Stack pointer points at 00 and when decremented it goes up to FF
            #The SP points at the value at the top of the stack (most recently pushed), or at 
            #address F4 if the stack is empty.
            elif opcode == PUSH:
                # grab the register argument
                #pc + 1 - the program counter is going to grab the register that we are looking at
                register = self.ram[self.pc + 1] #get register number from memory (for eg. R0)
                #then we can get our value from that register                
                val = self.reg[register] #then we look in that register to get the value that we are going to push
                # Decrement the SP or stack pointer => R7
                # the SP holds the address of wherever the top of our stack is
                self.reg[SP] -= 1
                # Copy the value in the given register to the address pointed to by SP.
                # push the value in the given register on to our stack
                # set that value to the value we got from our register
                self.ram[self.reg[SP]] = val #points to the address that is at the top of our stack
                self.pc += 2        

            elif opcode == POP:
                #grab the value from the top of the stack
                #this is where we are going to put the value that we pop off
                register = self.ram[self.pc + 1]
                #pop the value at the top of the stack (pointed to by SP) into the given register
                val = self.ram[self.reg[SP]]
                # Copy the value from the address pointed to by SP to the given register.
                self.reg[register] = val
                # Increment SP.
                self.reg[SP] += 1 #move our stack pointer back 1
                self.pc += 2



            

