"""CPU functionality."""

import sys

# Instruction codes
HLT = 0b00000001  # halt -- 0b preceding tells computer it is a binary number
LDI = 0b10000010  # load
PRN = 0b01000111  # print
ADD = 0b10100000  # add
SUB = 0b10100001  # subtract
MUL = 0b10100010  # multiply
DIV = 0b10100011  # divide
PUSH = 0b01000101  # add to list
POP = 0b01000110  # take away from list
CALL = 0b01010000  # call the subroutine
RET = 0b00010001  # mark end of subroutine


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # inital ram to hold 256 bytes of memory
        self.reg = [0] * 8  # eight general purpose registers
        self.pc = 0  # program counter - address of currently executing instruction
        self.ir = None  # instruction register that holds copy of currently exexuting instruction
        self.reg[7] = 0xF4  # stack process @ index 7 of register
        self.running = True  # CPU_run is running while true
        self.branchtable = {}  # setting up the branch table
        self.branchtable[HLT] = self.HLT
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[POP] = self.POP
        self.branchtable[CALL] = self.CALL
        self.branchtable[RET] = self.RET

    def HLT(self):  # HALT
        self.running = False
        sys.exit()

    def LDI(self):
        register_index = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[register_index] = value

    def PRN(self):
        register_index = self.ram_read(self.pc + 1)
        print(self.reg[register_index])

    def PUSH(self):
        self.reg[7] -= 1  # decrement stack
        register_index = self.ram_read(self.pc + 1)
        value = self.reg[register_index]
        self.ram_write(self.reg[7], value)

    def POP(self):
        value = self.ram_read(self.reg[7])
        register_index = self.ram_read(self.pc + 1)
        self.reg[register_index] = value
        self.reg[7] += 1  # add to stack

    def CALL(self):
        self.reg[7] -= 1  # decrement stack
        self.ram_write(self.reg[7], self.pc + 2)
        address = self.reg[self.ram_read(self.pc + 1)]
        self.pc = address

    def RET(self):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1  # add to stack

    def add(self, op1=None, op2=None):
        self.alu('ADD', op1, op2)

    def mul(self, op1=None, op2=None):
        self.alu('MUL', op1, op2)

    def sub(self, op1=None, op2=None):
        self.alu('SUB', op1, op2)

    def div(self, op1=None, op2=None):
        self.alu('DIV', op1, op2)

    # Memory Address Register (mar) -- address or key we are writing value to
    # mar is address we are looking at and it is like an key in ram that returns the values at that address

    def ram_read(self, mar):
        return self.ram[mar]

    # Memory Data Register (mdr) -- what is being written to the value

    # add value to the address (mar) example ram(3,7) mar is 3 and the value will be mdr 7
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):  # add file_to_open to self???
        """Load a program into memory."""
        address = 0
        #file_to_open = '/examples/mult.ls8'

        with open('ls8/examples/mult.ls8', 'r') as f:
            program = f.readlines()

        for instruction in program:
            if instruction.startswith('#'):
                continue
            self.ram[address] = int(instruction.split(' ')[0], 2)
            address += 1

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

    def run(self):
        """Run the CPU."""
        # operand_a = self.ram_read(self.pc + 1)  # store bytes for a at pc + 1
        # operand_b = self.ram_read(self.pc + 2)  # store bytes for b at pc + 2

        while self.running:
            self.ir = self.ram_read(self.pc)  # current instruction
            # store bytes for a at pc + 1
            operand_a = self.ram_read(self.pc + 1)
            # store bytes for b at pc + 2
            operand_b = self.ram_read(self.pc + 2)
            # get # of operands
            num_of_operands = self.ir >> 6  # ir shifted to the right by 6 bitwise

            # if it is an ALU instruction
            # 1 and ir is shifted to the right by 5 bitwise
            is_alu_operation = (self.ir >> 5) & 0b1

            if is_alu_operation:
                self.alu(self.ir, operand_a, operand_b)
            else:
                self.branchtable[self.ir]()

            # does instruction set PC directly
            # 1  and ir is shifted to the right by 4 bitwise
            set_pc = (self.ir >> 4) & 0b0001

            if not set_pc:  # then point the PC to the next instruction in the memory
                self.pc += num_of_operands + 1

            # if ir == HLT:
            #     self.running = False
            #     self.pc = 0
            #     # Halt the function, exit
            # elif ir == LDI:
            #     self.reg[operand_a] = operand_b
            #     self.pc += 3
            # elif ir == PRN:
            #     print(self.reg[operand_a])
            #     self.pc += 2

            #     # halt function
