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
        self.__instructionMem = {}
    
    def loadInstructions(self,instructions):

        with open(instructions,"r") as instructions:
            instructions = instructions.read()
        
        instructions = [instructions[i:i+31] for i in range(0,len(instructions)//32)]
        startAddress = 0

        for instruction in instructions:
            self.instructionMem[format(startAddress,"032b")] = instruction
            startAddress+=4
        
        return format(startAddress,'032b')
    
    def getInstruction(self,address):

        try:
            return self.__instructionMem[address]
        except:
            return "No instruction exists at "+address
    
# includes the current program counter address and also the increment block is here itself.
class programCounter:

    def __init__(self):
        self.__currentAddress = 0
    
    def getCurrentAddress(self):
        currentAddress = format(self.__currentAddress,'032b')
        return currentAddress
    
    def setCurrentAddress(self,address):
        self.__currentAddress = int(address,2)
    
    def nextAddress(self):
        self.__currentAddress+=4
    
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
        return PC[:3]+sequence
    
    def getBranchAddress(offset,PC):
        offset = int(offset,2)
        PC = int(PC,2)
        return offset+PC
    
    

class registerFile:

    def __init__(self):
        self.__registers = {}

    def readData(self,registerAddress):
        try:
            return self.__registers[registerAddress]
        except:
            return -1

    def writeData(self,registerAddress,writeValue,controlUnit):
        if controlUnit.regWrite == "1":
            self.__registers[registerAddress] = writeValue
        else:
            return -1

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
    
    def setControlSignals(self,opCode,functionMode):

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

            return format(int(operand1,2)+int(operand2,2),'032b')
        
        elif AluSignal == "0110":
            return format(int(operand1,2)-int(operand2,2),'032b')
        
        elif AluSignal == "0000":
            return format(int(operand1,2) & int(operand2,2),'032b')
        
        elif AluSignal == "0001":
            return format(int(operand1,2) | int(operand2,2),'032b')
        
        elif AluSignal == "0111":

            if int(operand1,2) >= int(operand2,2):
                return format(0,'032b')
            else:
                return format(1,'032b')  


class dataMemory:

    def __init__(self):
        self.dataMem = {}

    def readMemory(self,address):
        pass

    def writeMemory(self,address,writeValue):
        pass
    



    

    
