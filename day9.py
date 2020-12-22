class Computer:


    def __init__(self, _intcode, _pointer = 0):
        self.intcode = _intcode
        self.pointer = _pointer
        self.length = len(_intcode)
        self.relBase = 0

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
                    input1 = inputs[0]
                    inputs = inputs[1:]
                else:
                    print("Suspending program")
                    self.pointer = pointer
                    break
                #print("Input number:")
                #input1 = input()
                result = input1
                self.store(pointer+1, input1, modes[0])

            elif opCode == 4:  # Print output
                numParams = 1
                output = self.get(pointer+1, modes[0])
                result = output
                print("Output: " + str(output))

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
            #print("Code: " + str(self.intcode[pointer : pointer + numParams+1])
                   #+ " , opcode = " + str(opCode)
                   #+ " numpar = " + str(numParams)
                   #+ ",\n\t result = " + str(result))
            pointer += (numParams +1)
            opCode = self.intcode[pointer]%100
            modes = [(self.intcode[pointer]%1000)/100,
                     (self.intcode[pointer]%10000)/1000,
                     (self.intcode[pointer]%100000)/10000]
        #print(str(output)+ ", " + str(finished))
        #print("----")
        return True

intcodeQuine = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

opfile = open("inputDay9.text", 'r')
intcode0 = opfile.readline().split(',')
intcodeDefault = [int(i) for i in intcode0]

x = Computer(intcodeDefault)
x.run([2])
