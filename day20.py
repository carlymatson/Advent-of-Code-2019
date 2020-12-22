mazeFile = open("inputDay18.text", 'r')
maze = mazeFile.readlines()

height = len(maze)
width = len(maze[0])
start = (0, 0)
doors = set()
found = dict()

numKeys = 0

# Parse maze
for y in range(height):
    for x in range(width):
        ch = maze[y][x]
        if ch == '@':
            start = (x, y)
        if (ch >= 'A') and (ch <= 'Z'):
            doors.add(ch)
        if (ch >= 'a') and (ch <= 'z'):
            numKeys += 1
#print("Start is at " + str(start))
#print("Doors: " + str(doors))

class MazeState:

    def __init__(self, _locs, _steps, _keys = set()):
        self.locations = _locs
        self.stepCount = _steps
        self.keysFound = _keys

    def __repr__(self):
        ret = ("State at " + str(self.location)
               + " with keys " + str(self.keysFound)
               + " and step count " + str(self.stepCount))
        return ret

    def worseThan(self, ms2):
        if ((self.keysFound).issubset(ms2.keysFound)
              and (self.stepCount >= ms2.stepCount)):
              return True
        return False

    def getAdjacent(self):
        for i in range(4):
            x = self.locations[i][0]
            y = self.locations[i][1]  ## Update all references to this.
            adjacents = set()
            direcs = [(1,0), (0,1), (-1, 0), (0, -1)]
            for vec in direcs:
                newLoc = (x + vec[0], y + vec[1])
                if ((newLoc[0] < 0) or (newLoc[0] >= width)
                        or (newLoc[1] < 0) or (newLoc[1] >= height)):
                    continue
                ch = maze[newLoc[1]][newLoc[0]]
                if (ch == '#'):
                    continue
                if ch in doors:
                    if ch.lower() in self.keysFound:
                        pass
                    else:
                        continue
                newKeys = set(self.keysFound)
                if (ch >= 'a') and (ch <= 'z'):
                    newKeys.add(ch)
                newState = MazeState(newLoc, self.stepCount +1, newKeys)
                worse = False
                if newLoc not in found:
                    found[newLoc] = list()
                else:
                    for oldState in found[newLoc]:
                        if newState.worseThan(oldState):
                            worse = True
                            break
                if worse != True:
                    found[newLoc].append(newState)
                    adjacents.add(newState)
            #print("Adjacents: " + str(adjacents))
        return adjacents

startState = MazeState(start, 0)
found[start] = [startState]

frontier = {startState}
allKeysFound = False
numKeysFound = 0
steps = 0
print("Num keys: " + str(numKeys))
while allKeysFound == False: # while end condition not met
    newStates = set()
    for state in frontier:
        newStates = newStates.union(state.getAdjacent())
    frontier = newStates
    #print("Frontier:")
    for state in frontier:
        if len(state.keysFound) > numKeysFound:
            numKeysFound = len(state.keysFound)
            print("Num keys found: " + str(numKeysFound))
        #print(state)
    if numKeysFound == numKeys:
        allKeysFound = True
        steps = state.stepCount

print("Step count: " + str(steps))
