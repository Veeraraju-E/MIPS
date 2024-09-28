import csv

'''
4. ALU
6. Control Unit
7. ALU Control
'''

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
        pass

    def readData(self,registerAddress):
        pass

    def writeData(self,registerAddress,writeValue):
        pass


class dataMemory:

    def __init__(self):
        self.dataMem = {}

    def readMemory(self,address):
        pass

    def writeMemory(self,address,writeValue):
        pass
    



    

    
