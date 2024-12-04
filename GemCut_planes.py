import time
import csv
from DashBoard import *
from GemCutHardcode import *

from Python.bCAPClient.bcapclient import BCAPClient
from GemCutFunctions import *





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

        current_tool = client.robot_execute(robot_handle, "CurTool")
        #print(f"Current tool in use is Tool{current_tool}")

        current_tool_def = client.robot_execute(robot_handle, "GetToolDef", 1)
        #print(f"Current tooldef is {current_tool_def}")

        tool_pose = [0, 0, Dopheight, 0, 0, 0]
        client.robot_execute(robot_handle, "SetToolDef", [1, tool_pose])

        current_tool_def = client.robot_execute(robot_handle, "GetToolDef", 1)
        print(f"Current dopheight is {current_tool_def[2]}")


        JointReset = [joint_positions, "J"]
        client.robot_move(robot_handle, 1, JointReset, move_speed)





    else:
        client = 0
        robot_handle = 0
         # Base position with fixed X, Y values and starting angles for Roll, Pitch, and Yaw at -90 degrees
        #base_position = {"X": 0, "Y": -360, "Z": 200}

    # Possible increments from the base position for Roll, Pitch, and Yaw (-45, -20, 0, 20, 45)

    #initial_position = [0, -360.5, 300, 90, 0, 0, -3]

    #Pose = [initial_position, "P", "@E"]
    #client.robot_move(robot_handle, 2, Pose, move_speed)

      # Example positions for 6 joints
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

            if (GemStep == "Pav")    and (row["Step"] == "Pav"):      FacetLoop(row, LapProcess, client, robot_handle)    # Pav
            if (GemStep == "Crown")  and (row["Step"] == "Crown"):    FacetLoop(row, LapProcess, client, robot_handle)    # Crown
            #if (GemStep == "Girdle") and (row["Step"] == "Girdle"):   GirdleLoop(row, LapProcess, client, robot_handle)   # Girdle
            if (GemStep == "CwrnT")  and (row["Step"] == "CrwnT"):    FacetLoop(row, LapProcess, client, robot_handle)    # Crown Table
            if (GemStep == "PavT")   and (row["Step"] == "PavT"):     FacetLoop(row, LapProcess, client, robot_handle)    # Pav Table
            #TODO Add girdle functionality

    #Needs to use GirdleZ instead of Zint, NO tool offset
    #Needs girdlex1y1 and girdlex2y2



# Dependent on cut:
# Rough pass -- approach from very high. 0.5mm
# mid pass -- 0.5mm approach,
#
# For each facet

    client.robot_move(robot_handle, 1, JointReset, move_speed)


#Close
    if offline_mode == False:
        client.robot_execute(robot_handle, "GiveArm")
        client.robot_release(robot_handle)
        client.controller_disconnect(controller_handle)

finally:
    # Stop the BCAP service
    if offline_mode == False:
        client.service_stop()

