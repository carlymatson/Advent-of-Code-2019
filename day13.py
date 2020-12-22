class Computer:

    def __init__(self, _intcode, _pointer = 0):
        self.intcode = _intcode
        self.pointer = _pointer
        self.length = len(_intcode)
        self.relBase = 0
        self.outputs = list()

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
        pointer = self.pointer
        opCode = self.intcode[pointer]%100
        modes = [(self.intcode[pointer]%1000)/100,
                 (self.intcode[pointer]%10000)/1000,
                 (self.intcode[pointer]%100000)/10000]
        #relBase = self.relBase
        numParams = 1
        finished = False
        while pointer < self.length:
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
                    input1 = inputs.pop(0)
                else:
                    drawScreen(self.outputs)
                    print("Input 1, 2, or 3: ")
                    try:
                        input1 = int(input()) - 2
                    except:
                        input1 = 0
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
                intcode = self.store(pointer+3, result, modes[2])

            elif opCode == 9: # Adjust relative base
                numParams = 1
                change = self.get(pointer+1, modes[0])
                result = self.relBase + change
                self.relBase += change
            elif opCode == 99:
                finished = True
                break
            else:
                print("Something went wrong.")
                print("Operator at position" + str(pointer)
                      +" is equal to " + str(self.intcode[pointer]))
            pointer += (numParams +1)
            opCode = self.intcode[pointer]%100
            modes = [(self.intcode[pointer]%1000)/100,
                     (self.intcode[pointer]%10000)/1000,
                     (self.intcode[pointer]%100000)/10000]

        return self.outputs


opfile = open("inputDay13.text", 'r')
intcode0 = opfile.readline().split(',')
intcodeDefault = [int(i) for i in intcode0]


def drawScreen(screenList):
    tiles = dict()
    maxX = 0
    maxY = 0
    i = 0
    while i+2 < len(screenList):
        x = screenList[i] # First two values specify coordinates. Third is tile ID.
        y = screenList[i+1]
        if x > maxX: # Huh?
            maxX = x
        if y > maxY:
            maxY = y
        tileId = screenList[i+2]
        # Want to know where the ball is? This is where to do it.
        tiles[(x,y)] = tileId
        i += 3
    print("Score: " + str(tiles[(-1,0)]))
    for y in range(maxY+1):
        for x in range(maxX+1):
            if (x,y) in tiles:
                drawTile(tiles[(x,y)])
        print("\n")

def drawTile(tileId):
    if tileId == 0:
        tileChar = ' '
    elif tileId == 1:
        tileChar = 'W'
    elif tileId == 2:
        tileChar = '+'
    elif tileId == 3:
        tileChar = '-'
    elif tileId == 4:
        tileChar = 'O'
    else:
        print("Something went wrong.")
    print(tileChar),

x = Computer(intcodeDefault)
x.run()
#blockCount = 0
