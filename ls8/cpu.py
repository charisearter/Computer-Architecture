"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # inital ram to hold 256 bytes of memory
        self.register = [0] * 8  # eight general purpose registers
        self.pc = 0  # program counter - address of currently executing instruction

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

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

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


HLT = 0b00000001  # 0b preceding tells computer it is a binary number
LDI = 0b10000010
PRN = 0b01000111


def run(self):
    """Run the CPU."""
    # ir is instruction register
    # pc is the counter -> points us to memory location of ram
    running = True
    ir = self.ram[self.pc]  # current instruction
    operand_a = self.ram_read(self.pc + 1)  # store bytes for a at pc + 1
    operand_b = self.ram_read(self.pc + 2)  # store bytes for b at pc + 2

    while running:
        if ir == HLT:
            running = False
            self.pc = 0
            # Halt the function, exit
        elif ir == LDI:
            self.register[operand_a] = operand_b
            self.pc += 3
        elif ir == PRN:
            print(self.register[operand_a])
            self.pc += 2
        elif ir == HLT:
            self.pc = 0
            running = False
            # halt function
        '''
halted random py from class
'''
