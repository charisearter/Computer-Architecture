"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # initialize the ram to hold 256 bytes of memory
        self.reg = [0] * 8  # eight general purpose registers
        # self.reg[7] is the reserved index of the Stack Pointer (SP)
        self.pc = 0  # program counter - address of currently executing instruction
        self.running = True  # CPU_run is running while true loop
        # Flag is set to no operation (NOP) because it doesn't do anything until certain CMP conditions are set in ALU
        self.FL = 0
    # Memory Address Register (MAR) -- Holds memory address we're reading/writing
    # MAR is address we are looking at and it is like a key in ram that returns the values at that address

    def ram_read(self, MAR):
        return self.ram[MAR]

    # Memory Data Register (MDR) - holds value of what was just read
    # add value to the address (MAR) key:value MAR is key : MDR is valye MAR:MDR
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        address = 0  # counter for index
        if len(sys.argv) != 2:  # if sys.argc is not 2, something is missing
            print("usage: comp.py progname")  # print this
            sys.exit(1)  # exit ... no idea what 1 means
        try:  # sys.argv takes 2 arguments. 1st argument is program file running
            with open(sys.argv[1]) as f:  # open the file at index 1 (2nd argument)
                for line in f:  # for each line in the file (f)
                    line = line.strip()  # take away any leading or trailing spaces (whitespace)
                    # if line is empty or starts with #
                    if line == '' or line[0] == "#":
                        continue  # go to the next one
                    try:
                        # splits # away and starts where it needs to be
                        str_value = line.split("#")[0]
                        # changes into integer at base 2
                        value = int(str_value, 2)
                    except ValueError:  # if none of these work
                        # print this error with the string value
                        print(f"Invalid number: {str_value}")
                        sys.exit(1)  # exit
                    # add the value at the index of whatever the address counter is
                    self.ram[address] = value
                    address += 1  # increment address counter
        except FileNotFoundError:  # if no file found
            print(f"File not found: {sys.argv[1]}")  # print error
            sys.exit(2)  # exit

    def alu(self, op, reg_a, reg_b):  # Algorithmic Logic Unit (ALU)
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] == self.reg[reg_b]:  # E A == B
                self.FL |= 0b00000001
                self.FL &= 0b11111001  # mask
            if self.reg[reg_a] < self.reg[reg_b]:  # L A < B
                self.FL |= 0b00000100
                self.FL &= 0b11111100  # mask
            if self.reg[reg_a] > self.reg[reg_b]:  # G A > B
                self.FL |= 0b00000010
                self.FL &= 0b11111010  # mask
        else:
            # if none work give this error
            raise Exception(f"Unsupported ALU operation {op}")

    def trace(self):  # don't touch this
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # Instruction codes
        HLT = 0b00000001  # halt -- 0b preceding tells computer it is a binary number
        LDI = 0b10000010  # load
        PRN = 0b01000111  # print
        ADD = 0b10100000  # add
        SUB = 0b10100001  # subtract
        MUL = 0b10100010  # multiply
        PUSH = 0b01000101  # add to list
        POP = 0b01000110  # take away from list
        CALL = 0b01010000  # call the subroutine
        RET = 0b00010001  # mark end of subroutine (return)
        CMP = 0b10100111  # handled by ALU and uses Flags
        # If equal (E) flag is set, jump to the address stored in the given register
        JEQ = 0b01010101  # jump is equal
        JMP = 0b01010100  # jump to address stored in given register, set PC to that address
        # if not equal (E = false), jump to address stored in given register
        JNE = 0b01010110  # jump is not equal
        SP = 7  # stack pointer - reserved index of self.reg
        # operand_a = self.ram_read(self.pc + 1)  # store bytes for a at pc + 1
        # operand_b = self.ram_read(self.pc + 2)  # store bytes for b at pc + 2

        while self.running:
            # Instruction Register (IR) -> holds the copy of the currently executing instruction
            IR = self.ram_read(self.pc)
            # store bytes for a at pc + 1
            operand_a = self.ram_read(self.pc + 1)
            # store bytes for b at pc + 2
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:  # HALT
                self.running = False
            elif IR == LDI:  # Load
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:  # Print
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == ADD:  # Add
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif IR == SUB:  # Subtract
                self.alu("SUB", operand_a, operand_b)
                self.pc += 3
            elif IR == MUL:  # Multiply
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif IR == CMP:  # compare
                self.alu('CMP', operand_a, operand_b)
                self.pc += 3
            elif IR == JMP:  # jump
                self.pc = self.reg[operand_a]
            elif IR == JEQ:  # Jump is equal
                if self.FL == 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == JNE:  # jump is not equal
                if self.FL != 1:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == PUSH:  # Push - insert
                SP -= 1
                self.ram_write(SP, self.reg[operand_a])
                self.pc += 2
            elif IR == POP:  # Pop - remove # from on the right   to = from
                # creates spot -- to on the left hand side
                self.reg[operand_a] = self.ram[SP]
                SP += 1  # increment stack pointer
                self.pc += 2
            elif IR == CALL:
                value = self.pc + 2  # the address of next instruction after call
                SP -= 1  # decrement
                self.ram[SP] = value  # writes value at index SP in ram
                # sets PC to register of wherever it needs to go
                self.pc = self.reg[operand_a]
            elif IR == RET:
                # pops off value stored from stack and set PC to it to go back to it
                self.pc = self.ram[SP]
                SP += 1  # increment
            else:  # otherwise
                print(f'Unknown instruction {IR} at address {self.pc}')
                sys.exit()
