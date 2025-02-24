import time
import csv
from DashBoard_temp import *
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

        tool_pose = [[0, 0, Dopheight, 0, 0, 0], "P"]
        client.robot_execute(robot_handle, "SetToolDef", [1, tool_pose])


        current_tool_def = client.robot_execute(robot_handle, "GetToolDef", 1)
        print(f"Current dopheight is {current_tool_def[2]}")

        JointReset = [joint_positions, "J"]
        client.robot_move(robot_handle, 1, JointReset, move_speed_rapid)

    else:
        client = 0
        robot_handle = 0
         # Base position with fixed X, Y values and starting angles for Roll, Pitch, and Yaw at -90 degrees
        #base_position = {"X": 0, "Y": -360, "Z": 200}

    with open("planes.csv", mode="r") as file:
        reader = csv.DictReader(file)

        # Trim spaces from headers
        reader.fieldnames = [header.strip() for header in reader.fieldnames]

        #print(reader.fieldnames) #Debug column headers

        for row in reader:
            row = {key.strip(): value.strip() for key, value in row.items()}
            print(GemSteps)
            if ("Pav" in GemSteps)    and (row["Step"] == "Pav"):      FacetLoop(row, LapProcess, client, robot_handle)    # Pav
            if ("Crown" in GemSteps)  and (row["Step"] == "Crown"):    FacetLoop(row, LapProcess, client, robot_handle)    # Crown
            if ("Gird" in GemSteps) and (row["Step"] == "Gird"):   GirdleLoop(row, LapProcess, client, robot_handle)   # Girdle
            if ("CrownT" in GemSteps)  and (row["Step"] == "CrownT"):    FacetLoop(row, LapProcess, client, robot_handle)    # Crown Table
            if ("PavT" in GemSteps)  and (row["Step"] == "PavT"):     FacetLoop(row, LapProcess, client, robot_handle)    # Pav Table
            #TODO Think about adding a separate table loop function

    #Joint Reset to safe position
    client.robot_move(robot_handle, 1, JointReset, move_speed_rapid)

    if offline_mode == False:
        client.robot_execute(robot_handle, "GiveArm")
        client.robot_release(robot_handle)
        client.controller_disconnect(controller_handle)

finally:
    # Stop the BCAP service
    if offline_mode == False:
        client.service_stop()

