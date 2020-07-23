        
                
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
        
"""
