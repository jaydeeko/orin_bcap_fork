offline_mode = False #False = real run. True = test mode
indexwheelreal= 360/96 #Technically, degrees per index. Facetomatic uses this for planes.csv, doesn't impact CAM

#X1Y1, X2Y2 that cuts oscillate between
X1Y1 = [0, -450]
X2Y2 = [0, -350]

#Oscillation points for Girdle
GirdX1Y1 = [0, -300]
GirdX2Y2 = [0, -325]

ZtoTableOffset = 250  #Height from table to aluminum plate

PitchCal = 0
GirdleCal = 0


joint_positions = [-90, 40, 57, 0, 0, -20] #Safe position

#TODO use speedbase

# Rough (360), Medium (1200), Polish (3000), Final polish  (50k)

# LapProcesses = { # DiscHeight    ZDOC   ZDepthTot    SpeedBase          FlatSweep
#         "Rough":  [2,             .1,          12,         300,              5],
#         "Medium": [2,            0.05,          1,         200,              5],
#         "Polish": [2,            0.01,        0.2,         150,             10],
#         "FinPol": [12,           0.001,       0.05,        100,             50]
# }

LapProcesses = { # DiscHeight    ZDOC   ZDepthTot    SpeedBase          FlatSweep
        "Rough":  [2,            10,          10,         1,              2],
        "Medium": [2,            2,          1,         .8,              5],
        "Polish": [2,            2,        0.2,         .6,             10],
        "FinPol": [12,           2,       0.05,        .4,             50]
}


#=========================================
#Shouldnt ever change:

# Define connection parameters
HOST = "169.254.183.80"  # Replace with the robot's IP address
PORT = 5007  # Standard port for BCAP
TIMEOUT = 2000  # Timeout in milliseconds

# Robot parameters
robot_name = "vp6242a"  # Name of the robot in the controller
move_speed = "Speed=100"  # Movement speed

