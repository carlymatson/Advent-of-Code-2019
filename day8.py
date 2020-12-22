pixFile = open("inputDay8.text", 'r')
stri = pixFile.readline()

def countZeroes():
    pointer = 0
    minCount0 = 151 # The actual maximum is 150, so this is always over.
    product = 0
    while pointer < len(stri):
        subPoint = 0 # Pointer for individual layer
        count0 = 0
        count1 = 0
        count2 = 0
        while subPoint < 150 and pointer < len(stri):
            if stri[pointer].isspace():
                break
            num = int(stri[pointer])
            if num == 0:
                count0 += 1
            elif num == 1:
                count1 += 1
            elif num == 2:
                count2 += 1
            pointer += 1
            subPoint += 1
        if count0 < minCount0:
            minCount0 = count0
            product = count1 * count2
        if stri[pointer].isspace():
            break
    return product

def findPic():
    picArray = ['2']*150 # Start with a transparent picture.
    pointer = 0
    while pointer < len(stri):
        if stri[pointer].isspace():
            break
        if picArray[pointer % 150]=='2': # If transparent, replace.
            picArray[pointer%150] = stri[pointer]
        pointer+=1
    return picArray


#print("Final Product: " + str(countZeroes()))

picArray = findPic()
# Printing the picture:
for i in range(150):
    if picArray[i]=='2':
        picArray[i]=' '
    elif picArray[i]=='1':
        picArray[i]='#'
    elif picArray[i]=='0':
        picArray[i]=' '
for i in range(6):
    for j in range(25):
        print(str(picArray[25*i + j])),
    print("\n")
