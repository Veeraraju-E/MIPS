import csv

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
        "add":"000000",
        "sub":"000000",
        "and":"000000",
        "slt":"000000",
        "beq":"000100",
        "or":"000000",
        "lw":"100011",
        "sw":"101011",
        "j":"0010000"
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
        "beq":"B",
        "or":"R",
        "lw":"I",
        "sw":"I",
        "j":"J"
    }

    def compileInstruction(line):
        try:
            instructionType = handleTextSection.__instructionType[line[0]]

            if instructionType == "R":
                return handleTextSection.__handleRType(line[0],line[3],line[2].replace(',',''),line[1].replace(',',''))
            
            elif instructionType == "I":
                return -1
            
            elif instructionType == "B":
                return -1

            elif instructionType == "J":
                return -1
        except:
            return -1
    
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
            print("issue")
            return -1
        
        print(opCode+rs+rt+rd+"00000"+functionMode)
        return opCode+rs+rt+rd+"00000"+functionMode

        

    def __handleIType(mnemonic,rs,rt,immediate):
        pass

    def __handleBranchType(rs,rt,label):
        pass

    def __handleJumpType(label):
        pass
    

class handleDataSection:

    def compileVariable(line):
        pass

    def __assignMemory(label,value):
        pass


compiledCode = ""
dataSectionCompiled = ""
textSectionCompiled = ""

with open('./test.mips','r') as file:

    mipsCode = csv.reader(file,delimiter=' ')
    dataSectionEncountered = False

    for line in mipsCode:

        emptyStringCount = line.count('')
        for i in range(emptyStringCount):
            line.remove('')

        if len(line) == 0:
            continue

        elif len(line) == 1 and line[0] == '.data':
            dataSectionEncountered = True

        elif len(line) == 1 and line[0] == '.text':
            dataSectionEncountered = False

        elif len(line) == 1:
            continue

        elif dataSectionEncountered == True:
            handleDataSection.compileVariable(line)
        
        else:
            handleTextSection.compileInstruction(line)

            


        
