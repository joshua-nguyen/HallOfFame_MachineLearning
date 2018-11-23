import numpy as np

class record_b(): #18 vars
    G    = 0
    AB   = 0
    R    = 0
    H    = 0
    SecB = 0
    TB   = 0
    HR   = 0
    RBI  = 0
    SB   = 0
    CS   = 0
    BB   = 0
    SO   = 0
    IBB  = 0
    HBP  = 0
    SH   = 0
    SF   = 0
    GIDP = 0

    def __init__(self, G, AB, R, H, SecB, TB, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH, SF, GIDP):
        self.G    = G
        self.AB   = AB
        self.R    = R 
        self.H    = H
        self.SecB = SecB
        self.TB   = TB 
        self.HR   = HR 
        self.RBI  = RBI
        self.SB   = SB 
        self.CS   = CS 
        self.BB   = BB 
        self.SO   = SO 
        self.IBB  = IBB
        self.HBP  = HBP
        self.SH   = SH 
        self.SF   = SF 
        self.GIDP = GIDP

    def __add__(self, other):
        assert type(self) is type(other)
        self.G    += other.G
        self.AB   += other.AB
        self.R    += other.R 
        self.H    += other.H
        self.SecB += other.SecB
        self.TB   += other.TB 
        self.HR   += other.HR 
        self.RBI  += other.RBI
        self.SB   += other.SB 
        self.CS   += other.CS 
        self.BB   += other.BB 
        self.SO   += other.SO 
        self.IBB  += other.IBB
        self.HBP  += other.HBP
        self.SH   += other.SH 
        self.SF   += other.SF 
        self.GIDP += other.GIDP

class batter():
    pid = ""
    year = ""
    stint = ""
    teamid = ""
    lgID = ""

    def __init__(self, pid, year, stint, teamid, lgID, record):
        self.pid = pid 
        self.year = year
        self.stint =    stint
        self.teamid =   teamid
        self.lgID =     lgID
        self.record = record
    
    def __eq__(self, other):
        return self.pid==other.get_id()

    def get_id(self):
        return self.pid
    
    def get_record(self):
        return self.record
    
    def add_record(self,other):
        self.record + other.get_record()

def list_find(a, obj):
    for i in a:
        if i == obj:
            return i
    return False



mlb_batting = np.genfromtxt(
    'mlb_Batting.csv',
    delimiter=',',
    dtype=None,
    missing_values={0:"", 'b':"N\A", 2:"???"},
    filling_values={0:0, 'b':0, 2:-999},
    names=[
        'playerID','yearID','stint','teamID','lgID','G','AB','R','H','2B','3B','HR','RBI','SB','CS','BB','SO','IBB','HBP','SH','SF','GIDP'
    ])
'''
mlb_pitching = np.genfromtxt(
    'mlb_Batting.csv',
    delimiter=',',
    dtype=None,
    names=[
        'playerID','yearID','stint','teamID','lgID','W','L','G','GS','CG','SHO','SV','IPouts','H','ER','HR','BB','SO','BAOpp','ERA','IBB','WP','HBP','BK','BFP','GF','R','SH','SF','GIDP'
    ])
'''
batters = []
count = 0
for i in mlb_batting:
    myrec=record_b(i[5],i[6],i[7],i[8],i[9],i[10],i[11],i[12],i[13],i[14],i[15],i[16],i[17],i[18],i[19],i[20],i[21])
    mybat = batter(i[0],i[1],i[2],i[3],i[4],myrec)
    found = list_find(batters, mybat)
    if found:
        found.add_record(mybat)
    else:
        batters.append(mybat)
    print(count)
    count+=1
np.savetxt("test.csv", batters, delimiter=",")
