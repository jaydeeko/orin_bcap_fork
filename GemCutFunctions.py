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

def GrindCut(target_pose, tool_z_angle, world_y_angle, a=1, v=1):
    x, y, z, roll, pitch, yaw = target_pose  # Unpack the target pose array
    print(world_y_angle, tool_z_angle)
    # Rotate N degrees around the tool's Z-axis
    tool_rotation = R.from_euler('z', radians(tool_z_angle), degrees=False)  # Tool's Z-axis rotation

    # Rotate M degrees around the world Y-axis
    world_rotation = R.from_euler('x', radians(world_y_angle), degrees=False)  # World's Y-axis rotation

    # Initial rotation based on target pose
    initial_rotation = R.from_euler('xyz', [radians(roll), radians(pitch), radians(yaw)], degrees=False)

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