GemName = "pc01346.stl"

#Then put into straight down (table)
#remove cutting dist
#Get dop tool height, set as TCP
#Lower and stop on contact. Use this to define table top. This Z from table is "Z to table"
#Dop needs a height measuring tool, and a fixed line for mounting point (Reprint with real stop?)
#Tuning height will be separate values

#Notes: If GirdleZ is wrong, it impacts zints and girdlez, but all numbers need to be very close to correct or
#there will be a major mismatch, prone to crashes

LapProcess = "Rough"    #INFO:       "Rough"         "Medium"          "Finish"          "FinPol"
#                                  Rough (360),   Medium (1200),    Polish (3000),   Final polish (50k)

Move_Speed_Cut = "Speed=100"

RoughDOC = 5           #This is the depth of cut for rough passes #FIXME This is not a good name. Not per pass DOC, total depth of process
#INFO: After a cut, add RoughDOC to ZDopTune and clear RoughDOC for new cut

ZDopTune = 5         #Adjusts the TCP  <--- #if you cut a 10mm OD disc and it measures 10.02, change this to 0.01
GirdleTune = 0.0       #Z adjustment for girdle (cut deeper with negative numbers)

MaxMaterialDiameter = 30

GemSteps = ["Pav"] #= Pav, Gird, Crown, CrownT, PavT

#TODO -- align labels

Gemscale = 12.0 #Gemscale -- multiplier for gem size
#INFO -- GemScale is radius of gem (as long as Gird Z =~1)

ZtoTableOffset = 187.68  #Height from table to aluminum plate, set with 67mm TCP and 90 degree setting on tool, lower to contact with disc
# was 200 before

#Gets set every time a new gem is mounted
Dopheight = 313.72 - ZtoTableOffset - 3    #Length offset for dop Will have to learn how to measure this

#INFO Use 67mm for TCP to determine tabletop (remove dop)
#INFO Measure this with the robot and dop mounted
#INFO Go into table cut mode and lower until contact. Set this as Dopheight
#INFO Then, use ZDopTune to influence positional motions after this point

Indexcheat = 0    #Index Cheater -- offset that gets added each index. Set to 0 at start
PitchTweak = 0.0  #Pitch Cheater -- shouldnt change other than initial setup. Set to 0 at start
