#the cleanest code I found on the interwebsssssss
#to learn how to clean code nicely

## ALU ops
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
INC = 0b01100101
DEC = 0b01100110
CMP = 0b10100111
AND = 0b10101000
NOT = 0b01101001
OR  = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101

## PC mutators
CALL = 0b01010000
RET  = 0b00010001
INT  = 0b01010010
IRET = 0b00010011
JMP  = 0b01010100
JEQ  = 0b01010101
JNE  = 0b01010110
JGT  = 0b01010111
JLT  = 0b01011000
JLE  = 0b01011001
JGE  = 0b01011010

## Other
NOP  = 0b00000000
HLT  = 0b00000001
LDI  = 0b10000010
LD   = 0b10000011
ST   = 0b10000100
PUSH = 0b01000101
POP  = 0b01000110
PRN  = 0b01000111
PRA  = 0b01001000



import sys
#used in the system:
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JNE = 0b01010110
JEQ = 0b01010101

CALL = 0b01010000
PUSH = 0b01000101


class CPU2:
    def __init__(self):
        """Construct A New CPU"""
        # build out registers
        self.registers = [0] * 8
        # build out RAM
        self.ram = [0] * 256
        # set Program Counter (PC)
        self.pc = 0
        # set Stack Pointer (SP) index in our register, will always point to position 7 in our Registers
        self.sp = 7
        # Assign SP to the value of 244 in our RAM
        self.registers[7] = 0xF4
        # Dict to hold FL
        self.flags = {}
        # Construct a branch table
        self.branch_table = {}
        self.branch_table[JEQ] = self.jeq
        self.branch_table[JMP] = self.jmp
        self.branch_table[JNE] = self.jne
        self.branch_table[CMP] = self.cmp_func
        self.branch_table[LDI] = self.ldi
        self.branch_table[PRN] = self.prn
        self.branch_table[ADD] = self.add
        self.branch_table[MUL] = self.mul
        self.branch_table[PUSH] = self.push
        self.branch_table[POP] = self.pop
        self.branch_table[CALL] = self.call
        self.branch_table[RET] = self.ret

    def load(self, filename):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        address = 0

        program = []
        with open (sys.argv[1]) as f:
            for line in f:
                try: 
                    line = line.split("#", 1)[0]
                    line = int(line, 2)
                    program.append(line)
                except ValueError:
                    pass
                
                
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    # ALU to perform arithmatic operations and also CMP operations
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        # vars to be used for flagging
        a = self.registers[reg_a]
        b = self.registers[reg_b]

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        elif op == "CMP":
            if a == b:
                self.flags['E'] = 1
            else:
                self.flags['E'] = 0
            if a < b:
                self.flags['L'] = 1
            else:
                self.flags['L'] = 0
            if a > b:
                self.flags['G'] = 1
            else:
                self.flags['G'] = 0
        else:
            raise Exception("Unsupported ALU operation")

    def read_ram(self, MAR):
        return self.ram[MAR]

    def write_ram(self, MAR, MDR):
        self.ram[MAR] = MDR

    def jeq(self, a=None, b=None):
        if self.flags['E'] == 1:
            self.pc = self.registers[a]
        else:
            self.pc += 2

    def jmp(self, a=None, b=None):
        self.pc = self.registers[a]

    def jne(self, a=None, b=None):
        if self.flags['E'] == 0:
            self.pc = self.registers[a]
        else:
            self.pc += 2

    def cmp_func(self, a=None, b=None):
        self.alu("CMP", a, b)

    def ldi(self, a=None, b=None):
        self.registers[a] = b

    def prn(self, a=None, b=None):
        print(self.registers[a])

    def add(self, a=None, b=None):
        self.alu("ADD", a, b)

    def mul(self, a=None, b=None):
        self.alu("MUL", a, b)

    def push(self, a=None, b=None):
        self.registers[self.sp] -= 1
        val = self.registers[a]
        self.write_ram(self.registers[self.sp], val)

    def pop(self, a=None):
        val = self.read_ram(self.registers[self.sp])
        self.registers[a] = val
        self.registers[self.sp] += 1

    def call(self, b=None):
        val = self.pc + 2
        self.registers[self.sp] -= 1
        self.write_ram(self.registers[self.sp], val)
        reg = self.read_ram(self.pc + 1)
        addr = self.registers[reg]
        self.pc = addr

    def ret(self):
        ret_addr = self.registers[self.sp]
        self.pc = self.read_ram(ret_addr)
        self.registers[self.sp] += 1

    def run(self):
        """Run The CPU"""

        # a dict to check for jump instructions
        jump = [CALL, JNE, RET, JMP, JEQ]

        while True:
            IR = self.read_ram(self.pc)
            operand_a = self.read_ram(self.pc + 1)
            operand_b = self.read_ram(self.pc + 2)
            if IR == HLT:
                print("Exiting program...")
                sys.exit(1)
            elif IR in jump:
                self.branch_table[IR](operand_a, operand_b)
            elif IR in self.branch_table:
                self.branch_table[IR](operand_a, operand_b)
                self.pc += (IR >> 6) + 1
            else:
                print(IR)