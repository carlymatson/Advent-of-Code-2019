opfile = open("inputDay5.text", 'r')
intcode0 = opfile.readline().split(',')
intcodeDefault = [int(i) for i in intcode0]
#opList2 = [1,5,6,7,2,3,4,10,99, 0,0,0]

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

def run(_intCode):
    intcode = list(_intCode)
    #intcode[1] = _noun
    #intcode[2] = _verb
    pointer = 0
    opCode = intcode[pointer]%100
    modes = [(intcode[pointer]%1000)/100, (intcode[pointer]%10000)/1000]
    relBase = 0
    numParams = 1
    while opCode != 99:
        #print("Intcode: " + str(intcode))
        if opCode == 1:
            numParams = 3
            num1 = get(intcode, pointer+1,modes[0])
            num2 = get(intcode, pointer+2,modes[1])
            store(intcode, pointer+3, num1+num2)
            #do stuff
        elif opCode == 2:
            numParams = 3
            num1 = get(intcode, pointer+1,modes[0])
            num2 = get(intcode, pointer+2,modes[1])
            store(intcode, pointer+3, num1*num2)
            #stuff
        elif opCode == 3:
            numParams = 1
            print("Input number:")
            input1 = input()
            store(intcode, pointer+1, input1)
        elif opCode == 4:
            numParams = 1
            print("Output:" + str(get(intcode, pointer+1, modes[0])))
        elif opCode == 5:
            numParams = 2
            if get(intcode, pointer+1, modes[0]) != 0:
                pointer = get(intcode, pointer+2, modes[1])
                numParams = -1 # Don't advance the pointer again.
        elif opCode == 6:
            numParams = 2
            if get(intcode, pointer+1, modes[0]) == 0:
                pointer = get(intcode, pointer+2, modes[1])
                numParams = -1 # Don't advance the pointer again.
        elif opCode == 7:
            numParams = 3
            lessThan = get(intcode, pointer+1, modes[0]) < get(intcode, pointer+2, modes[1])
            if lessThan:
                store(intcode, pointer+3, 1)
            else:
                store(intcode, pointer+3, 0)
        elif opCode == 8:
            numParams = 3
            equal = get(intcode, pointer+1, modes[0]) == get(intcode, pointer+2, modes[1])
            if equal:
                store(intcode, pointer+3, 1)
            else:
                store(intcode, pointer+3, 0)
        elif opCode == 9:
            numParams = 1
            relBase += get(intcode, pointer+1, modes[0])
        else:
            #print("Something went wrong.")
            print("Operator at position" + str(pointer) +" is equal to " + str(intcode[pointer]))
        pointer += (numParams +1)
        opCode = intcode[pointer]%100
        modes = [(intcode[pointer]%1000)/100, (intcode[pointer]%10000)/1000]
    return intcode[0]

codeEqual8 = [3,9,8,9,10,9,4,9,99,-1,8] #Returns 1 if input is equal to 8.
codeLess8 = [3,9,7,9,10,9,4,9,99,-1,8] #Returns 1 if input is less than 8.
codeJumpTest = [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9]
codeLargeTest = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

run(codeLess8)
#for noun in range(100):
#    for verb in range(100):
#        if computer(noun, verb) == 19690720:
#            print("Noun: " + str(noun) + ", Verb: " + str(verb))
#            exit
