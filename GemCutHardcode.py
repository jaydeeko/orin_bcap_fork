from DashBoard_temp import RoughDOC

offline_mode = False #False = real run. True = test mode
#TODO Convert to "RealRun" -> True when running. If RealRun = True

indexwheelreal= 360/96 #Technically, degrees per index. Facetomatic uses this for planes.csv to determine facet number, gemcut uses it to calc back to angles

#X1Y1, X2Y2 that cuts oscillate between
X1Y1 = [0, 325]
X2Y2 = [-27, 375]

#Oscillation points for Girdle
GirdX1Y1 = [0, 325]
GirdX2Y2 = [0, 330]

Yaw = 0 #Positive numbers trail the gem on a clockwise rotation

ZtoTableOffset = 187.68  #Height from table to aluminum plate, set with 67mm TCP and 90 degree setting on tool, lower to contact with disc
# was 200 before

#ZtoTableOffset = 400
#Use this for test mode

#TODO permanently fixture the machine, this is a huge pain to deal with on setup

PitchCal = 0
GirdleCal = 0

GirdleBoundary = 25.0 # Below this value, pav and crown facets will use

#joint_positions = [-90, 40, 57, 0, 0, -20] #Safe position
#joint_positions = [-90, 12, 155, 0, -70, -20] #Safe position
joint_positions = [94, 17, 101, 0, 30, 55]

#TODO use speedbase

# Rough (360), Medium (1200), Polish (3000), Final polish  (50k)

#TODO For lap processes, DOC can be converted to an absolute height using max material diameter so that initial rough pass is tight

LapProcesses = { # DiscHeight    ZDOC    ZDepthTot    SpeedBase          FlatSweep
        "Rough":  [0,             0.1,        RoughDOC,         300,              5],
        "Medium": [0,            0.05,         .1,         200,              5],
        "Polish": [0,            0.01,        0.01,         150,             10],
        "FinPol": [0,           0.001,       0.05,        100,             50]
}


#=========================================
#Shouldnt ever change:

# Define connection parameters
HOST = "169.254.183.80"  # Replace with the robot's IP address
PORT = 5007  # Standard port for BCAP
TIMEOUT = 2000  # Timeout in milliseconds

# Robot parameters
robot_name = "vp6242a"  # Name of the robot in the controller
move_speed_rapid = "Speed=100"  # Movement speed

