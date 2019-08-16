def parse(path):
    tagDict = {"NOTES":[]}

    f = open(path)
    key, val = "", ""
    state = 0 #1: reading tag, 2: reading value
    for line in f:
        for char in line:           
            if state == 0:
                if char == "#":
                    state = 1
            elif state == 1:
                if char != ":":
                    key += char
                else:
                    state = 2
            else:
                if char != ";":
                    val += char
                else:
                    if key == "NOTES":
                        tagDict[key] += [val] #list of charts
                    else:
                        tagDict[key] = val
                    key, val = "", ""
                    state = 0

    return tagDict #effectively a song, with multiple charts

class Chart:
    def __init__(tagDict, ind): #takes an ouput from parse() and an index of which chart to read, copies relevant details
        pass