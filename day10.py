spaceFile = open("inputDay10.text", 'r')
spaceRows = spaceFile.readlines()
cols = len(spaceRows[0])

astLocs = set()
for y in range(len(spaceRows)):
    for x in range(len(spaceRows[y])):
        if  spaceRows[y][x]  == '#':
            astLocs.add((x, y))

print(astLocs)

mostSeen = 0
bestAst = (0,0)
numSeenFrom = dict()
for ast1 in astLocs:
    #print("Ast loc: " + str(ast1))
    countSeen = 0
    linesOfSight = set()
    for ast2 in astLocs:
        slope = (ast2[0] - ast1[0], ast2[1] - ast1[1])
        seen = True
        for line in linesOfSight:
            if slope[0]*line[1]-slope[1]*line[0] == 0 and (slope[0]*line[0] > 0 or slope[1]*line[1]>0):
                seen = False
                print("I seen slope " + str(slope) +" at line " + str(line))
                break
        if seen:
            linesOfSight.add(slope)
            countSeen += 1
    #print("Seen: " + str(linesOfSight))
    #print("Count: " + str(countSeen))
    numSeenFrom[ast1] = countSeen
    if countSeen > mostSeen:
        mostSeen = countSeen
        bestAst  = ast1

for y in range(len(spaceRows)):
    for x in range(cols):
        if (x, y) in astLocs:
            print(numSeenFrom[(x,y)]),
        else:
            print(' '),
    print("\n")

print("Number of asteroids: " + str(len(astLocs)))
print("Final Count Seen:" + str(mostSeen - 1)) # Don't count the asteroid itself.
