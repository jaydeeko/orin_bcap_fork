GemName = "pc01346.stl"

ZcutheightTweak = 12 #Gets added to total cut height, mm. Should really only change for rough
#TODO This needs to be converted to a value that tweaks girdle vs dopheight

#TODO dipheight needs to be physically measured
#TODO Start by removing tool from dopholder
#Then put into straight down (table)
#remove cutting dist
#Get dop tool height, set as TCP
#Lower and stop on contact. Use this to define table top. This Z from table is "Z to table"
#Put on cutting disk, do this again. Use this to define cutting disc height
#Dop needs a height measuring tool, and a fixed line for mounting point (Reprint with real stop?)
#Tuning height will be separate values
#Girdletune   (Adds to girdleZ)
#Ztune        (adds to z intercepts)

#Notes: If GirdleZ is wrong, it impacts zints and girdlez, but all numbers need to be very close to correct or
#there will be a major mismatch, prone to crashes

ZDopTune = 0.0        #Adjusts the height of the disc from the table
GirdleTune = 0.0   #Z adjustment for girdle (cut deeper with negative numbers)




LapProcess = "Rough"  #Rough (360), Medium (1200), Polish (3000), Final polish  (50k)
GemSteps = ["PavT"] #= Pav, Gird, Crown, CrownT, PavT #TODO-- align labels

Gemscale = 6.0 #Gemscale -- multiplier for gem size. (Target length)/(Print sheet length)
#TODO -- Gemscale is radius of gem (as long as Gird Z =~1)





#Gets set every time a new gem is mounted
Dopheight = 30 + 67.0 #Length offset for dop Will have to learn how to measure this
#TODO correct dopheight


#Gets set to zero on new gem, and adjusted after gem flip
IndexOffset = 0.0   #Degrees of rotation to set dop. Total crapshoot w/ bad transfer dop





Indexcheat = 0 #Index Cheater -- offset that gets added each index. Set to 0 at start
PitchTweak = 0.0 #Pitch Cheater -- shouldnt change other than initial setup. Set to 0 at start

#Cut speed, normalized to 100
Cutspeed = 100

#TODO determine how to set speed in code
