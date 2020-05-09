"""CPU functionality."""

import sys

# STOP THE PROGRAM FROM RUNNING
HLT = 0b00000001
# REGISTER register value
LDI = 0b10000010
# PRINT register
PRN = 0b10000010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 8
        self.reg = [0] * 8
        self.pc = 0
        self.running = False

    def load(self, path):
        """Load a program into memory."""

        if '.ls8' not in path:
            print('Not a valid program')
            print('HALTING NOW')
            return

        address = 0

        file = open(path, 'r')
        lines = file.readlines()

        for line in lines:

            if not line.startswith("#") and line.strip() != "":
                self.ram[address] = int(line.strip(), 2)

            address += 1

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, register):
        return self.ram[register]

    def ram_write(self, register, value):
        self.ram[register] = value

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

    def hlt(self):
        print('THE PROGRAM HAS HALTED')
        self.running = False
        self.pc += 1

    def ldi(self):
        register = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]

        print(f"[LDI] - Register: {register}, Value: {value}")

        self.ram_write(register, value)

        self.pc += 3

    def prn(self):
        register = self.ram_read(self.pc + 1)

        print(self.reg[register])

        self.pc += 2


    def run(self):
        """Run the CPU."""
    
        self.running = True

        while self.running:
            command = self.ram[self.pc]

            # HALT
            if command == 0b00000001:
                self.hlt()
            # LDI what does that even mean???
            elif command == 0b10000010:
                self.ldi()
            # PRN
            elif command == 0b01000111:
                self.prn()


