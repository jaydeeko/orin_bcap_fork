from scipy.spatial.transform import Rotation as R
from math import radians
# TODO this doc should hold all of the if
from DashBoard import *
from GemCutHardcode import *

def pose_trans(p_from, p_from_to):
    position_from = p_from[:3]
    # Convert roll/pitch/yaw to a rotation object
    orientation_from = R.from_euler('xyz', p_from[3:], degrees=False)

    position_from_to = p_from_to[:3]
    orientation_from_to = R.from_euler('xyz', p_from_to[3:], degrees=False)

    # Transform position
    transformed_position = position_from + orientation_from.apply(position_from_to)
    # Combine rotations
    combined_rotation = orientation_from * orientation_from_to
    # Get the new orientation in Euler angles
    new_orientation = combined_rotation.as_euler('xyz', degrees=False)

    resulting_pose = np.concatenate((transformed_position, new_orientation[:3]))
    return resulting_pose

def GrindCut(facetdata, a=1, v=1):
    x, y, z, index, pitch = facetdata  # Unpack the target pose array

    #print(pitch, index)

    # Rotate N degrees around the tool's Z-axis
    tool_rotation = R.from_euler('z', radians(index), degrees=False)  # Tool's Z-axis rotation

    # Rotate M degrees around the world Y-axis
    world_rotation = R.from_euler('x', radians(pitch), degrees=False)  # World's Y-axis rotation

    # Initial rotation based on target pose
    initial_rotation = R.from_euler('xyz', [radians(90), 0, 0], degrees=False)

    # Combine rotations: First world Y-axis, then tool Z-axis relative to the tool frame
    combined_rotation = world_rotation * initial_rotation * tool_rotation

    # Get the final orientation as Euler angles
    final_orientation = combined_rotation.as_euler('xyz', degrees=True)

    # Create the real pose
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

def execute_grind_cut(client, robot_handle, facet, move_speed, offline_mode=True):

    """
    Execute a grind cut operation, with an optional offline mode to skip robot commands.
    :param client: The BCAPGrindCut Client instance
    :param robot_handle: The robot handle object
    :param facet: The facet data [facX, facY, facZ, facI, facP]
    :param move_speed: Movement speed setting
    :param offline_mode: If True, commands are not sent to the robot (testing mode)
    """

    cut_position = GrindCut(facet)
    Pose = [cut_position, "CP", "@E"]

    # TODO move to joint base at the END of every move (no dwell)

    if offline_mode:
        pass
        #print("moved", facet)
        #print(f"[Offline Mode] Skipped: robot_move with Pose={Pose} and move_speed={move_speed}")
    else:
        print(robot_handle, Pose, move_speed, client)
        client.robot_move(robot_handle, 2, Pose, move_speed)


def FacetLoop(row, step, client, robot_handle):
    """
    Main function to process a single row and execute the corresponding operations.
    """

    DiscHeight = LapProcesses[step][0]

    ZDOC = LapProcesses[step][1]
    ZDepthTot = LapProcesses[step][2]
    SpeedBase = LapProcesses[step][3]
    #TODO Utilize speedbase
    FlatSweeps = LapProcesses[step][4]


    # Prepares the robot for operation if not in offline mode
    if not offline_mode:
        Pose = [joint_positions, "J"]
        #TODO delete this: execute_grind_cut(client, robot_handle, Pose, move_speed, offline_mode)
        client.robot_move(robot_handle, 1, Pose, move_speed)
        print("Went to home")

    # Extract and calculate parameters
    # z_offset = float(row["ZIntercept"]) if row["ZIntercept"] != "N/A" else float(row["GirdleZ"])

    z_disc = DiscHeight + ZtoTableOffset + ZTweak  # Adjust for Z intercept and table offset
    Ztable = z_disc + ZTweak

    Zstart = Ztable + ZDepthTot

    # TODO pitch += pitchcal
    # TODO girdle_z += girdlecal

    index = float(row["Index"]) * indexwheelreal + Indexcheat
    pitch = abs(float(row["Pitch"])) + PitchTweak  # Ensure pitch is positive

    # girdle_z = abs(float(row["GirdleZ"])) if row["GirdleZ"] != "N/A" else 0.0

    yaw = 0

    facP = pitch
    facI = index  # Index in degrees

    # Set the TCP (tool center point) based on Z offset
    # TODO SUPER NEED DOP HEIGHT SET
    # TODO Set TCP based on Z intercept
    # TODO  tool_pose = [0.0, 0.0, Dopheight + Zintercept, 0.0, 0.0, 0.0]
    # TODO  client.robot_change(robot_handle, "Tool1", tool_pose)
    # client.robot_change(robot_handle, "Tool1", tool_pose)
    #print(f"Tool pose NOT SET")

    if offline_mode == True:
        # Execute pavilion/crown operations
        client = 0
        robot_handle = 0
        run_cycle_between_positions(client, robot_handle, X1Y1, X2Y2, Zstart, Ztable, ZDOC, facI, facP, move_speed, offline_mode)
        final_sweep(client, robot_handle, X1Y1, X2Y2, Ztable, FlatSweeps, facI, facP, move_speed, offline_mode)
    else:
        print("realrun")
        run_cycle_between_positions(client, robot_handle, X1Y1, X2Y2, Zstart, Ztable, ZDOC, facI, facP, move_speed, offline_mode)
        final_sweep(client, robot_handle, X1Y1, X2Y2, Ztable, FlatSweeps, facI, facP, move_speed, offline_mode)


    # print(X1Y1, X2Y2, Zstart, Ztable, ZDOC, facI, facP, move_speed, offline_mode)

    print("FacetLoop complete.")

def run_cycle_between_positions(client, robot_handle, X1Y1, X2Y2, Zstart, Zfinal, Zdelta, facI, facP, move_speed, offline_mode):
    """
    Cycle between two positions while lowering Z from Zstart to Zfinal, lowering Z by Zdelta/2 each step.
    """
    current_Z = Zstart
    if Zdelta <= 0:
        print("Error: Zdelta must be greater than 0 to lower Z.")
        return

    while current_Z > Zfinal:  # Use '>' to prevent infinite loop when current_Z equals Zfinal
        # Move to the first position
        facX, facY = X1Y1
        pose = [facX, facY, current_Z, facI, facP]
        execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)

        # Lower Z by Zdelta / 2
        current_Z = round(max(current_Z - (Zdelta / 2), Zfinal), 4)
        print(f"Lowered Z to {current_Z}")

        # Move to the second position
        facX, facY = X2Y2
        pose = [facX, facY, current_Z, facI, facP]
        execute_grind_cut(client, robot_handle, pose, move_speed, offline_mode)

        # Lower Z by another Zdelta / 2
        current_Z = round( max(current_Z - (Zdelta / 2), Zfinal), 4)
        print(f"Lowered Z to {current_Z}")

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

        #print(f"Completed sweep {sweep_count + 1} at Z={Zfinal}")
