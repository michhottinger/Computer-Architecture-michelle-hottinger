"""CPU functionality."""
"""
CPU
    Executing instructions
    Gets them out of RAM
    Registers (like variables)
        Fixed names  R0-R7
        Fixed number of them -- 8 of them
        Fixed size -- 8 bits

Memory (RAM)
    A big array of bytes
    Each memory slot has an index, and a value stored at that index
    That index into memory AKA:
        pointer
        location
        address
"""
"""
- [ ] Inventory what is here
- [ ] Implement the `CPU` constructor
- [ ] Add RAM functions `ram_read()` and `ram_write()`
- [ ] Implement the core of `run()`
- [ ] Implement the `HLT` instruction handler
- [ ] Add the `LDI` instruction
- [ ] Add the `PRN` instruction
"""
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

"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc =0
        self.branch_table = {
            0b01000111 : "PRN",
            0b00000001 : "HLT",
            0b10000010 : "LDI",
            0b10100010 : "MUL",
            0b01000101 : "PUSH",
            0b01000110 : "POP",
            0b01010000 : "CALL",
            0b01010100 : "JMP",
            0b00010001 : "RET"
        }
        

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

#         program = [
#             # From print8.ls8
#             0b10000010, # LDI R0,8
#             0b00000000,
#             0b00001000,
#             0b01000111, # PRN R0
#             0b00000000,
#             0b00000001, # HLT
#         ]

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

            #Memory Address Register_ (MAR) and the _Memory Data Register_ (MDR)
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
    
    def PRN(self, reg):
        print(self.reg[reg])
    
    def LDI(self, reg, value):
        self.reg[reg] = value
        
    def HLT(self):
        return False
        
    
    def alu(self, op, reg_a= None, reg_b = None):
        """ALU operations."""
        
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        
        elif op == "LDI":
            self.LDI(reg_a, reg_b)
            
        elif op == "PRN":
            self.PRN(reg_a)
        
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

    def run(self):
        """Run the CPU."""
        sp = 7#stack pointer
        self.reg[sp] = 0xf4 #start one above f3 then decrement
        running = True
        count = 1
    
        while running:
            ir = self.ram_read(self.pc) # Instruction Register, contains a copy of the currently executing instruction
            if ir in self.branch_table:
                self.branch_table[ir]
            
            if ir in self.branch_table and self.branch_table[ir] == "HLT":
                running = self.HLT()
               
          
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            
            if ir in self.branch_table and not self.branch_table[ir] == "HLT":
                
                if self.branch_table[ir] == "LDI":
                    self.LDI(operand_a, operand_b)
                
                elif self.branch_table[ir] == "PRN":
                    self.PRN(operand_a)
                
                elif self.branch_table[ir] == "PUSH":
                    #decrement stack pointer
                    self.reg[sp] -= 1
    
                    self.reg[sp] &= 0xff#keeps r7 in the range 00-ff
    
                    #get register number
                    reg_num = self.ram[self.pc+1]
                    value = self.reg[reg_num]
    
                    #store in memory
                    address_to_push_to = self.reg[sp]
                    self.ram[address_to_push_to] = value
     
                elif self.branch_table[ir] == "POP":
                    #get value from RAM
                    address_to_pop_from = self.reg[sp]
                    value = self.ram[address_to_pop_from]
        
                    #store in the given registery
                    reg_num = self.ram[self.pc + 1]
                    self.reg[reg_num] = value
        
                    #increment SP
                    self.reg[sp] +=1
                
                else: 
                    op = self.branch_table[ir]
                    self.alu(op, operand_a, operand_b)
                
            
            
            count +=1
               
            #print(self.alu(ir, operand_a, operand_b))
            if (ir & (1<< 7)) >> 7 ==1:
                self.pc += 3
            else:
                self.pc += 2
                
    
            if self.branch_table[ir] == "CALL":
                return_addr = self.pc + 2
                #push on the stack
                self.reg[sp] -=1
                self.ram[self.reg[sp]] = return_addr
                    
                #get the address to call
                reg_num = self.ram[self.pc + 1]
                subroutine_addr = self.reg[reg_num]
                    
                #call it
                self.pc = subroutine_addr
                    
            else:
                self.branch_table[ir] == "RET"
                pass
                    
