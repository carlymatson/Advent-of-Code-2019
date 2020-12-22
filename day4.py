maximum = 790572
minimum = 245182

def getDigit(_number, _place):
    modNum = _number % (10**(_place+1))
    digit = modNum / (10**_place)
    return digit

def getDigits(_num):
    digList = [getDigit(_num, i) for i in range(6)]
    return digList

def toInt(_digitList):
    sum = 0
    for i in range(6):
        sum += _digitList[i]*(10**i)
    return sum

def increment(_digitList, _place):
    # Increment.
    _digitList[_place] += 1
    # Carry the one.
    if _digitList[_place] == 10:
        if _place == 5:
            #print("False bc _place")
            return False
        increment(_digitList, _place+1)
    for i in range(_place):
        _digitList[i] = _digitList[_place]
    return True


def check(_digitList):
    consecutive = True
    if _digitList[0]==_digitList[1] and _digitList[1] != _digitList[2]:
        return True
    if _digitList[4]==_digitList[5] and _digitList[3] != _digitList[4]:
        return True
    for i in range(1,4):
        if _digitList[i]==_digitList[i+1] and _digitList[i+1]!=_digitList[i+2] and _digitList[i-1]!=_digitList[i]:
            return True
    return False



digitList = getDigits(minimum)

# Find the next non-decreasing number.
for i in range(5):
    if digitList[5-i-1] < digitList[5-i]:
        for j in range(5-i):
            digitList[j] = digitList[5-i]
        break

# From here, increase to the next non-decreasing number and check validity.
count = 0
while toInt(digitList) <= maximum:
    if check(digitList):
        count += 1
        print(toInt(digitList))
    increment(digitList, 0)


print("Answer: " + str(count))
