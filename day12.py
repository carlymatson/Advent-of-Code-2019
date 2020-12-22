



def parse(_string):
    vals = list()
    i = 0
    while i < len(_string):
        if _string[i] == '=':
            j = i+1
            while (_string[j] != ',') and (_string[j] != '>'):
                j += 1
            vals.append(int(_string[i+1 : j]))
            i = j+1
        i += 1
    return (vals + [0]*3)

opfile = open("inputDay12.text", 'r')
bodyList0 = opfile.readlines()
bodyList = [parse(body) for body in bodyList0]

print(bodyList)

def getEnergy(_bodyList):
    total = 0
    for _body in _bodyList:
        pot = 0
        kin = 0
        for i in range(3):
            pot += abs(_body[i])
            kin += abs(_body[i+3])
        total += pot*kin
    return total

#steps = 0
#while steps < 1000:
#    for body1 in bodyList:
#        for body2 in bodyList:
#            for i in range(3):
#                if body2[i] > body1[i]:
#                    body1[i+3] += 1
#                elif body2[i] < body1[i]:
#                    body1[i+3] += -1
#
#    for body in bodyList:
#        for i in range(3):
#            body[i] += body[i+3]
#
#    steps += 1

#print("After " + str(steps) + " steps: " + str(bodyList))
#print("Energy in system: " + str(getEnergy(bodyList)))


xyzPeriods = [0, 0, 0]
numBodies = len(bodyList)

for i in range(3):
    steps = 0
    states = set()
    stateL = [0]*(2*numBodies)
    for bodyNum in range(4):
        stateL[2*bodyNum] = bodyList[bodyNum][i]
        stateL[2*bodyNum + 1] = bodyList[bodyNum][i + 3]
    state = tuple(stateL)
    states.add(state)
    repeatedState = False
    while repeatedState == False and steps < 300000:
        steps += 1
        # Update velocity states
        for j in range(numBodies):
            for k in range(numBodies):
                if stateL[2*k] > stateL[2*j]:
                    stateL[2*j + 1] += 1
                if stateL[2*k] < stateL[2*j]:
                    stateL[2*j + 1] += -1
        for j in range(numBodies):
            stateL[2*j] += stateL[2*j + 1]
        newState = tuple(stateL)
        if newState in states:
            repeatedState = True
            xyzPeriods[i] = steps
            print("Repeated state found!")
            break
        else:
            states.add(newState)
        #print("New state: " + str(newState))
        #print("States: " + str(states))

print("Steps: " + str(steps))
print("Periods: " + str(xyzPeriods))

# Note: I computed the LCM using an online calculator because lazy.
