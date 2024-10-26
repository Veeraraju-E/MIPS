import csv
from numpy import random
import os

class handleTextSection:
    """
    This section handles the text section
    """

    __registerAddressMap = {
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

    __instructionOpCode = {
        "addi":"001000",
        "add":"000000",
        "sub":"000000",
        "and":"000000",
        "slt":"000000",
        "beq":"000100",
        "or":"000000",
        "lw":"100011",
        "sw":"101011",
        "j":"000010"
    }

    __instructionFunctionMode = {
        "and":"100100",
        "add":"100000",
        "sub":"100010",
        "slt":"101010",
        "or":"100101"
    }

    __instructionType = {
        "addi":"AI",
        "add":"R",
        "sub":"R",
        "and":"R",
        "slt":"R",
        "or":"R",
        "beq":"B",
        "lw":"I",
        "sw":"I",
        "j":"J"
    }

    def encodeInstruction(line):
        try:
            #print(line)
            instructionType = handleTextSection.__instructionType[line[0]]
            if instructionType == "R":
                return handleTextSection.__handleRType(line[0],line[2].replace(',',''),line[3].replace(',',''),line[1].replace(',',''))
            elif instructionType == "I":
                addr_type = 0
                if '$' in line[2]:
                    addr_type = 1
                return handleTextSection.__handleIType(line[0], line[2], line[1].replace(',',''), addr_type)
            elif instructionType == "B":
                return handleTextSection.__handleBranchType(line[1].replace(',',''), line[2].replace(',',''), line[3])
            elif instructionType == "J":
                return handleTextSection.__handleJumpType(line[1])
            elif instructionType == "AI":
                #print("Hello")
                return handleTextSection.__handleAddi(line[0],line[2].replace(',',''),line[1].replace(',',''),line[3])
        except:
            return "Invalid Instruction",True
        
    def __handleAddi(mnemonic,rs,rt,constant):

        opCode = handleTextSection.__instructionOpCode[mnemonic]
        if int(constant) < 0:
            constant = format(int(constant) & 0xFFFF, '016b')
        else:
            constant = format(int(constant),'016b')
        rs,rt = handleTextSection.__encodeRegister(rs),handleTextSection.__encodeRegister(rt)

        return opCode+rs+rt+constant,True
    
    def __encodeRegister(register):
        try:
            return handleTextSection.__registerAddressMap[register]
        except:
            return -1
    
    def __handleRType(mnemonic,rs,rt,rd):

        opCode = handleTextSection.__instructionOpCode[mnemonic]
        functionMode = handleTextSection.__instructionFunctionMode[mnemonic]
        rs = handleTextSection.__encodeRegister(rs)
        rt = handleTextSection.__encodeRegister(rt)
        rd = handleTextSection.__encodeRegister(rd)

        if rs == -1 or rt == -1 or rd == -1:
            return "One of the registers is invalid",True
        
        return opCode+rs+rt+rd+"00000"+functionMode,True

    def __handleIType(mnemonic,rs,rt, addr_type):
        """
        :param mnemonic: lw/sw
        :param rs: $t0 etc
        :param rt: $t0 etc
        :param addr_type: a flag to check which type of loading or storing
            (based on labels in data section or on register values + offets)
            addr_type = 1 => lw $t0, num; rs = num, rt = $t0
            addr_type = 0 => lw $t0, 100($t2); rs = 100($t2), rt = $t0
        :return 32-bit instruction
        """
        opCode = handleTextSection.__instructionOpCode[mnemonic]
        rt = handleTextSection.__encodeRegister(rt)

        address = ""
        label = ""
        if not addr_type:
            if not labelPoolData.get(rs):
                return -1   # label DNE
            
            label = rs
            address,value = labelPoolData.get(label)
            rs = "00001"

            with open("data_memory.txt","a") as file:
                file.write(address+" "+value+" "+PC+"\n")
            
            return opCode+ rs + rt + format(0,'016b'),True

        else:
            rs = rs.replace('(',',').replace(')','')
            rs = rs.split(',')
            # print(rs)
            address = bin(int(rs[0])).replace('0b','')
            while len(address) < 16:
                address = '0' + address
            rs = rs[1]
            rs = handleTextSection.__encodeRegister(rs)

        if not address:
            return f"Label not found. Please declare {label}."
        
        elif len(address) > 16:
            return "Address too big."
        
        if rs == -1 or rt == -1:
            return "One of the registers is invalid"
        
        return opCode + rs + rt + address

    def __handleBranchType(rs,rt,label):

        opCode = handleTextSection.__instructionOpCode["beq"]
        rs = handleTextSection.__encodeRegister(rs)
        rt = handleTextSection.__encodeRegister(rt)

        if (labelPoolData.get(label)):
            return -1
        
        if labelPoolText.get(label):
            
            offset = int(labelPoolText[label],2) - int(PC,2)
            offset = format(offset & 0xFFFFFFFF, '032b')
            return opCode+rs+rt+offset,False

        unhandledBranchLabels[label] = PC
        return opCode+rs+rt+label,False
        
    def __handleJumpType(label):
        opCode = handleTextSection.__instructionOpCode["j"]
        if (labelPoolData.get(label)):
            return -1   # label DNE
        
        if labelPoolText.get(label):

            address = labelPoolText[label]
            removePCConcat = address[4:]
            jumpAddress = removePCConcat[:26]
            return opCode+jumpAddress,False
        
        unhandledJumpLabels[label] = PC
        return opCode+label,False
    
    
    
    def handleLabel(label):

        if label in labelPoolText.keys():
            return "Can not redefine "+label
        
        labelPoolText[label] = PC
        return 1
    
class handleDataSection:

    def encodeVariable(line):

        if line[1] != '.word':
            os.remove('./data_memory.txt')
            return "Invalid Data Type "+line[1]
        
        label = line[0].replace(':','')
        value = int(line[2])

        if label in labelPoolData.keys():
            os.remove('./data_memory.txt')
            return "Can not redefine " + label
        
        message = handleDataSection.__assignMemory(label,value)

        return message
        
    def __assignMemory(label,value):
        try:

            value = format(value,'032b')
            address = random.randint(0,2**31-1)
            address = format(address,'032b')
            
            labelPoolData[label] = [address,value]
            return 1
        
        except:
            os.remove('./data_memory.txt')
            return "Couldn't allocate enough space in the memory"

def assemble(filepath):
    global PC
    global machineCode
    with open(filepath,'r') as file:

        mipsCode = csv.reader(file,delimiter=' ')
        dataSectionEncountered = False
        errorEncountered = False

        try:
            if os.path.exists('./data_memory.txt'):
                os.remove('./data_memory.txt')
        except:
            print("System Error. Retry Again")

        for linenumber,line in enumerate(mipsCode):

            emptyStringCount = line.count('')
            for i in range(emptyStringCount):
                line.remove('')

            if len(line) == 0:
                continue

            elif len(line) == 1 and line[0] == '.data':
                dataSectionEncountered = True

            elif len(line) == 1 and line[0] == '.text':
                dataSectionEncountered = False

            elif len(line) == 1 and line[0].endswith(':') == False:
                errorEncountered = True
                print("Error at line " + str(linenumber+1))
                break
            
            elif len(line) == 1 and dataSectionEncountered == False and line[0].endswith(':') == True:
                message = handleTextSection.handleLabel(line[0].replace(":",''))

                if message != 1:
                    errorEncountered = True
                    print("Error at line "+ str(linenumber+1)+ " " + message)
                    break

            elif dataSectionEncountered == True:
                message = handleDataSection.encodeVariable(line)

                if message != 1:
                    errorEncountered = True
                    print("Error at line " + str(linenumber+1) + " " + message)
                    break
                
            else:
                encodedInstruction,notBranchOrJump = handleTextSection.encodeInstruction(line)
                PC = format(int(PC,2)+4,'032b')
                
                if len(encodedInstruction) != 32 and notBranchOrJump:
                    errorEncountered = True
                    print("Error at line " + str(linenumber+1) + " " + encodedInstruction)
                    break
                else:
                    machineCode+= encodedInstruction
        
        if errorEncountered == False:

            for key in unhandledBranchLabels.keys():

                try:

                    address = labelPoolText[key]
                    PCWhenCalled = unhandledBranchLabels[key]
                    
                    offset = format(int(address,2)-(int(PCWhenCalled,2)+4),'032b')[16:]

                    machineCode = machineCode.replace(key,offset)
                except:
                    errorEncountered = True
                    print("No label named ",key)
                    break
            
        if errorEncountered == False:

            for key in unhandledJumpLabels.keys():
                try:
                    address = labelPoolText[key]
                    removePCConcat = address[4:]
                    jumpAddress = removePCConcat[:26]

                    machineCode = machineCode.replace(key,jumpAddress)
                except:
                    errorEncountered = True
                    print("No label named ",key)
                    break
            
            if errorEncountered == False:

                with open("assembled_code.mips","w") as file:

                    file.write(machineCode)
                    print("The code is assembled at the file named assembled_code.mips.\nA data_memory.txt file is created to handle the .data section. Do Not Delete it!\n")

if __name__ == "__main__":

    PC = "0"*32
    labelPoolData = {}
    labelPoolText = {}
    unhandledBranchLabels = {}
    unhandledJumpLabels = {}
    machineCode = ""
    assemble("./test_code_5_mips_sim.asm")