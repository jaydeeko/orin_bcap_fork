import time
import csv

from Python.bCAPClient.bcapclient import BCAPClient
from GemCutFunctions import *
from GemCutSoftcode import *
from GemCutHardcode import *

#TODO learn how to set speed in code

#Cutfilter = Pav, Gird, Crown, CrwnT, PavT
Cutfilter = "Pav"
#TODO -- filter moves based on step


# Define connection parameters
HOST = "169.254.183.80"  # Replace with the robot's IP address
PORT = 5007  # Standard port for BCAP
TIMEOUT = 2000  # Timeout in milliseconds

# Robot parameters
robot_name = "vp6242a"  # Name of the robot in the controller
move_speed = "Speed=100"  # Movement speed

offline_mode = True

try:
    if offline_mode == False:
        # The boring stuff
        client = BCAPClient(HOST, PORT, TIMEOUT)
        client.service_start()
        controller_handle = client.controller_connect("", "CaoProv.DENSO.VRC", "localhost", "")
        robot_handle = client.controller_getrobot(controller_handle, robot_name, "")
        client.robot_execute(robot_handle, "Motor", [1, 0])
        client.robot_execute(robot_handle, "TakeArm")
        time.sleep(1)
        client.robot_change(robot_handle, "Tool1")

        tool_pose = [0.0, 0.0, Dopheight, 0.0, 0.0, 0.0]
        client.robot_change(robot_handle, "Tool1", tool_pose)
    else:
        client = 0
        robot_handle = 0
         # Base position with fixed X, Y values and starting angles for Roll, Pitch, and Yaw at -90 degrees
        #base_position = {"X": 0, "Y": -360, "Z": 200}

    # Possible increments from the base position for Roll, Pitch, and Yaw (-45, -20, 0, 20, 45)

    #initial_position = [0, -360.5, 300, 90, 0, 0, -3]

    #Pose = [initial_position, "P", "@E"]
    #client.robot_move(robot_handle, 2, Pose, move_speed)

    joint_positions = [-90, 40, 57, 0, 0, -20]  # Example positions for 6 joints
    #client.robot_execute(robot_handle, "MoveJ", "J(-90, 40, 57, 0, 0, -20)")
    #client.robot_move(robot_handle, 1, "J(-90, 40, 57, 0, 0, -20)")
    #client.robot_execute(robot_handle, "MoveJ", "[-90, 40, 57, 0, 0, -20]")




    with open("planes.csv", mode="r") as file:
        # Use csv.DictReader to read rows with proper column headers
        reader = csv.DictReader(file)

        # Trim spaces from headers
        reader.fieldnames = [header.strip() for header in reader.fieldnames]

        # Debug column headers
        #print(reader.fieldnames)



        for row in reader:
            row = {key.strip(): value.strip() for key, value in row.items()}



            pitch = float(row["Pitch"])

            if row["Step"] == "Pav":

                Pose = [joint_positions, "J"]
                #execute_grind_cut(client, robot_handle, Pose, move_speed, offline_mode)
                #client.robot_move(robot_handle, 1, Pose, move_speed)


                z_offset = float(row["ZIntercept"]) if row["ZIntercept"] != "N/A" else row["GirdleZ"]
                z_offset = abs(z_offset)
                z_offset += ZtoTableOffset #TODO add discheight (modulated by cut step) here

#TODO           tool_pose = [0.0, 0.0, Dopheight, 0.0, 0.0, 0.0]
#TODO           client.robot_change(robot_handle, "Tool1", tool_pose)

                index = float(row["Index"]) * indexwheelreal
                index += Indexcheat

                pitch = float(row["Pitch"])
                pitch = abs(pitch)
                #TODO pitch += pitchcal

                girdle_z = float(row["GirdleZ"]) if row["GirdleZ"] != "N/A" else 0.0
                #TODO girdle_z += girdlecal
                yaw = 0 # Define the yaw (static in this example)

                # Construct the facet based on the row and base position
                facX = X1Y1[0]
                facY = X1Y1[1]
                facZ = z_offset
                facP = pitch
                facI = index #in degrees

                #TODO Set TCP based on Z intercept


                print(facX, facY, facZ, facI,  facP)

                pose = [facX, facY, facZ, facI,  facP]
                execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)


                pose = [facX, facY, facZ-45, facI,  facP]
                execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)



                pose = [facX, facY+30, facZ-50, facI,  facP]
                execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)


                #TODO cycle between x0y0 and x1y1 lowering Z from Zstart down to Zfinal

                pose = [facX, facY+30, facZ, facI,  facP]
                execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)


                #TODO cycle between x0y0 and x1y1 at final Z, number of counts equal to flatsweep

                    # Define the pose and move the robot






#TODO Add girdle functionality
    #Needs to use GirdleZ instead of Zint, NO tool offset
    #Needs girdlex1y1 and girdlex2y2



# Dependent on cut:
# Rough pass -- approach from very high. 0.5mm
# mid pass -- 0.5mm approach,
#
# For each facet





#Close
    if offline_mode == False:
        client.robot_execute(robot_handle, "GiveArm")
        client.robot_release(robot_handle)
        client.controller_disconnect(controller_handle)

finally:
    # Stop the BCAP service
    if offline_mode == False:
        client.service_stop()

