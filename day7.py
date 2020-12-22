opfile = open("inputDay7.text", 'r')
intcode0 = opfile.readline().split(',')
intcodeDefault = [int(i) for i in intcode0]
#intcodeDefault = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#intcodeDefault = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

def get(_intCode, _pos, _mode):
    val = 0
    if _mode == 0: # Position mode
        val = _intCode[_intCode[_pos]]
    elif _mode == 1: # Immediate mode
        val = _intCode[_pos]
    elif _mode == 2: # Relative mode
        val = _intCode[[_pos]+relBase]
    return val

def store(_intCode, _pos, _value, _mode=0):
    if _mode == 0:
        _intCode[_intCode[_pos]] = _value
    elif _mode == 2:
        _intCode[_intCode[_pos]+relBase] = _value
    else:
        print("Something wrong in Store")
        return False
    return True

def run(intcode, inputs = [], pointer = 0):
    #intcode = list(_intCode) If I want to alter the actual "program" I shouldn't make a copy.
    output = None
    opCode = intcode[pointer]%100
    modes = [(intcode[pointer]%1000)/100, (intcode[pointer]%10000)/1000]
    relBase = 0
    numParams = 1
    finished = False
    while opCode < len(intcode):
        if opCode == 1: # Add
            numParams = 3
            num1 = get(intcode, pointer+1,modes[0])
            num2 = get(intcode, pointer+2,modes[1])
            #print(str(intcode[pointer: pointer+numParams+1]) + ": " + str(num1) + ", " + str(num2))
            store(intcode, pointer+3, num1+num2)
        elif opCode == 2: # Multiply
            numParams = 3
            num1 = get(intcode, pointer+1,modes[0])
            num2 = get(intcode, pointer+2,modes[1])
            #print(str(intcode[pointer: pointer+numParams+1]) + ": " + str(num1) + ", " + str(num2))
            store(intcode, pointer+3, num1*num2)
        elif opCode == 3: # Take input
            numParams = 1
            if len(inputs) > 0:
                input1 = inputs[0]
                inputs = inputs[1:]
            else:
                #print("Suspending amp " + str(amp) + ". Pointer = " + str(pointer) + ", output = " + str(output))
                break
            #print("Input number:")
            #input1 = input()
            store(intcode, pointer+1, input1)
        elif opCode == 4:  # Print output
            numParams = 1
            output = get(intcode, pointer+1, modes[0])
            #print("Output:" + str(get(intcode, pointer+1, modes[0])))
        elif opCode == 5: # Jump if True
            numParams = 2
            if get(intcode, pointer+1, modes[0]) != 0:
                pointer = get(intcode, pointer+2, modes[1])
                numParams = -1 # Don't advance the pointer again.
        elif opCode == 6: # Jump if False
            numParams = 2
            if get(intcode, pointer+1, modes[0]) == 0:
                pointer = get(intcode, pointer+2, modes[1])
                numParams = -1 # Don't advance the pointer again.
        elif opCode == 7: # Write True if less than
            numParams = 3
            lessThan = get(intcode, pointer+1, modes[0]) < get(intcode, pointer+2, modes[1])
            if lessThan:
                store(intcode, pointer+3, 1)
            else:
                store(intcode, pointer+3, 0)
        elif opCode == 8: # Write True if equal
            numParams = 3
            equal = get(intcode, pointer+1, modes[0]) == get(intcode, pointer+2, modes[1])
            if equal:
                store(intcode, pointer+3, 1)
            else:
                store(intcode, pointer+3, 0)
        elif opCode == 9: # Adjust relative base
            numParams = 1
            relBase += get(intcode, pointer+1, modes[0])
        elif opCode == 99:
            finished = True
            break
        else:
            print("Something went wrong.")
            print("Operator at position" + str(pointer) +" is equal to " + str(intcode[pointer]))
        pointer += (numParams +1)
        opCode = intcode[pointer]%100
        modes = [(intcode[pointer]%1000)/100, (intcode[pointer]%10000)/1000]
    #print(str(output)+ ", " + str(finished))
    #print("----")
    return [output, finished, pointer]

def getPermutations(_list):
    if len(_list)==0 or len(_list)==1:
        return [list(_list)] # A list containing a single copy of the original list.
    permList = []
    for i in range(len(_list)):
        subList = _list[:i] + _list[i+1:]
        #print("Sublist for item i: " + str(subList))
        permList += [[_list[i]] + subPerm for subPerm in getPermutations(subList)]
    return(permList)


maxOutput = 0
for phases in getPermutations([5,6,7,8,9]):
#for i in range(1):
    #phases = [5,6,7,8,9]
    #print("Phase: " + str(phases))
    ampCodes = [list(intcodeDefault) for i in range(5)]
    pointers = [0]*5
    inputs = []
    doneRunning = [False]*5
    outputList = [0, False]
    firstLoop = True
    amp = 0
    while doneRunning[amp%5] != True:
        #if amp%5==4:
            #print("Amp: " + str(amp))
        if outputList[0] == None:
            print("Output is none")
            break
        if firstLoop:
            inputs = [phases[amp], outputList[0]]
        else:
            inputs = [outputList[0]]
        outputList = run(ampCodes[amp%5], inputs, pointers[amp%5])
        pointers[amp%5] = outputList[2]
        doneRunning[amp%5] = outputList[1]
        lastOutput = outputList[0]
        #print("Output on amp=" + str(amp) + ": " + str(outputList[0]))
        if amp == 4:
            firstLoop = False
        amp += 1
    print("Phase last output: " + str(lastOutput))
    if lastOutput > maxOutput:
        maxOutput = lastOutput
print("Maximum output:" + str(maxOutput))
