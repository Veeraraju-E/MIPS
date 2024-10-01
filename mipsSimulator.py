import functionalUnits as FU
from functionalUnits import ALU
from functionalUnits import otherUnits

import csv

class simulator:

    def __init__(self):
        
        self.instructionMemory = FU.InstructionMemory()
        self.dataMemory = FU.dataMemory()
        self.registerFile = FU.registerFile()
        self.programCounter = FU.programCounter()
        self.aluControlUnit = FU.AluControl()
        self.controlUnit = FU.controlUnit()
        
    
    def __allocateMemoryData(self,dataFile):

        with open (dataFile,"r") as dataFile:

            dataFile = csv.reader(dataFile,delimiter=" ")

            for word in dataFile:
                self.dataMemory.writeMemory(word[0],word[1],True,self.controlUnit)
        
        print(self.dataMemory.dataMem)
            
    
    def __allocateMemoryInstruction(self,assembledCode):

        instructions = ""

        with open(assembledCode,"r") as instructionFile:

            instructions = instructionFile.read()
            PC = 0

        for startIndex in range(0,len(instructions),32):

            instruction = instructions[startIndex:startIndex+32]

            self.instructionMemory.loadInstruction(format(PC,'032b'),instruction)
            PC+=4
        
        return len(instruction)//32
        
        print(self.instructionMemory.instructionMem)
    
    def simulate(self):

        self.__allocateMemoryData("./data_memory.txt")
        noOfInstructions = self.__allocateMemoryInstruction("assembled_code.mips")

        for i in range(0,noOfInstructions):

            instruction = self.instructionMemory.getInstruction(self.programCounter.getCurrentAddress())
            self.programCounter.nextAddress()

            self.controlUnit.setControlSignals(instruction[:6])

            signExtended = otherUnits.signExtend(instruction[16:])
            branchAddress = otherUnits.getBranchAddress(signExtended,self.programCounter.getCurrentAddress())

            leftShiftBy2 = otherUnits.leftShiftForJump(instruction[6:])
            jumpAddress = otherUnits.concatPCAddress(leftShiftBy2,self.programCounter.getCurrentAddress())

            readData1,readData2 = self.registerFile.readData(instruction[6:11],instruction[11:16])
            writeRegister = instruction[11:16] if self.controlUnit.regDst == "0" else instruction[16:21]
            readData2 = readData2 if self.controlUnit.AluSrc == "0" else signExtended

            self.aluControlUnit.setSignal(self.controlUnit.AluOp,instruction[26:])
            result,zero = ALU.performOperation(self.aluControlUnit.signal,readData1,readData2)

            readData = self.dataMemory.readMemory(result,self.controlUnit)

            writeData = result if self.controlUnit.memToReg == "0" else readData
            self.registerFile.writeData(writeRegister,writeData,self.controlUnit)
            self.programCounter.setCurrentAddress(branchAddress,jumpAddress,self.controlUnit,zero)





            
            
            
            





