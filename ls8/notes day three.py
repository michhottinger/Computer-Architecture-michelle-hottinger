        
                
 """ 
CPU stack
push and pop instructions to use with the stack
components of a stack?
--push a thing on the stack, then store it
--store items in RAM is an option
--store in registers is another option but they are used for other thigs
register = [0] * 8

pc = 0  # Program Counter, index into memory of the current instruction
# AKA a pointer to the current instruction

fl = 0
sp = 7
register[sp] = 0xff

running = True

while running:
    inst = memory[pc]

    if inst == 1:  # PRINT_BEEJ
        print("Beej")
        pc += 1

    elif inst == 2:  # HALT
        running = False

    elif inst == 3:  # SAVE_REG
        reg_num = memory[pc + 1]
        value = memory[pc + 2]

        register[reg_num] = value

        pc += 3

    elif inst == 4: # PRINT_REG
        reg_num = memory[pc + 1]
        print(register[reg_num])

        pc += 2
        
    elif inst == 5:#push
    #decriment stack pointer
    register[sp] -= 1
    
    register[sp] &= 0xff#keeps r7 in the 
    
    #get register number
    reg_num = memeory[pc+1]
    value = register[reg_num]
    
    #store in memory
    address_to_push_to = register[sp]
    memeory [address_to_push_to] = value
    
    pc += 2
    
    elif inst ==6:
    #get value from RAM
        address_to_pop_from = register[sp]
        value = memory[addres_to_pop_from]
        
        #store in the given registery
        reg_num = memory[pc + 1]
        register[reg_num] = value
        
        #increment SP
        register[sp] +=1
        
        pc +=2

    else:
        print(f"Unknown instruction {inst}")
 
 
Day 4

3save register[subroutine addr]
2
6[subroutine addr]
7call r2
2halt
subroutine:
1print 
1print
1print
8ret



elif inst == CALL:
#get address of the next instruction
return_addr = pc + 2

#push that on the stack
register[sp] -= 1
address_to_push_to = register[sp]
memory[address_to_push_to] = return_addr]

#set the PC to the subroutine addres
reg_num = memory[pc + 1]
subroutine_addr = register[reg_num]

pc = subroutine_addr

elif inst == RET

#get reutrn address from top of stack

address_to_pop_from = self.reg[sp]
return_addr = self.ram[address_to_pop_from]
self.reg[sp] += 1

#set pc to return addr
self.pc = return_addr

MORE NOTES:

Rules:
when you call a function, push the return address onto the stack
when you return, pop the reutrn address off the stack (and store it in the pc)

Stack:
699: a = ?   |mains stack frame
698: b = ?  
697: [addr1]

696: x = 2
695: y = 7
694: z = ?
693: [addr2]


def mult2(x, y):
    z = x*y
    return z


def main():
    a = 2<---call it and pc moves here and sets a to 2
    
    #we must return to the middle of expression at = sign
    
    #addr2
    #v
    b = mult2(9a, 7)<---we can't assign b until we compute mult2
    print(b)#14
    return
    
main()<---pc is here at first

#[addr1]
#y

print("Done")

Interrupts




"""
