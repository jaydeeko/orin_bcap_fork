from scipy.spatial.transform import Rotation as R
from math import radians
from DashBoard_temp import *
from GemCutHardcode import *

def pose_trans(p_from, p_from_to):
    position_from = p_from[:3]
    orientation_from = R.from_euler('xyz', p_from[3:], degrees=False)

    position_from_to = p_from_to[:3]
    orientation_from_to = R.from_euler('xyz', p_from_to[3:], degrees=False)

    transformed_position = position_from + orientation_from.apply(position_from_to)
    combined_rotation = orientation_from * orientation_from_to
    new_orientation = combined_rotation.as_euler('xyz', degrees=False)

    resulting_pose = np.concatenate((transformed_position, new_orientation[:3]))
    return resulting_pose

def GrindCutPrime(facetdata):
    x, y, z, index, pitch = facetdata

    tool_rotation = R.from_euler('z', radians(index), degrees=False)
    #world_rotation = R.from_euler('x', radians(pitch), degrees=False)
    world_rotation = R.from_euler('x', radians(-pitch), degrees=False)


    #initial_rotation = R.from_euler('xyz', [radians(90), 0, radians(Yaw)], degrees=False)
    initial_rotation = R.from_euler('xyz', [radians(90), 0, radians(Yaw+180)], degrees=False)
    combined_rotation = world_rotation * initial_rotation * tool_rotation
    final_orientation = combined_rotation.as_euler('xyz', degrees=True)

    real_pose = [
        round(float(x), 4),
        round(float(y), 4),
        round(float(z), 4),
        round(float(final_orientation[0]), 4),
        round(float(final_orientation[1]), 4),
        round(float(final_orientation[2]), 4),
        -3
    ]
    return real_pose

def GrindCut(facetdata):
    x, y, z, index, pitch = facetdata
    tool_rotation = R.from_euler('z', radians(index), degrees=False)
    world_rotation = R.from_euler('x', radians(-pitch), degrees=False)

    initial_rotation = R.from_euler('xyz', [radians(90), 0, radians(Yaw+180)], degrees=False)
    #initial_rotation = R.from_euler('xyz', [radians(90), radians(0), radians(Yaw+180)], degrees=False)
    combined_rotation = world_rotation * initial_rotation * tool_rotation
    final_orientation = combined_rotation.as_euler('xyz', degrees=True)

    real_pose = [
        round(float(x), 4),
        round(float(y), 4),
        round(float(z), 4),
        round(float(final_orientation[0]), 4),
        round(float(final_orientation[1]), 4),
        round(float(final_orientation[2]), 4),
        -1
    ]
    return real_pose

def execute_grind_cut_prime(client, robot_handle, facet, move_speed, offline_mode=True):

    """
    :param facet: The facet data [facX, facY, facZ, facI, facP]
    :param move_speed: Movement speed setting
    :param offline_mode: If True, commands are not sent to the robot (testing mode)
    """

    cut_position = GrindCutPrime(facet)
    Pose = [cut_position, "@0"]

    if offline_mode:
        pass
        #print("moved", facet)
        #print(f"[Offline Mode] Skipped: robot_move with Pose={Pose} and move_speed={move_speed}")
    else:
        print("Pose Primed")
        client.robot_move(robot_handle, 1, Pose, "") #1 works, #2 is linear motion, but jams on figure

def execute_grind_cut(client, robot_handle, facet, move_speed, offline_mode=True):

    """
    :param facet: The facet data [facX, facY, facZ, facI, facP]
    :param move_speed: Movement speed setting
    :param offline_mode: If True, commands are not sent to the robot (testing mode)
    """

    cut_position = GrindCut(facet)
    Pose = [cut_position, "@0"]

    if offline_mode:
        pass
        #print("moved", facet)
        #print(f"[Offline Mode] Skipped: robot_move with Pose={Pose} and move_speed={move_speed}")
    else:
        #print("Z target = ", cut_position[2])
        client.robot_move(robot_handle, 2, Pose, "") #1 works, #2 is linear motion, but jams on figure

