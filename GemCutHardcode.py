indexwheelreal= 360/96

#Height from table to aluminum plate
ZtoTableOffset = 250

#z offset based on grit:
# Rough (360), Medium (1200), Polish (3000), Final polish  (50k)

#TODO use discheight
#TODO use Zcutstep
#TODO use speedbase
#TODO use flatsweep

#Zcutheight = [12, 1, 0.2, 0.05]
#                DiscHeight          Zcutstep       ZcutHeight    SpeedBase      FlatSweep
Rough       =    [2,                   .1,           12,            300,           2]
Medium      =    [2,                   .05,          1,             200,           5]
Polish      =    [2,                   .01,          0.2,           150,           10]
FinalPolish =    [12,                  .001,         0.05,          100,           50]

#X1Y1, X2Y2 that cuts oscillate between
X1Y1 = [0, -450]
X2Y2 = [0, -350]


#        Rough (360), Medium (1200), Polish (3000), Final polish  (50k)
#Total cut height, mm -> changed to softcode
#Zcutheight = [12, 1, 0.2, 0.05]





