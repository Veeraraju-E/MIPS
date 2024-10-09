import csv

"""
This file contains class definitions of various Functional Units of the MIPS Procesor
They are:
1. Instruction Memory
2. Data Memory
3. Register File
4. Alu Control Unit
5. ALU (abstract class)
6. Control Unit
7. Program Counter
8. other Units
"""

class InstructionMemory:

    def __init__(self):
        self.instructionMem = {}
    
    def loadInstruction(self,address,instruction):

        self.instructionMem[address] = instruction
    
    def getInstruction(self,address):
        #print(address)
        try:
            return self.instructionMem[address]
        except:
            return "No instruction exists at "+address
    
# includes the current program counter address and also the increment block is here itself.
class programCounter:

    def __init__(self):
        self.__currentAddress = "0"*32
    
    def getCurrentAddress(self):
        return self.__currentAddress
    
    def setCurrentAddress(self,branchAddress,jumpAddress,controlUnit,zero):
        #print(branchAddress)
        self.__currentAddress = self.__currentAddress if (int(controlUnit.branch) & int(zero) == 0) else branchAddress
        self.__currentAddress = self.__currentAddress if controlUnit.jump == "0" else jumpAddress 
    
    def nextAddress(self):
        self.__currentAddress=format(int(self.__currentAddress,2)+4,'032b')
    
# this includes sign extension unit, left shift units, jump address calculator unit
class otherUnits:

    def signExtend(immediateField):
        if len(immediateField) != 16:
            return "Error"
        immediateField=immediateField[0]*16+immediateField

        return immediateField
    
    def leftShiftBy2(sequence):
        return sequence[2:]+"00"
    
    def leftShiftForJump(sequence):
        return sequence+"00"
    
    def concatPCAddress(sequence,PC):
        return PC[:4]+sequence
    
    def getBranchAddress(offset,PC):
        
        offset = int(offset,2)
        PC = int(PC,2)
        return format(offset+PC,'032b')
    
class registerFile:

    def __init__(self):
        self.__registers = {}


        self. __registerAddressMap = {
        "$zero":"00000",
        "$at":"00001",
        "$a0":"00010",
        "$a1":"00011",
        "$v0":"00100",
        "$v1":"00101",
        "$v2":"00110",
        "$v3":"00111",
        "$t0":"01000",
        "$t1":"01001",
        "$t2":"01010",
        "$t3":"01011",
        "$t4":"01100",
        "$t5":"01101",
        "$t6":"01110",
        "$t7":"01111",
        "$s0":"10000",
        "$s1":"10001",
        "$s2":"10010",
        "$s3":"10011",
        "$s4":"10100",
        "$s5":"10101",
        "$s6":"10110",
        "$s7":"10111",
        "$t8":"11000",
        "$t9":"11001",
        "$k0":"11010",
        "$k1":"11011",
        "$gp":"11100",
        "$sp":"11101",
        "$fp":"11110",
        "$ra":"11111"
    }
        for i in range(32):
            self.__registers[format(i,'05b')] = format(0,'032b')
        # self.__registers[format(8,'05b')] = format(10,'032b')
        # self.__registers[format(9,'05b')] = format(20,'032b')

    def printAllRegisters(self):

        for register in self.__registerAddressMap.keys():
            valueInBinary = self.__registers[self.__registerAddressMap[register]]
            valueInInt = int(valueInBinary,2)
            print(register," : ",valueInBinary," or in decimal it is ",valueInInt)
        

    def readData(self,registerAddress1,registerAddress2):
        
        try:
            return self.__registers[registerAddress1],self.__registers[registerAddress2]
        except:
            return -1,-1

    def writeData(self,registerAddress,writeValue,controlUnit,isStaticBinding):
        if isStaticBinding == True:
            self.__registers[registerAddress] = writeValue
        elif controlUnit.regWrite == "1":
            self.__registers[registerAddress] = writeValue
        else:
            return ["-1","-1"]

