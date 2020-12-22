mazeFile = open("inputDay18.text", 'r')
maze = mazeFile.readlines()

height = len(maze)
width = len(maze[0])
starts = []
doors = set()
allKeys = set()
explored = dict()

numKeys = 0
numKeysFound = 0
steps = 0




# Parse maze
for y in range(height):
    for x in range(width):
        ch = maze[y][x]
        if ch == '@':
            starts.append((x, y))
        if (ch >= 'A') and (ch <= 'Z'):
            doors.add(ch)
        if (ch >= 'a') and (ch <= 'z'):
            allKeys.add(ch)
            numKeys += 1
print("Num keys: " + str(numKeys))
#import pdb; pdb.set_trace()



class MazeState:

    def __init__(self, _roboLoc, _steps, _keys = set(), _prev = [None]*4):
        self.robotLocs = _roboLoc
        self.stepCount = _steps
        self.keysFound = _keys
        self.previous = _prev


    def __repr__(self):
        ret = ("State at " + str(self.robotLocs)
               + "\n\t with keys " + str(self.keysFound)
               + " and step count " + str(self.stepCount))
        return ret

    def getFrontier(self):
        frontier = list()
        for i in range(4):
            rLoc = self.robotLocs[i]
            for loc in getAdjacents(rLoc, self.previous[i]):
                vec = (loc[0]-rLoc[0], loc[1]-rLoc[1])
                stepsTaken = 1
                opts = getAdjacents(loc, rLoc)
                # If explored, check if we need anything that way.
                if (loc in explored and
                        len(explored[loc].difference(self.keysFound)) == 0):
                    continue
                # Continue down path.
                while (len(opts) == 1) and (charAt(loc) not in allKeys):
                    prevLoc = loc
                    loc = opts[0]
                    opts = getAdjacents(loc, prevLoc)
                    stepsTaken += 1
                # If new location is all explored, make note of that.
                if set(opts).issubset(explored.keys()):
                    stuffThatWay = set()
                    for path in opts:
                        stuffThatWay.union(explored[path])
                    explored[(rLoc[0]+vec[0], rLoc[1]+vec[1])] = stuffThatWay
                    continue
                # Create a new maze state.
                nRoLocs = list(self.robotLocs)
                nRoLocs[i] = loc
                nKeys = set(self.keysFound)
                if charAt(loc) in allKeys:
                    nKeys.add(charAt(loc))
                nSteps = self.stepCount + stepsTaken
                nPrev = list(self.previous)
                nPrev[i] = rLoc
                frontier.append(MazeState(nRoLocs, nSteps, nKeys, nPrev))
        return frontier


def charAt(_loc):
    return maze[_loc[1]][_loc[0]]

def getAdjacents(_loc, _prev = None):
    direcs = [(1,0), (0,1), (-1, 0), (0, -1)]
    x = _loc[0]
    y = _loc[1]
    adjs = list()
    for vec in direcs:
        newLoc = (x + vec[0], y + vec[1])
        if (charAt(newLoc) == '#' or newLoc == _prev):
            continue
        else:
            adjs.append(newLoc)
    return adjs



def markPath(_loc):
    adjs = getAdjacents(_loc)
    count = 0
    markPath = False
    adjKeyPaths = set()
    chr = maze[_loc[1]][_loc[0]]
    if chr >= 'a' and chr <= 'z':
        adjKeyPaths.add(chr)      # What if there are multiple?
        markPath = True
    for _loc2 in adjs:
        if _loc2 in explored:
            adjKeyPaths.union(explored[_loc2])
        else:
            count += 1
    if count == 1 or markPath == True:
        explored[_loc] = adjKeyPaths
        return True
    return False

startState = MazeState(starts, 0)

front = list(startState.getFrontier())
print("Front: " + str(front))

for st in front:
    print("State: " + str(st))
    print("Frontier: " + str(st.getFrontier()))
#frontier = [startState]



print("Step count: " + str(steps))
