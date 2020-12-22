opfile = open("inputDay2.text", 'r')
intcode0 = opfile.readline().split(',')
intcodeStart = [int(i) for i in intcode0]
#opList2 = [1,5,6,7,2,3,4,10,99, 0,0,0]

def computer(_noun, _verb):
    intcode = list(intcodeStart)
    intcode[1] = _noun
    intcode[2] = _verb
    pointer = 0
    operator = intcode[pointer]
    while (operator ==1) or (operator ==2):
        #print("In while loop. posOp = " + str(posOp))
        num1 = intcode[intcode[pointer + 1]]
        num2 = intcode[intcode[pointer + 2]]
        if operator == 1:
            result = num1 + num2
        else:
            result = num1*num2
            #print("Putting " + str(num1) + "," + str(num2) + "in position " + str(opList[posOp + 3]))
        intcode[intcode[pointer + 3]] = result
        pointer += 4
        operator = intcode[pointer]
    if operator != 99:
        print("Something went wrong.")
        print("Operator at position" + str(pointer) +" is equal to " + str(intcode[pointer]))
    return intcode[0]

for noun in range(100):
    for verb in range(100):
        if computer(noun, verb) == 19690720:
            print("Noun: " + str(noun) + ", Verb: " + str(verb))
            exit
