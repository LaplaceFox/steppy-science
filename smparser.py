from copy import deepcopy as copy

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
        self.measures = list(map(lambda x: x.strip().split("\n"), chart[-1].split(","))) #take just the notes, split into measures

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
        
        self.measuresToNotes()

        self.beatsToSec()

    def measuresToNotes(self):
        notes = []
        for i in range(len(self.measures)):
            measure = self.measures[i]
            div = len(measure) #division within measure
            for j in range(div):
                if measure[j] != "0000":
                    beat = (i + j/div) * 4
                    notes.append((beat, measure[j]))
        self.notes = notes

    def beatsToSec(self): #scan through chart, keeping track of the next BPM change or stop, converting beat differences to seconds
        bpms = copy(self.bpms)
        assert(len(bpms) > 0) #need to have an initial bpm

        (lastBeat,curBPM) = bpms.pop(0)
        assert(lastBeat == 0) #make sure the first BPM is actually at the beginning
        lastTime = 0

        taggedNotes = list(map(lambda x: (x[0], 0, x[1]), self.notes)) #replace (beat, note) with (beat, 0, note)
        taggedStops = list(map(lambda x: (x[0], 1, x[1]), self.stops)) #replace (beat, sec) with (beat, 1, sec)
        taggedBPMS = list(map(lambda x: (x[0], 2, x[1]), bpms)) #replace (beat, bpm) with (beat, 2, bpm)

        events = sorted((taggedNotes + taggedStops + taggedBPMS))
        
        notetimes = []

        for (beat, etype, val) in events:
            if etype == 1: #stop
                lastBeat = beat
                lastTime += val
            else:
                beatDiff = beat - lastBeat
                timeDiff = 60/curBPM * beatDiff

                lastBeat = beat
                lastTime += timeDiff
                if etype == 0:
                    notetimes.append((lastTime, val))
                else:
                    curBPM = val

        firstTime = notetimes[0][0]
        self.notetimes = list(map(lambda x: (round(x[0]-firstTime,4),x[1]), notetimes))
        print(self.notetimes)