def FacetLoop(row, step, client, robot_handle):

    tool_pose = [[0, 0, Dopheight - abs(ZDopTune) + abs((float(row["ZIntercept"]) * Gemscale)), 0, 0, 0], "P"]
    client.robot_execute(robot_handle, "SetToolDef", [1, tool_pose])

    current_tool_def = client.robot_execute(robot_handle, "GetToolDef", 1)
    print(f"Current dopheight is {current_tool_def[2]}")

    DiscHeight = LapProcesses[step][0] #TODO remove discheight from everywhere

    ZDOC = LapProcesses[step][1]
    ZDepthTot = LapProcesses[step][2]  #TODO maybe this should be an independent parameter
    SpeedBase = LapProcesses[step][3]
    #TODO Utilize speedbase, or change speedbase to string based on step column
    FlatSweeps = LapProcesses[step][4]


    # Prepares the robot for operation if not in offline mode
    if not offline_mode:
        Pose = [joint_positions, "J"]
        client.robot_move(robot_handle, 1, Pose, move_speed_rapid)
        print("facetloopstart")

    z_disc = DiscHeight + ZtoTableOffset   # Adjust for Z intercept and table offset ##TODO Align ZTweak to girdle, used differently
    ZStop = z_disc

    Zstart = ZStop + ZDepthTot

    index = float(row["Index"]) * indexwheelreal + Indexcheat
    pitch = abs(float(row["Pitch"])) + PitchTweak  # Ensure pitch is positive

    facP = pitch
    facI = index  # Index in degrees


    # if offline_mode == True:
    #     # Execute pavilion/crown operations
    #     client = 0
    #     robot_handle = 0
    #     run_cycle_between_positions(client, robot_handle, X1Y1, X2Y2, Zstart, Ztable, ZDOC, facI, facP, move_speed, offline_mode)
    #     final_sweep(client, robot_handle, X1Y1, X2Y2, Ztable, FlatSweeps, facI, facP, move_speed, offline_mode)
    # else:

    if abs(float(row["Pitch"])) >= GirdleBoundary:
        print("NotGirdle")
        run_cycle_prime(client, robot_handle, X1Y1, X2Y2, Zstart + 0.0001, Zstart, ZDOC, facI, facP, Move_Speed_Cut, offline_mode) #TODO fix
        run_cycle_between_positions(client, robot_handle, X1Y1, X2Y2, Zstart, ZStop, ZDOC, facI, facP, Move_Speed_Cut, offline_mode)
        final_sweep(client, robot_handle, X1Y1, X2Y2, ZStop, FlatSweeps, facI, facP, Move_Speed_Cut, offline_mode)

    if abs(float(row["Pitch"])) < GirdleBoundary:
        print("Girdleish")
        run_cycle_prime(client, robot_handle, GirdX1Y1, GirdX2Y2, Zstart + 0.0001, Zstart, ZDOC, facI, facP, Move_Speed_Cut, offline_mode)  #TODO FIX
        run_cycle_between_positions(client, robot_handle, GirdX1Y1, GirdX2Y2, Zstart, ZStop, ZDOC, facI, facP, Move_Speed_Cut, offline_mode)
        final_sweep(client, robot_handle, GirdX1Y1, GirdX2Y2, ZStop, FlatSweeps, facI, facP, Move_Speed_Cut, offline_mode)

    # print(X1Y1, X2Y2, Zstart, Ztable, ZDOC, facI, facP, move_speed, offline_mode)

    print("FacetLoop complete.")

