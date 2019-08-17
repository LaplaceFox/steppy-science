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
    def __init__(self, tagDict, ind): #takes an ouput from parse() and an index of which chart to read, copies relevant details
        chart = tagDict["NOTES"][ind] #get the chart we want
        chart = list(map(lambda x: x.strip(), chart.split(":"))) #split into properties
        self.notes = list(map(lambda x: x.strip().split("\n"), chart[-1].split(","))) #take just the notes, split into measures

        self.name = tagDict["TITLE"]
        self.artist = tagDict["ARTIST"]

        bpms = list(map(lambda x: x.strip(), tagDict["BPMS"].split(","))) #split into individual bpm changes
        self.bpms = list(map(lambda x: tuple(map(lambda y: float(y),x.split("="))), bpms)) #convert to (beat, BPM) pairs of floats

        #same but stops
        stops = list(map(lambda x: x.strip(), tagDict["STOPS"].split(","))) 
        if stops == [""]: #what if no stops?
            self.stops = [];
        else:
            self.stops = list(map(lambda x: tuple(map(lambda y: float(y),x.split("="))), stops))