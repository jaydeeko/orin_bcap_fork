

#Current cut step
#Rough (360), Medium (1200), Polish (3000), Final polish  (50k)
Step = 'Rough'
#TODO -- select parameters based on cut step [if step=rough, A=rough[1], B=rough[2]]

#Gemscale -- Trying to make this either width or length
Gemscale = 25
#TODO -- multiply Z ints and girdleZ

#Index Cheater -- offset to each index. Ensure 0 at start
Indexcheat = 0
#TODO -- add this to all index moves

#Length offset for dop
Dopheight = 75
#TODO -- add this to tool offset


#Total cut height, mm
Zcutheight = 12
#Zcutheight = [12, 1, 0.2, 0.05]
#TODO factors in to STEP


#Length of gem to center? top of girdle? Cutoff for edge?
GemMiddle = 12
#TODO determine if this is needed. How to use? maybe it is "Girdle height?



#Cut speed, normalized to 100
Cutspeed = 100
#TODO Multiply move speeds by Cutspeed/100
#TODO determine how to set speed in code





#MediumCode (Adjustable but not likely to change

#Number of indices, moved to csv handler
# index = 96



