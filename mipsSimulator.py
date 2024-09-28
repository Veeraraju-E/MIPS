import csv
from numpy import random
import os

labelPool = {}
encodedCode = ""
dataSectionencoded = ""
textSectionencoded = ""

class handleTextSection:

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
            print(line)
            instructionType = handleTextSection.__instructionType[line[0]]
            if instructionType == "R":
                return handleTextSection.__handleRType(line[0],line[3],line[2].replace(',',''),line[1].replace(',',''))
            elif instructionType == "I":
                # lw and sw only , line = ['lw', '$t2,', 'num'] or line = ['lw', '$t2,', '100($t0)']
                addr_type = 0
                if '$' in line[2]:  # stronger condition?
                    addr_type = 1
                return handleTextSection.__handleIType(line[0], line[2], line[1].replace(',',''), addr_type)
            elif instructionType == "B":
                return handleTextSection.__handleBranchType(line[1].replace(',',''), line[2].replace(',',''), line[3])
            elif instructionType == "J":
                return handleTextSection.__handleJumpType(line[1])
        except:
            return "Invalid Instruction"
    
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
            return "One of the registers is invalid"
        
        return opCode+rs+rt+rd+"00000"+functionMode

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
            address = labelPool.get(rs, None) # 16-bit address, default None
            label = rs
            rs = "00000"
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
        address = labelPool.get(label, None)        # depends on how data section is to handled

        return opCode + rs + rt + address

    def __handleJumpType(label):
        opCode = handleTextSection.__instructionOpCode["j"]
        address = labelPool.get(label, None)        # depends on how data section is to handled
        
        return opCode + address
    

class handleDataSection:

    def encodeVariable(line):

        if line[1] != '.word':
            os.remove('./data_memory.txt')
            return "Invalid Data Type "+line[1]
        
        label = line[0].replace(':','')
        value = int(line[2])

        if label in labelPool.keys():
            os.remove('./data_memory.txt')
            return "Can not redefine " + label
        
        message = handleDataSection.__assignMemory(label,value)

        return message
        
    def __assignMemory(label,value):
        try:

            value = format(value,'032b')
            address = random.randint(0,2**30)
            address = format(address,'032b')

            with open('data_memory.txt','a') as file:
                file.write(address+" "+value+'\n')
            
            labelPool[label] = value
            return 1
        
        except:
            os.remove('./data_memory.txt')
            return "Couldn't allocate enough space in the memory"

with open('./test.mips','r') as file:

    mipsCode = csv.reader(file,delimiter=' ')
    dataSectionEncountered = False

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

        elif len(line) == 1 and line[0].count(':') == 0:
            print("Error at line " + str(linenumber+1))

        elif dataSectionEncountered == True:
            message=handleDataSection.encodeVariable(line)

            if message != 1:
                 print("Error at line " + str(linenumber+1) + " " + message)
        
        else:
            encodedInstruction = handleTextSection.encodeInstruction(line)
            if len(encodedInstruction) != 32:
                print("Error at line " + str(linenumber+1) + " " + encodedInstruction)
            else:
                textSectionencoded += encodedInstruction
