recipe_file = open("inputDay14.text", 'r')

recipes = dict()
num_per_batch = dict()
extras = dict()
heights = dict()
heights["ORE"] = 0


# Do this for everything, somehow... Another while loop?
# if rescipes[this].keys().issubset(heights):
# ht = 0
# for key in keys():
#   if heights[key] > ht:
#       ht = heights[key]
#heights[this] = ht

# Parse file into recipe dictionary and number per batch.

for line in recipe_file.readlines():
    parts = line.split("=>")
    in_pairs = parts[0].strip().split(", ")
    out_pair = parts[1].strip().split(" ")
    chem = out_pair[1]
    recipes[chem] = dict()
    recipes[chem][chem] = int(out_pair[0])
    for pair in in_pairs:
        p = pair.strip().split(" ")
        recipes[chem][p[1]] = -int(p[0])


amount = dict()
amount["FUEL"] = -1
debts = {"FUEL"}
oreCount = 0

count = 0
finished = False
while len(debts) > 0 and count < 200:
    chem = debts.pop()
    #print("Chem:" + chem)
    #print("Amounts before: " + str(amount))
    #print("Debts before: " + str(debts))
    numBatches = -(amount[chem] / recipes[chem][chem])
    print("Recipe: " + str(recipes[chem]))

    for ingr in recipes[chem]:
        if ingr not in amount.keys():
            amount[ingr] = 0
        #print("Amount of ingr: " + str(amount[ingr]))
        #print("Amount change: " + str(recipes[chem][ingr]*numBatches))
        amount[ingr]+= recipes[chem][ingr]*numBatches
        if amount[ingr] < 0 and ingr!="ORE":
            debts.add(ingr)
    print("Amounts: " + str(amount))
    print("Debts: " + str(debts))
    print("-----")
    count += 1
