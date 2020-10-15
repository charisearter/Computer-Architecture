"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # inital ram to hold 256 bytes of memory
        self.reg = [0] * 8  # eight general purpose registers
        self.pc = 0  # program counter - address of currently executing instruction
        self.running = True  # CPU_run is running while true

    # Memory Address Register (mar) -- address or key we are writing value to
    # mar is address we are looking at and it is like an key in ram that returns the values at that address

    def ram_read(self, mar):
        return self.ram[mar]

    # Memory Data Register (mdr) -- what is being written to the value

    # add value to the address (mar) example ram(3,7) mar is 3 and the value will be mdr 7
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv) != 2:
            print("usage: comp.py progname")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    if line == '' or line[0] == "#":
                        continue
                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 2)
                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit(1)
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'SUB':
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == 'DIV':
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception(f"Unsupported ALU operation {op}")

    def trace(self):
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
        MUL = 0b10100010  # multiply
        PUSH = 0b01000101  # add to list
        POP = 0b01000110  # take away from list
        CALL = 0b01010000  # call the subroutine
        RET = 0b00010001  # mark end of subroutine (return)
        SP = 7  # stack pointer
        # operand_a = self.ram_read(self.pc + 1)  # store bytes for a at pc + 1
        # operand_b = self.ram_read(self.pc + 2)  # store bytes for b at pc + 2

        while self.running:
            IR = self.ram_read(self.pc)  # current instruction
            # store bytes for a at pc + 1
            operand_a = self.ram_read(self.pc + 1)
            # store bytes for b at pc + 2
            operand_b = self.ram_read(self.pc + 2)

            if IR == HLT:
                self.running = False
                self.pc = 0
                # Halt the function, exit
            elif IR == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif IR == PUSH:
                SP -= 1
                self.ram_write(SP, self.reg[operand_a])
                self.pc += 2
            elif IR == POP:
                self.reg[operand_a] = self.ram[SP]  # creates spot
                SP += 1  # increment stack pointer
                self.pc += 2
            elif IR == CALL:
                SP -= 1
                self.ram_write(SP, operand_b)
                self.pc = self.reg[self.ram_read(operand_a)]
            elif IR == RET:
                address = self.ram_read(SP)
                SP += 1
                self.pc = address
