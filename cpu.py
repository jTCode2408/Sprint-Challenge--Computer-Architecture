"""CPU functionality."""
import sys

#ops
LDI = 0b10000010 
PRN = 0b01000111
HLT = 0b00000001 
MUL = 0b10100010
PUSH = 0b01000101 
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
JMP = 0b01010100
CMP = 0b10100111
JNE = 0b01010110
JEQ = 0b01010101

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running=True
        self.ram = [0] *256
        self.reg =[0] *8
        self.pc =0
        self.sp=7 #r7 is resreved top of stack location
        self.E=True #Equal flag
        self.branch_table ={
        LDI: self.LDI, 
        PRN: self.PRN,
        HLT: self.HLT,
        MUL: self.MUL,
        PUSH: self.PUSH, 
        POP: self.POP,
        CALL: self.CALL,
        RET: self.RET,
        JMP: self.JMP,
        CMP: self.CMP,
        JNE: self.JNE,
        JEQ: self.JEQ
        }

    def LDI(self): #3bit op
        reg=self.ram_read(self.pc+1) #read reg
        value = self.ram_read(self.pc+2) 
        self.reg[reg] =value #get val at reg
        self.pc+=3 #move pc

    def PRN(self):#2bit op
        reg=self.ram_read(self.pc+1) #read reg
        value =self.reg[reg]#get reg  val
        print(value)#print val
        self.pc+=2

    def HLT(self):
        self.running =False
        self.pc+=1

    def MUL(self):#3bit op
        self.alu('MUL', self.pc+1, self.pc+2)
        self.pc+=3

    def PUSH(self):
        self.sp -=1 #decrement sp
        reg = self.ram[self.pc + 1] ##get val to store
        value = self.reg[reg] #set val to push
        self.ram[self.sp] = value #store val
        self.pc += 2 #move pc

    def POP(self):
        value = self.ram[self.sp]#set val to stack loc
        self.reg[self.ram[self.pc + 1]] = value #set val from stack loc
        self.sp +=1 #move sp
        self.pc += 2 #move pc
### CALL ###:
#subroutine (function) at the address stored in the register.
#address of instruction directly after CALL pushed on stack. #returns where we left off after fn finishes
#PC set to the address stored in the given register
# go to location in RAM and run 1st instruction
# PC can move forward or backwards from its current location.
#01010000 00000rrr
#50 0r
    def CALL(self):
        self.reg[self.sp] -= 1 #push on stack
        #get address/val at address
        #set pc to address,
        #run op at sp in reg
        self.ram_write(self.pc + 2, self.reg[self.sp])


    def RET(self):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

    def CMP(self):
        reg_a =self.ram_read(self.pc+1) #set reg idnex
        reg_b=self.ram_read(self.pc+2)
        self.alu('CMP', reg_a, reg_b) #compare op at reg's
        self.pc+=3

##- JMP:
#Jump to the address stored in the given register.
#Set the PC to the address stored in the given register.
#01010100 00000rrr
#54 0r
    def JMP(self):
        reg =self.ram[self.pc+1] #get reg loc
        self.pc = self.reg[reg] #set pc to reg loc
##- JEQ:
#If equal flag is set (true), jump to address stored in the given register.
#01010101 00000rrr
#55 0r
    def JEQ(self):
        if self.E ==True:
            reg=self.ram[self.pc+1]
            self.pc =self.reg[reg]
        else:
            self.pc+=2
##- JNE:
#If E flag is clear (false, 0), jump to the address stored in the given register.
#01010110 00000rrr
#56 0r
    def JNE(self):
        if self.E ==False:
            reg=self.ram[self.pc+1]
            self.pc=self.reg[reg]
        else:
            self.pc+=2

##### SPRINT TASKS #######
#Add the CMP instruction and equal flag to your LS-8.
#Add the JMP instruction.
#Add the JEQ and JNE instructions.

 #ram_read:ACCEPT ADDRESS TO READ-- and RETURNS VALUE @ address
 #ram_write:ACCEPT VALUE TO WRITE AND ADDRESS TO WRITE TO
    def ram_read(self, position):
        return self.ram[position]

    def ram_write(self, position, value):
        self.ram[position] =value

    def load(self, f):
        """Load a program into memory."""
        filename = sys.argv[1]
        address = 0
        with open(filename) as f:
            for line in f:
                value = line.split("#")
                try:
                    v = int(value[0], 2)
                except ValueError:
                    continue
                self.ram[address] = v
                address += 1
    
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

##- CMP:
#instruction handled by the ALU.
#CMP registerA registerB
#Compare the values in two registers.
#If equal, set the Equal E flag to 1, otherwise set it to 0.
#If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
#If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
#10100111 00000aaa 00000bbb
#A7 0a 0b
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] * self.reg[reg_b]
        elif op =="CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E =1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.E=1
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.E=0
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
            ir= self.ram_read(self.pc)
            #need to  call fn
            self.branch_table[ir]()

