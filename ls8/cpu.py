"""CPU functionality."""

import sys
import re

# STOP THE PROGRAM FROM RUNNING
HLT = 0b00000001
# REGISTER register value
LDI = 0b10000010
# PRINT register
PRN = 0b01000111
# MUL
MUL = 0b10100010
ALU = [MUL]

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            self.ram[0] = HLT
            print('Not a valid program')
            print('HALTING NOW')
            return

        address = 0
        path = sys.argv[1]
        file = open(path, 'r')
        lines = file.readlines()

        for line in lines:
            line = re.sub('#.*', '', line)
            if line.strip() != "":
                self.ram[address] = int(line.strip(), 2)
                address += 1

    def ram_read(self, register):
        return self.ram[register]

    def ram_write(self, register, value):
        self.reg[register] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

        self.pc += 3

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
            if command == HLT:
                self.hlt()
            # LDI what does that even mean???
            elif command == LDI:
                self.ldi()
            # PRN
            elif command == PRN:
                self.prn()
            elif command == MUL:
                self.alu('MUL', self.ram_read(self.pc + 1),
                         self.ram_read(self.pc + 2))

