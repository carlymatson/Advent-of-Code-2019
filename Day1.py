modfile = open("inputDay1.text", 'r')
modList = [line for line in modfile.readlines()]
#modList = [36]
total = 0
subtotal = 0
for module in modList:
    mass = int(module)
    fuelMass = mass / 3 - 2
    while fuelMass > 0:
        subtotal += fuelMass
        #print("Fuelmass = " + str(fuelMass))
        mass = fuelMass
        fuelMass = mass / 3 - 2
    total += subtotal
    subtotal = 0
print(total)

###
