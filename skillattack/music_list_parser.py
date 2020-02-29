from urllib.request import urlopen
from urllib.parse import quote

class Song:
    def __init__(self, line):
        split = line.split("\t")
        # [id, -, GSP, BSP, DSP, ESP, CSP, BDP, DDP, EDP, CDP, title, artist]
        #  0   1  2    3    4    5    6    7    8    9    10   11     12
        self.id = split[0]
        self.singles = list(map(lambda x: int(x), split[2:7]))
        self.doubles = list(map(lambda x: int(x), split[7:11]))
        self.title = fixtitle(split[11])
        self.artist = split[12].strip()

    def __repr__(self):
        disp  = "Title: %s\n"%(self.title)
        disp += "Artist: %s\n"%(self.artist)

        #convert to strings
        singles = list(map(lambda x: str(x) if x > 0 else "-", self.singles))
        s_diffs = ["GSP", "BSP", "DSP", "ESP", "CSP"]

        #difficulty labels
        for i in range(len(s_diffs)):
            disp += "{}: {:>2}  ".format(s_diffs[i],singles[i])
        
        disp += "\n" + " "*9 #offset for next line

        #convert to strings
        doubles = list(map(lambda x: str(x) if x > 0 else "-", self.doubles))
        d_diffs = ["BDP", "DDP", "EDP", "CDP"]

        #difficulty labels
        for i in range(len(d_diffs)):
            disp += "{}: {:>2}  ".format(d_diffs[i],doubles[i])

        return disp

def fixtitle(title):
    url = "https://remywiki.com/index.php?search=" + title
    url = quote(url.encode('utf8'), ':/?=') #percent-encode the unicode characters
    html = urlopen(url).read()
    pagetitle = str(html).split("<title>")[1].split("</title>")[0]
    return pagetitle[:-11]