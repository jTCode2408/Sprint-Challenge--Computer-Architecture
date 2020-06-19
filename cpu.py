"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running=False
        self.ram = [0] *256
        self.reg =[0] *8
        self.pc =0
        self.stackp=7 #r7 is resreved top of stack location (r4 if empty)
        self.equal=False

    def ops(self, operation):
        branch_table ={
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MULT,
            0b00000001: self.HLT,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010110 : self.JNE,
            0b01010101: self.JEQ
        }

        if operation in branch_table:
            branch_table[operation]()

        else:
            print(f'Unknown instruction {operation} at address {self.pc}')
        sys.exit(1)

        
    def LDI(self):
        reg=self.ram_read(self.pc+1)
        value = self.ram_read(self.pc+2)
        self.reg[reg] =value
        self.pc+=3

    def PRN(self):
        reg=self.ram_read(self.pc+1)
        print(self.reg[reg])
        self.pc+=2

    def HLT(self):
        self.running =False
        self.pc+=1

    def MULT(self):
        self.alu('MULT', self.pc+1, self.pc+2)
        self.pc+=3

    def PUSH(self):
        #decrement stackp
        self.stackp -=1
        #set reg place
        reg = self.ram[self.pc + 1]
        #set val as reg splace
        value = self.reg[reg]
        #stackp is value
        self.ram[self.stackp] = value
        #move pc pointer
        self.pc += 2

    def POP(self):
        value = self.ram[self.stackp]
        #get next ram
        self.reg[self.ram[self.pc + 1]] = value
        #increment stackp
        self.stackp +=1
        self.pc += 2

        def CALL(self, operand_a, operand_b):
            self.PUSH(self.pc+2)
            self.pc =self.reg[operand_a]


        def RET(self):
            self.pc = self.POP()

        def CMP(self):
        def JMP(self):
        def JEQ(self):
        def JNE(self):

## check- Need Stack & CALL/RET (& subroutine calls) from Wed/Thrus emplimented to work?--
### CALL ###:
#subroutine (function) at the address stored in the register.
#address of instruction directly after CALL pushed on stack. #returns where we left off after fn finishes
#PC set to the address stored in the given register
# go to location in RAM and run 1st instruction
# PC can move forward or backwards from its current location.
#Machine code:
#01010000 00000rrr
#50 0r

##### SPRINT TASKS #######

#Add the CMP instruction and equal flag to your LS-8.
##- CMP:
#instruction handled by the ALU.
#CMP registerA registerB
#Compare the values in two registers.
#If equal, set the Equal E flag to 1, otherwise set it to 0.
#If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
#If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
#Machine code:
#10100111 00000aaa 00000bbb
#A7 0a 0b

#Add the JMP instruction.
##- JMP:
#Jump to the address stored in the given register.
#Set the PC to the address stored in the given register.
#Machine code:
#01010100 00000rrr
#54 0r

#Add the JEQ and JNE instructions.
##- JEQ:
#If equal flag is set (true), jump to address stored in the given register.
#Machine code:
#01010101 00000rrr
#55 0r

##- JNE:
#If E flag is clear (false, 0), jump to the address stored in the given register.
#Machine code:
#01010110 00000rrr
#56 0r

        
#Inside the CPU, there are two internal registers used for memory operations: 
 #mdr- data that was read/to write
 #mar- register address being read/written to

 #ram_read:ACCEPT ADDRESS TO READ-- and RETURNS VALUE @ address
 #ram_write:ACCEPT VALUE TO WRITE AND ADDRESS TO WRITE TO
    def ram_read(self, position):
        return self.ram[position]

    def ram_write(self, position, value):
        self.ram[position] =value


    def load(self, f):
        """Load a program into memory."""
        file = f
        program = open(f"{file}", "rb")
        address = 0
        for line in program:
            if line[0] == "0" or line[0] == "1":
                op = line.split("#", 1)[0]
                self.ram[address] = int(op, 2)
                address += 1
    
        # For now, we've just hardcoded a program:

        #program = [
         #   # From print8.ls8
          #  0b10000010, # LDI R0,8
           # 0b00000000,
           # 0b00001000,
           # 0b01000111, # PRN R0
           # 0b00000000,
           # 0b00000001, # HLT
        #]

        #for instruction in program:
         #   self.ram[address] = instruction
          #  address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MULT":
            self.reg[self.ram[reg_a]] * self.reg[self.ram[reg_b]]
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
#implement code to run
#read memory address
#store memory address in IR
##using ram_read(), read the bytes at PC+1 and PC+2 from RAM into variables operand_a and operand_b in case the instruction needs them.
        
        self.running =True

        while self.running:
            self.trace()
            ir= self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            #need to  call fn
            self.ops(ir)


