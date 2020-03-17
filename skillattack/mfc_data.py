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

def getviable():
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
    print("MFC: %s\n5LP: %s\nSDP: %s\nTotal: %s"%(mfc,flp,sdp,len(scorelist)))

    return [mfc, flp, sdp, len(scorelist)]