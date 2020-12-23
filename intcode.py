class Computer:

    def __init__(self, intcode, pointer = 0):
        self.intcode = intcode
        self.pointer = pointer
        self.length = len(intcode)
        self.relative_base = 0

    def _pad(self, new_length):
        self.intcode = self.intcode + [0]*(new_length + 1 - self.length)
        self.length = len(self.intcode)

    def _get(self, parameter, mode):
        if parameter > self.length-1:
            self._pad(parameter + 1)
        val = 0
        if mode == 0: # Position mode
            position = self.get(parameter, 1)
            val = self.get(position, 1)
        elif mode == 1: # Immediate mode
            val = self.intcode[parameter]
        elif mode == 2: # Relative mode
            position = self.get(parameter, 1) + self.relative_base
            val = self.get(position, 1)
        return val

    def _store(self, parameter, value, mode): #Still need to catch negative vals.
        position = parameter
        if mode == 0:
            position = self._get(parameter, 1)
        elif mode == 2:
            position = self._get(parameter, 1) + self.relative_base
        else:
            print("Something wrong in self._store")
            return False
        if position > self.length-1:
            self._pad(position + 1)
        self.intcode[position] = value
        return True

    def run(self, inputs = []):
        output = None
        pointer = self.pointer
        num_parameters = 1
        finished = False
        while pointer < self.length:
            operator_code = self.intcode[pointer]%100
            modes = [int( self.intcode[pointer]%(10**(i+3))/(10**(i+2)) ) for i in range(3)]
            result = None
            if operator_code == 1: # Add
                num_parameters = 3
                num1 = self._get(pointer+1, modes[0])
                num2 = self._get(pointer+2, modes[1])
                result = num1 + num2
                self._store(pointer+3, result, modes[2])
            elif operator_code == 2: # Multiply
                num_parameters = 3
                num1 = self._get(pointer+1, modes[0])
                num2 = self._get(pointer+2, modes[1])
                result = num1 * num2
                self._store(pointer+3, result, modes[2])
            elif operator_code == 3: # Take input
                num_parameters = 1
                if len(inputs) > 0:
                    input1 = inputs.pop(0)
                else:
                    print("Suspending program") # Note: Only for specific usage.
                    self.pointer = pointer
                    break
                #print("Input number:")
                #input1 = input()
                result = input1
                self._store(pointer+1, input1, modes[0])
            elif operator_code == 4:  # Output
                num_parameters = 1
                output = self._get(pointer+1, modes[0])
                result = output
                print("Output: " + str(output))
            elif operator_code == 5: # Jump if Nonzero
                num_parameters = 2
                if self._get(pointer+1, modes[0]) != 0:
                    pointer = self._get(pointer+2, modes[1])
                    num_parameters = -1
                    result = pointer
                else:
                    result = -1
            elif operator_code == 6: # Jump if Zero
                num_parameters = 2
                if self._get(pointer+1, modes[0]) == 0:
                    pointer = self._get(pointer+2, modes[1])
                    num_parameters = -1
                    result = pointer
                else:
                    result = -1
            elif operator_code == 7: # Write 1 if less than
                num_parameters = 3
                if self._get(pointer+1, modes[0]) < self._get(pointer+2, modes[1]):
                    result = 1
                else:
                    result = 0
                self._store(pointer+3, result, modes[2])
            elif operator_code == 8: # Write 1 if equal
                num_parameters = 3
                if self._get(pointer+1, modes[0]) == self._get(pointer+2, modes[1]):
                    result = 1
                else:
                    result = 0
                intcode = self._store(pointer+3, result, modes[2])
            elif operator_code == 9: # Adjust relative base
                num_parameters = 1
                change = self._get(pointer+1, modes[0])
                #result = self.relative_base + change # Is this ever used?
                self.relative_base += change
            elif operator_code == 99:
                finished = True
                break
            else:
                print("Something went wrong.")
            pointer += (num_parameters+1)
        return True
