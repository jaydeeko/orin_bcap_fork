from scipy.spatial.transform import Rotation as R
from math import radians



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

def GrindCut(target_pose, a=1, v=1):
    x, y, z, index, pitch = target_pose  # Unpack the target pose array

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
    #print(real_pose)
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
        print("moved")
        #print(f"[Offline Mode] Skipped: robot_move with Pose={Pose} and move_speed={move_speed}")
    else:
        client.robot_move(robot_handle, 2, Pose, move_speed)