def GirdleLoop(row, step, client, robot_handle):
    # Determine the Z offset based on conditions
    #TODO Girdle needs less space

    tool_pose = [[0, 0, Dopheight - ZDopTune, 0, 0, 0], "P"] #This P should never change

    client.robot_execute(robot_handle, "SetToolDef", [1, tool_pose])

    current_tool_def = client.robot_execute(robot_handle, "GetToolDef", 1)
    print(f"Current dopheight is {current_tool_def[2]}")

    """
    Main function to process a single row and execute the corresponding operations.
    """

    #Define Zintercept
    GirdleZ = float(row["GirdleZ"]) * Gemscale


    DiscHeight = LapProcesses[step][0]
    ZDOC = LapProcesses[step][1]

    #ZDepthTot = LapProcesses[step][2]
    ZDepthTot = abs(MaxMaterialDiameter/2 - GirdleZ + 5)

    SpeedBase = LapProcesses[step][3]
    FlatSweeps = LapProcesses[step][4]

    # Prepares the robot for operation if not in offline mode
    if not offline_mode:
        Pose = [joint_positions, "J"]
        client.robot_move(robot_handle, 1, Pose, move_speed_rapid)
        print("facetloopstart")

    z_disc = DiscHeight + ZtoTableOffset # Adjust for Z intercept and table offset
    Zstop = z_disc + GirdleTune + GirdleZ
    Zstart = Zstop + ZDepthTot


    index = float(row["Index"]) * indexwheelreal + Indexcheat
    pitch = abs(float(row["Pitch"])) + PitchTweak + PitchCal  # Ensure pitch is positive

    facP = pitch
    facI = index  # Index in degrees

    run_cycle_prime(client, robot_handle, GirdX1Y1, GirdX2Y2, Zstart, Zstop, ZDOC, facI, facP, Move_Speed_Cut, offline_mode)

    run_cycle_between_positions(client, robot_handle, GirdX1Y1, GirdX2Y2, Zstart, Zstop, ZDOC, facI, facP, Move_Speed_Cut, offline_mode)

    final_sweep(client, robot_handle, GirdX1Y1, GirdX2Y2, Zstop, FlatSweeps, facI, facP, Move_Speed_Cut, offline_mode)

    print("GirdLoop complete.")

def run_cycle_prime(client, robot_handle, X1Y1, X2Y2, Zstart, Zfinal, Zdelta, facI, facP, move_speed, offline_mode):
    """
    Cycle between two positions while lowering Z from Zstart to Zfinal, lowering Z by Zdelta/2 each step.
    """
    current_Z = Zstart
    facX, facY = X1Y1
    pose = [facX, facY, current_Z, facI, facP]
    execute_grind_cut_prime(client, robot_handle, pose, move_speed, offline_mode)


    print("Figure is primed")

def run_cycle_between_positions(client, robot_handle, X1Y1, X2Y2, Zstart, Zfinal, Zdelta, facI, facP, move_speed, offline_mode):
    """
    Cycle between two positions while lowering Z from Zstart to Zfinal, lowering Z by Zdelta/2 each step.
    """
    current_Z = Zstart
    if Zdelta <= 0:
        print("Error: Zdelta must be greater than 0 to lower Z.")
        return

    while current_Z > Zfinal:  # Use '>' to prevent infinite loop when current_Z equals Zfinal
        print("Current Z =", current_Z, "Z final =", Zfinal)
        # Move to the first position
        facX, facY = X1Y1
        pose = [facX, facY, current_Z, facI, facP]
        execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)

        # Lower Z by Zdelta / 2
        current_Z = round(max(current_Z - (Zdelta / 2), Zfinal), 4)

        # Move to the second position
        facX, facY = X2Y2
        pose = [facX, facY, current_Z, facI, facP]
        execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)

        # Lower Z by another Zdelta / 2
        current_Z = round( max(current_Z - (Zdelta / 2), Zfinal), 4)


    print("Zfinal reached. Cycle complete.")

def final_sweep(client, robot_handle, X1Y1, X2Y2, Zfinal, flatsweep, facI, facP, move_speed, offline_mode):
    """
    Perform a number of sweeps at the final Z level.
    """
    for sweep_count in range(flatsweep):
        # Move to the first position
        facX, facY = X1Y1
        pose = [facX, facY, Zfinal, facI, facP]
        execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)

        # Move to the second position
        facX, facY = X2Y2
        pose = [facX, facY, Zfinal, facI, facP]
        execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)

    pose = [facX, facY, Zfinal + 10, facI, facP]
    execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)
    #print(f"Completed sweep {sweep_count + 1} at Z={Zfinal}")


