instructionfile = open("inputDay3.text", 'r')
instructions = [line.split(',') for line in instructionfile.readlines()]


def walk(_oldPoint, _dir):
    vec = (0,0)
    if _dir == 'U':
        vec = (1,0)
    elif _dir == 'D':
        vec = (-1,0)
    elif _dir == 'R':
        vec = (0,1)
    elif _dir == 'L':
        vec = (0,-1)
    else:
        print("Something went wrong. _dir = " + str(_dir))
    newPoint = (_oldPoint[0] + vec[0], _oldPoint[1] + vec[1])
    return newPoint

wire1dist = dict()
stepCount = 0

oldPoint = (0,0)
newPoint = (0, 0)
pointsWire1 = set(oldPoint)
for inst in instructions[0]:
    dir = inst[0]
    steps = int(inst[1:])
    for i in range(steps):
        newPoint = walk(oldPoint, dir)
        pointsWire1.add(newPoint)
        stepCount += 1
        if newPoint not in wire1dist:
            wire1dist[newPoint] = stepCount
        oldPoint = newPoint


distance = -1
stepCount = 0
oldPoint = (0,0)
newPoint = (0, 0)

for inst in instructions[1]:
    dir = inst[0]
    steps = int(inst[1:])
    for i in range(steps):
        newPoint = walk(oldPoint, dir)
        stepCount += 1
        if newPoint in pointsWire1:
            #dist = abs(newPoint[0]) + abs(newPoint[1])
            dist = wire1dist[newPoint] + stepCount
            if dist == 0:
                pass
            elif (dist < distance) or (distance < 0):
                distance = dist
        oldPoint = newPoint

print(distance)
