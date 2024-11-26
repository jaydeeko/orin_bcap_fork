import time

from bCAPClient.bcapclient import BCAPClient

#TODO learn how to set speed in code

# Example usage:



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
    base_position = {"X": 0, "Y": -360, "Z": 200, "Indexdeg": 0, "Pitch": 90}

    # Possible increments from the base position for Roll, Pitch, and Yaw (-45, -20, 0, 20, 45)
    indexincrements = [-200, 120, 175, 210, 310]
    pitchincrements = [0, 10, 20, 45]
    initial_position = [0, -360.5, 200, 90, 0, 0, -3]

    #Pose = [initial_position, "P", "@E"]
    #client.robot_move(robot_handle, 2, Pose, move_speed)

    joint_positions = [-90, 40, 57, 0, 0, -20]  # Example positions for 6 joints
    #client.robot_execute(robot_handle, "MoveJ", "J(-90, 40, 57, 0, 0, -20)")
    #client.robot_move(robot_handle, 1, "J(-90, 40, 57, 0, 0, -20)")
    #client.robot_execute(robot_handle, "MoveJ", "[-90, 40, 57, 0, 0, -20]")

    Pose = [joint_positions, "J"]
    client.robot_move(robot_handle, 1, Pose, move_speed)
    print("Start loop")



    for pitch in pitchincrements:
        for roll in indexincrements:
            yaw = 0


            facet = [base_position["X"], base_position["Y"], base_position["Z"], base_position["Pitch"], base_position["Indexdeg"], yaw]
            cut_position = GrindCut(facet, roll, pitch)
            Pose = [cut_position, "CP", "@E"]
            client.robot_move(robot_handle, 2, Pose, move_speed)

            facet = [base_position["X"], base_position["Y"], base_position["Z"]-45, base_position["Pitch"], base_position["Indexdeg"], yaw]
            cut_position = GrindCut(facet, roll, pitch)
            Pose = [cut_position, "CP", "@E"]
            client.robot_move(robot_handle, 2, Pose, move_speed)

            facet = [base_position["X"], base_position["Y"]+30, base_position["Z"]-50, base_position["Pitch"], base_position["Indexdeg"], yaw]
            cut_position = GrindCut(facet, roll, pitch)
            Pose = [cut_position, "CP", "@E"]
            client.robot_move(robot_handle, 2, Pose, move_speed)

            facet = [base_position["X"], base_position["Y"]+30, base_position["Z"], base_position["Pitch"], base_position["Indexdeg"], yaw]
            cut_position = GrindCut(facet, roll, pitch)
            Pose = [cut_position, "CP", "@E"]
            client.robot_move(robot_handle, 2, Pose, move_speed)


'''
Dependent on cut:
Rough pass -- approach from very high. 0.5mm 
mid pass -- 0.5mm approach, 


For each facet


'''







#Close
    client.robot_execute(robot_handle, "GiveArm")
    client.robot_release(robot_handle)
    client.controller_disconnect(controller_handle)

finally:
    # Stop the BCAP service
    client.service_stop()

