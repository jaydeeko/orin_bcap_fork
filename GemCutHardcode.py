

#Height from table to aluminum plate
ZtoTableOffset = 150

#z offset based on grit:
# Rough (360), Medium (1200), Polish (3000), Final polish  (50k)
discheight = [2, 2, 2, 12]

#                DiscHeight          Zcutstep            SpeedBase      FlatSweep
Rough       =    [2,                   .1,                  300,           2]
Medium      =    [2,                   .05,                 200,           5]
Polish      =    [2,                   .01,                 150,           10]
FinalPolish =    [12,                  .001,                 100,          50]

#X1Y1, X2Y2 that cuts oscillate between
X1Y1 = [200, 200]
X2Y2 = [200, 205]


#        Rough (360), Medium (1200), Polish (3000), Final polish  (50k)
#Total cut height, mm -> changed to softcode
#Zcutheight = [12, 1, 0.2, 0.05]

indexwheelreal= 360/96

#Number of "flat transitions" in the process
flatsweep = [2, 5, 10, 50]

