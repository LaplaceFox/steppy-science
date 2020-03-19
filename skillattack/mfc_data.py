from music_list_parser import Song, Chart

'''
Chart:
    id: song number + difficulty name (ex. 573ESP)
    name: song name + [difficulty name] (ex. Yamato nadenade Kaguya-hime[ESP])
    diff_name: (ex. ESP)
    diff_num: (ex. 14)

    getScores(): returns a list of all non-zero scores
'''

#1 point viable charts: 8-10 Difficulty, DSP, ESP, CSP only

def getViable():
    viables = []

    f = open("master_music.txt")
    musiclines = f.readlines()
    f.close()

    for line in musiclines:
        thisSong = Song(line)
        for chart in thisSong.charts(True,False):
            if chart.diff_name in ["DSP","ESP","CSP"] and 8 <= chart.diff_num <= 10:
                viables.append(chart)
    return viables

def breakdown(chart): #modify later to take score cutoffs and labels as input
    scorelist = chart.getScores()

    sdp, flp, mfc = 0, 0, 0

    for score in scorelist:
        if score == 1000000:
            mfc += 1
        if score >= 999950:
            flp += 1
        if score >= 999900:
            sdp += 1

    #debug
    #print("MFC: %s\n5LP: %s\nSDP: %s\nTotal: %s"%(mfc,flp,sdp,len(scorelist)))

    return [mfc, flp, sdp, len(scorelist)]

def cmetrics(brkdwn, a, b, succession = False):
    #if succession == True, we use Laplace's Rule of Succession (no relation)
    mfc   = brkdwn[0]
    flp   = brkdwn[1]
    sdp   = brkdwn[2]
    total = brkdwn[3]

    if succession:
        mfc += 1
        flp += 2
        sdp += 3
        total += 4

    return (mfc + a*flp + b*sdp) / total

def precomputeBreakdowns():
    viablelist = getViable()
    f = open("1point-viable-breakdowns.txt","w")
    f.write("chartID;MFC;5LP;SDP;Total\n")

    for i in range(len(viablelist)):
        print("[%s/%s]"%(i+1,len(viablelist)))
        chart = viablelist[i]
        brks = list(map(lambda x: str(x), breakdown(chart)))
        f.write(chart.id + ";" + ";".join(brks) + "\n")
    f.close()

def computeMetrics(a, b, succession = False):
    viablelist = getViable()
    chartDict = {}
    for chart in viablelist:
        chartDict[chart.id] = chart

    f = open("1point-viable-breakdowns.txt")
    lines = f.readlines()[1:]
    f.close()

    metriclist = [] #list of pairs of (metric, ID)

    for line in lines:
        line = line.split(";")
        chartID = line[0]
        brkdwn = list(map(lambda x: int(x), line[1:])) #remove the id, convert to int
        metric = cmetrics(brkdwn, a, b, succession)

        metriclist.append((metric, chartID))

    metriclist.sort()
    metriclist = metriclist[::-1] #sort from largest to smallest

    f = open("metric_out.txt","w")

    f.write("Metric used: (#MFC + %s*#L5P + %s*#SDP) / #scores\n"%(a,b))
    nextline = "Laplace's rule of succession used: "

    if succession:
        f.write(nextline + "Yes\n\n")
    else:
        f.write(nextline + "No\n\n")

    for (metric, chartID) in metriclist:
        title = chartDict[chartID].name
        f.write("%s : %.5f\n"%(title,metric))
    f.close()