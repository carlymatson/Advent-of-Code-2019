

class Computer:


    def __init__(self, _intcode, _pointer = 0):
        self.intcode = _intcode
        self.pointer = _pointer
        self.length = len(_intcode)
        self.relBase = 0
        self.outputs = list()
        self.finished = False

    def pad(self, _newLength):
        self.intcode = self.intcode + [0]*(_newLength + 1 - self.length)
        self.length = len(self.intcode)

    def get(self, _par, _mode):
        if _par > self.length-1:
            self.pad(_par + 1)
        val = 0
        if _mode == 0: # Position mode
            pos = self.get(_par, 1)
            val = self.get(pos, 1)
        elif _mode == 1: # Immediate mode
            val = self.intcode[_par]
        elif _mode == 2: # Relative mode
            pos = self.get(_par, 1) + self.relBase
            val = self.get(pos, 1)
        return val

    def store(self, _par, _value, _mode): #Still need to catch negative vals.
        pos = _par
        if _mode == 0:
            pos = self.get(_par, 1)
        elif _mode == 2:
            pos = self.get(_par, 1) + self.relBase
        else:
            print("Something wrong in Store")
            return False
        if pos > self.length-1:
            self.pad(pos + 1)
        self.intcode[pos] = _value
        #print("Storing " + str(_value) + " at position " + str(pos))
        return True

    def run(self, inputs = []):
        output = None
        self.outputs = [] # This shouldn't apply for every robot.
        pointer = self.pointer
        opCode = self.intcode[pointer]%100
        modes = [(self.intcode[pointer]%1000)/100,
                 (self.intcode[pointer]%10000)/1000,
                 (self.intcode[pointer]%100000)/10000]
        numParams = 1
        while (pointer < self.length) and (self.finished == False):

            result = None

            if opCode == 1: # Add
                numParams = 3
                num1 = self.get(pointer+1, modes[0])
                num2 = self.get(pointer+2, modes[1])
                result = num1 + num2
                self.store(pointer+3, result, modes[2])

            elif opCode == 2: # Multiply
                numParams = 3
                num1 = self.get(pointer+1, modes[0])
                num2 = self.get(pointer+2, modes[1])
                result = num1 * num2
                self.store(pointer+3, result, modes[2])

            elif opCode == 3: # Take input
                numParams = 1
                if len(inputs) > 0:
                    input1 = inputs[0]
                    inputs = inputs[1:]
                else:
                    #drawScreen(self.outputs)
                    print("Suspending program")
                    self.pointer = pointer
                    return(self.outputs)
                result = input1
                self.store(pointer+1, input1, modes[0])

            elif opCode == 4:  # Print output
                numParams = 1
                output = self.get(pointer+1, modes[0])
                result = output
                self.outputs.append(output)
                #print("Output: " + str(output))

            elif opCode == 5: # Jump if Nonzero
                numParams = 2
                if self.get(pointer+1, modes[0]) != 0:
                    pointer = self.get(pointer+2, modes[1])
                    numParams = -1
                    result = pointer
                else:
                    result = -1

            elif opCode == 6: # Jump if Zero
                numParams = 2
                if self.get(pointer+1, modes[0]) == 0:
                    pointer = self.get(pointer+2, modes[1])
                    numParams = -1
                    result = pointer
                else:
                    result = -1

            elif opCode == 7: # Write 1 if less than
                numParams = 3
                lessThan = (self.get(pointer+1, modes[0])
                            < self.get(pointer+2, modes[1]))
                if lessThan:
                    result = 1
                else:
                    result = 0
                self.store(pointer+3, result, modes[2])

            elif opCode == 8: # Write 1 if equal
                numParams = 3
                equal = (self.get(pointer+1, modes[0])
                         == self.get(pointer+2, modes[1]))
                if equal:
                    result = 1
                else:
                    result = 0
                self.store(pointer+3, result, modes[2])

            elif opCode == 9: # Adjust relative base
                numParams = 1
                change = self.get(pointer+1, modes[0])
                result = self.relBase + change
                self.relBase += change
            elif opCode == 99:
                self.finished = True
                break
            else:
                print("Something went wrong.")
                print("Operator at position" + str(pointer)
                      +" is equal to " + str(self.intcode[pointer]))
            #print("Code: " + str(self.intcode[pointer : pointer + numParams+1])
                   #+ " , opcode = " + str(opCode)
                   #+ " numpar = " + str(numParams)
            #       + ",\n\t result = " + str(result)
            #       + ", point = " + str(pointer))
            pointer += (numParams +1)
            opCode = self.intcode[pointer]%100
            modes = [(self.intcode[pointer]%1000)/100,
                     (self.intcode[pointer]%10000)/1000,
                     (self.intcode[pointer]%100000)/10000]
            self.pointer = pointer
        return self.outputs



def drawScreen(bounds, _x, _y, dir):
    if (dir % 4) == 0:
        roboChar = '^'
    elif (dir % 4) == 1:
        roboChar = '>'
    elif (dir % 4) == 2:
        roboChar = 'v'
    else:
        roboChar = '<'
    for y in range(bounds[2], bounds[3]+1):
        for x in range(bounds[0], bounds[1]+1):
            if (x,y) == (_x,_y):
                print(roboChar),
            elif ((x,y) in tileColor) and (tileColor[(x,y)] == 1):
                print('#'),
            else:
                print(' '),
        print("\n")




def updateBounds(x, y, bounds):
    if x < bounds[0]:
        bounds[0] = x
    if x > bounds[1]:
        bounds[1] = x
    if y < bounds[2]:
        bounds[2] = y
    if y > bounds[3]:
        bounds[3] = y
    return bounds

opfile = open("inputDay11.text", 'r')
intcode0 = opfile.readline().split(',')
intcodeRobot = [int(i) for i in intcode0]

robot = Computer(intcodeRobot)
color = 1
x = 0
y = 0
bounds = [0,0,0,0]
tileColor = dict()
tilesPainted = set()
countPainted = 0
direcVecs = [(0,-1), (1,0), (0,1), (-1,0)]
dir = 0
time = 0
while (robot.finished == False) and time < 10000:
    print("Robot is at position (" + str(x) + ", " + str(y) + ")")
    print("Robot pointer: " + str(robot.pointer))
    print("Val9: " + str(robot.intcode[9]))
    outs = robot.run([color])
    print("Input: " + str(color) +", Robot outputs: " + str(outs))
    if (x,y) not in tileColor:
        tileColor[(x,y)] = 0
    if tileColor[(x,y)] != outs[0]:
        tileColor[(x,y)] = outs[0]
        if (x,y) not in tilesPainted:
            tilesPainted.add((x,y))
            countPainted += 1
    # Update robot direction and move one space
    dir += (2*outs[1] - 1)
    x += direcVecs[dir % 4][0]
    y += direcVecs[dir % 4][1]
    bounds = updateBounds(x,y, bounds)
    # Read new tile color from camera
    if (x,y) in tileColor:
        color = tileColor[(x,y)]
    else:
        color = 0
        tileColor[(x,y)] = 0 # This might be unnecessary.
    time += 1

drawScreen(bounds, x, y, dir)
print("Count Painted: " + str(countPainted))
print("Time: " + str(time))
print("Finished: " + str(robot.finished))
