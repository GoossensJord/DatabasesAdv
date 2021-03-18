begin = [1,0,0,0,0]
new = [1,0,0,0,0]
total = []
output = []
def testing(list):
    counter = 0
    for x in range(1,len(begin)):
        if counter < len(begin):
            new[counter] = begin[x-1] + begin[x]
            counter+=1
    testing(new)
