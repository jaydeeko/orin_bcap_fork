GemName = "pc01346.stl"
LapProcess = "Rough"    #INFO:       "Rough"         "Medium"          "Finish"          "FinPol"
Move_Speed_Cut = "Speed=100"
RoughDOC = 12           #This is the depth of cut for rough passes
ZDopTune = 0.0         #Adjusts the TCP  <--- #if you cut a 10mm OD disc and it measures 10.02, change this to 0.01
GirdleTune = 0.0       #Z adjustment for girdle (cut deeper with negative numbers)
MaxMaterialDiameter = 0
GemSteps = ["PavT"] #= Pav, Gird, Crown, CrownT, PavT
Gemscale = 6.0 #Gemscale -- multiplier for gem size
Dopheight = 30 + 87.0 #Length offset for dop Will have to learn how to measure this
Indexcheat = 0    #Index Cheater -- offset that gets added each index. Set to 0 at start
PitchTweak = 0.0  #Pitch Cheater -- shouldnt change other than initial setup. Set to 0 at start
