orbitFile = open("inputDay6.text", 'r')
#orbitFile = open("testInputDay6.text", 'r')
orbits = orbitFile.readlines()
orbitGraph = dict()

for orbit in orbits:
    objs = orbit.rstrip().split(')')
    #if objs[0] in orbitGraph:
    #    orbitGraph[objs[0]].append(objs[1]) #Add to orbit list.
    #else:
    #    orbitGraph[objs[0]] = [objs[1]]  #Create new list with one orbit.
    orbitGraph[objs[1]] = objs[0] # Object 1 orbits around object 0.


def countOrbits(obj):
    count = 0
    if obj in orbitGraph:
        for satellite in orbitGraph[obj]:
            count += 1 # Count the direct orbit
            count += countOrbits(satellite)  #Count the indirect orbits
    return count

#orbitTotal = 0
#for obj in orbitGraph:
#    orbitTotal += countOrbits(obj)

#print(orbitTotal)

myCenters = list()
obj1 = "YOU"
center = ""
while obj1 in orbitGraph:
    if obj1 == "COM":
        break
    center = orbitGraph[obj1]
    myCenters.append(center)
    #print(str(obj1) + " is orbiting " + str(center))
    obj1 = center
santaCenters = list()
obj2 = "SAN" #Santa.
sharedObj = "COM"
while obj2 in orbitGraph:
    if obj2 == "COM":
        break
    center = orbitGraph[obj2]
    santaCenters.append(center)
    obj2 = center
    if center in myCenters:
        centralObj = center
        break

transferCount = len(santaCenters) - 1 #Transfers from Santa to center.
for cen in myCenters:
    if cen == centralObj:
        break
    else:
        transferCount += 1

print("Number of transfers: " + str(transferCount))
