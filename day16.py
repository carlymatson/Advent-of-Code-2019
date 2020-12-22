inFile = open("day16input.text", 'r')
input = inFile.readline().strip()

print "Input: " + input


def FFT(_input):
    N = len(_input)
    charList = []
    for i in range(N):
        digit = i + 1
        pattern = [0]*digit + [1]*digit + [0]*digit + [-1]*digit
        newDigit = 0
        for j in range(N):
            newDigit += int(_input[j]) * pattern[(j+1)%(4*digit)]
        charList.append(str(newDigit)[-1])
    return "".join(charList)

timer = 0

while timer < 100:
    print "%d: "%(timer) + input[:8]
    input = FFT(input)
    timer += 1

print "%d: "%(timer) + input[:8]
