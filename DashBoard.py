GemName = "pc01346.stl"

ZcutheightTweak = 12 #Gets added to total cut height, mm. Should really only change for rough
Yaw = 0 #Positive numbers trail the gem on a clockwise rotation

LapProcess = "Rough"  #Rough (360), Medium (1200), Polish (3000), Final polish  (50k)
GemSteps = ["Pav", "Gird"] #= Pav, Gird, Crown, CrownT, PavT #TODO-- align labels

Gemscale = 10.0 #Gemscale -- multiplier for gem size. (Target length)/(Print sheet length)
#TODO -- Gemscale implemented but maybe suspect

Dopheight = 35.0 #Length offset for dop Will have to learn how to measure this

IndexOffset = 0.0   #Degrees of rotation to set dop. Total crapshoot w/ bad transfer dop
ZTweak = 0.0        #Adjusts the height of the disc from the table
GirdleTweak = 0.0   #Z adjustment for girdle (cut deeper with negative numbers)

Indexcheat = 0 #Index Cheater -- offset that gets added each index. Set to 0 at start
PitchTweak = 0.0 #Pitch Cheater -- shouldnt change other than initial setup. Set to 0 at start

#Cut speed, normalized to 100
Cutspeed = 100

#TODO determine how to set speed in code