class controlUnit:

    def __init__(self):
        self.memWrite = "0"
        self.memRead = "0"
        self.memToReg = "0"

        self.regWrite = "0"
        self.regDst = "0"

        self.AluOp = "00"
        self.AluSrc = "0"
        
        self.jump = "0"
        self.branch = "0"
    
    def setControlSignals(self,opCode):

        # R type
        if opCode == "000000":

            self.regDst = "1"
            self.regWrite = "1"
            self.AluSrc = "0"
            self.memWrite = "0"
            self.memRead = "0"
            self.memToReg = "0"
            self.branch = "0"
            self.jump = "0"
            self.AluOp = "10"
        
        # beq
        elif opCode == "000100":

            self.regDst = "0"
            self.regWrite = "0"
            self.AluSrc = "0"
            self.memWrite = "0"
            self.memRead = "0"
            self.memToReg = "0"
            self.branch = "1"
            self.jump = "0"
            self.AluOp = "01"
        
        # j
        elif opCode == "000010":

            self.regDst = "0"
            self.regWrite = "0"
            self.AluSrc = "0"
            self.memWrite = "0"
            self.memRead = "0"
            self.memToReg = "0"
            self.branch = "0"
            self.jump = "1"
            self.AluOp = "11"
        
        # lw
        elif opCode == "100011":

            self.regDst = "0"
            self.regWrite = "1"
            self.AluSrc = "1"
            self.memWrite = "0"
            self.memRead = "1"
            self.memToReg = "1"
            self.branch = "0"
            self.jump = "0"
            self.AluOp = "00"
        
        # sw
        elif opCode == "101011":

            self.regDst = "0"
            self.regWrite = "0"
            self.AluSrc = "1"
            self.memWrite = "1"
            self.memRead = "0"
            self.memToReg = "0"
            self.branch = "0"
            self.jump = "0"
            self.AluOp = "00"
        
        elif opCode == "001000":

            self.regDst = "0"
            self.regWrite = "1"
            self.AluSrc = "1"
            self.memWrite = "0"
            self.memRead = "0"
            self.memToReg = "0"
            self.branch = "0"
            self.jump = "0"
            self.AluOp = "00"


class AluControl:

    def __init__(self):
        self.signal = "0000"
    
    def setSignal(self,AluOp,functionMode):
        # lw,sw,addi
        if AluOp == "00":
            self.signal = "0010"
        
        # beq
        elif AluOp == "01":
            self.signal = "0110"
        
        elif AluOp == "10":
            # add
            if functionMode == "100000":
                self.signal = "0010"
            # sub
            elif functionMode == "100010":
                self.signal = "0110"
            # and
            elif functionMode == "100100":
                self.signal = "0000"
            #or
            elif functionMode == "100101":
                self.signal = "0001"
            # slt
            elif functionMode == "101010":
                self.signal = "0111"
        else:
            self.signal = "0000"
        

class ALU:

    def performOperation(AluSignal,operand1,operand2):

        if AluSignal == "0010":
            return format(int(operand1,2) + int(operand2,2),'032b'),"1" if int(operand1,2)-int(operand2,2) == 0 else "0"
        
        elif AluSignal == "0110":
            return format(int(operand1,2) - int(operand2,2),'032b'),"1" if int(operand1,2)-int(operand2,2) == 0 else "0"
        
        elif AluSignal == "0000":
            return format(int(operand1,2) & int(operand2,2),'032b'),"1" if int(operand1,2)-int(operand2,2) == 0 else "0"
        
        elif AluSignal == "0001":
            return format(int(operand1,2) | int(operand2,2),'032b'),"1" if int(operand1,2)-int(operand2,2) == 0 else "0"
        
        elif AluSignal == "0111":
            return format(1,'032b') if int(operand1,2)-int(operand2,2) < 0 else format(0,'032b'),"1" if int(operand1,2)-int(operand2,2) == 0 else "0"
        else:
            print("Hello")

class dataMemory:

    def __init__(self):
        self.dataMem = {}

    def readMemory(self,address,controlUnit):
        if controlUnit.memRead == "1":

            try:
                return self.dataMem[address]
            except:
                return -1
        
        else:
            return -1

    def writeMemory(self,address,writeValue,isStaticBinding,controlUnit):

        print(address,writeValue)
        
        if isStaticBinding:
            self.dataMem[address] = writeValue
        
        elif controlUnit.memWrite == "1":
            self.dataMem[address] = writeValue
        
        else:
            return -1
    



    

    
