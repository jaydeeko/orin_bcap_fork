import time

import csv

from Python.bCAPClient.bcapclient import BCAPClient


from GemCutFunctions import *
from GemCutSoftcode import *
from GemCutHardcode import *

#TODO learn how to set speed in code

#Cutfilter = Pavilion, Crown, Girdle
Cutfilter = "Pavilion"
#TODO -- filter moves based on step


# Define connection parameters
HOST = "169.254.183.80"  # Replace with the robot's IP address
PORT = 5007  # Standard port for BCAP
TIMEOUT = 2000  # Timeout in milliseconds

# Robot parameters
robot_name = "vp6242a"  # Name of the robot in the controller
move_speed = "Speed=100"  # Movement speed



try:
    # The boring stuff
    client = BCAPClient(HOST, PORT, TIMEOUT)
    client.service_start()
    controller_handle = client.controller_connect("", "CaoProv.DENSO.VRC", "localhost", "")
    robot_handle = client.controller_getrobot(controller_handle, robot_name, "")
    client.robot_execute(robot_handle, "Motor", [1, 0])
    client.robot_execute(robot_handle, "TakeArm")
    time.sleep(1)
    client.robot_change(robot_handle, "Tool1")


     # Base position with fixed X, Y values and starting angles for Roll, Pitch, and Yaw at -90 degrees
    #base_position = {"X": 0, "Y": -360, "Z": 200}

    # Possible increments from the base position for Roll, Pitch, and Yaw (-45, -20, 0, 20, 45)
    indexincrements = [-200, 120, 175, 210, 310]
    pitchincrements = [0, 10, 20, 45]
    #initial_position = [0, -360.5, 300, 90, 0, 0, -3]

    #Pose = [initial_position, "P", "@E"]
    #client.robot_move(robot_handle, 2, Pose, move_speed)

    joint_positions = [-90, 40, 57, 0, 0, -20]  # Example positions for 6 joints
    #client.robot_execute(robot_handle, "MoveJ", "J(-90, 40, 57, 0, 0, -20)")
    #client.robot_move(robot_handle, 1, "J(-90, 40, 57, 0, 0, -20)")
    #client.robot_execute(robot_handle, "MoveJ", "[-90, 40, 57, 0, 0, -20]")

    Pose = [joint_positions, "J"]
    client.robot_move(robot_handle, 1, Pose, move_speed)


    with open("planes.csv", mode="r") as file:
        # Use csv.DictReader to read rows with proper column headers
        reader = csv.DictReader(file)

        # Trim spaces from headers
        reader.fieldnames = [header.strip() for header in reader.fieldnames]

        # Debug column headers
        print("Trimmed Headers in CSV:", reader.fieldnames)



        for row in reader:
            row = {key.strip(): value.strip() for key, value in row.items()}

            if float(row["Pitch"]) > 0:

                z_offset = float(row["ZIntercept"]) if row["ZIntercept"] != "N/A" else row["GirdleZ"]
                z_offset =+ ZtoTableOffset



                index = float(row["Index"]) * indexwheelreal
                pitch = float(row["Pitch"])
                girdle_z = float(row["GirdleZ"]) if row["GirdleZ"] != "N/A" else 0.0
                yaw = 0 # Define the yaw (static in this example)


                # Construct the facet based on the row and base position
                facX = X1Y1[0]
                facY = X1Y1[1]
                facZ = z_offset
                facP = pitch
                #TODO invert pitch (*-1) for pavilion vs crown
                facI = index #in degrees
                facYw = yaw

                #TODO Set TCP based on Z intercept
                print(X1Y1[1])
                print(facY)

                # Initial position
                facet = [facX, facY, facZ, facP,  facI, facYw]
                cut_position = GrindCut(facet)
                Pose = [cut_position, "CP", "@E"]
                print(Pose)
                client.robot_move(robot_handle, 2, Pose, move_speed)

                facet = [facX, facY, facZ-45, facP, facI, facYw]
                cut_position = GrindCut(facet)
                Pose = [cut_position, "CP", "@E"]
                client.robot_move(robot_handle, 2, Pose, move_speed)

                facet = [facX, facY+30, facZ-50, facP, facI, facYw]
                cut_position = GrindCut(facet)
                Pose = [cut_position, "CP", "@E"]
                client.robot_move(robot_handle, 2, Pose, move_speed)

                #TODO cycle between x0y0 and x1y1 lowering Z from Zstart down to Zfinal

                facet = [facX, facY+30, facZ, facP, facI, facY]
                cut_position = GrindCut(facet)
                Pose = [cut_position, "CP", "@E"]
                client.robot_move(robot_handle, 2, Pose, move_speed)

                #TODO cycle between x0y0 and x1y1 at final Z, number of counts equal to flatsweep

                    # Define the pose and move the robot










# Dependent on cut:
# Rough pass -- approach from very high. 0.5mm
# mid pass -- 0.5mm approach,
#
# For each facet







#Close
    client.robot_execute(robot_handle, "GiveArm")
    client.robot_release(robot_handle)
    client.controller_disconnect(controller_handle)

finally:
    # Stop the BCAP service
    client.service_stop()

