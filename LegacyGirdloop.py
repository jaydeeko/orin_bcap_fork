def GirdzleLoop(row, step, client, robot_handle):
    tool_pose = [0, 0, Dopheight + (row["GirdleZ"] * Gemscale) + GirdleTweak - GirdleCal, 0, 0, 0]
    client.robot_execute(robot_handle, "SetToolDef", [1, tool_pose])

    current_tool_def = client.robot_execute(robot_handle, "GetToolDef", 1)
    print(f"Current dopheight is {current_tool_def[2]}")

    """
    Main function to process a single row and execute the corresponding operations.
    """

    DiscHeight = LapProcesses[step][0]

    ZDOC = LapProcesses[step][1]
    ZDepthTot = LapProcesses[step][2]
    SpeedBase = LapProcesses[step][3]
    # TODO Utilize speedbase
    FlatSweeps = LapProcesses[step][4]

    # Prepares the robot for operation if not in offline mode
    if not offline_mode:
        Pose = [joint_positions, "J"]
        client.robot_move(robot_handle, 1, Pose, move_speed)
        print("facetloopstart")

    z_disc = DiscHeight + ZtoTableOffset + ZTweak  # Adjust for Z intercept and table offset
    Ztable = z_disc + ZTweak

    Zstart = Ztable + ZDepthTot

    index = float(row["Index"]) * indexwheelreal + Indexcheat
    pitch = abs(float(row["Pitch"])) + PitchTweak + PitchCal  # Ensure pitch is positive

    facP = pitch
    facI = index  # Index in degrees

    # Set the TCP (tool center point) based on Z offset

    # client.robot_change(robot_handle, "Tool1", tool_pose)
    # print(f"Tool pose NOT SET")

    if offline_mode == True:
        # Execute pavilion/crown operations
        client = 0
        robot_handle = 0
        run_cycle_between_positions(client, robot_handle, GirdX1Y1, GirdX2Y2, Zstart, Ztable, ZDOC, facI, facP, move_speed / 2, offline_mode)
        final_sweep(client, robot_handle, X1Y1, X2Y2, Ztable, FlatSweeps, facI, facP, move_speed, offline_mode)
    else:
        print("realrun")
        run_cycle_between_positions(client, robot_handle, GirdX1Y1, GirdX2Y2, Zstart, Ztable, ZDOC, facI, facP, move_speed / 2, offline_mode)
        final_sweep(client, robot_handle, X1Y1, X2Y2, Ztable, FlatSweeps, facI, facP, move_speed, offline_mode)

    # print(X1Y1, X2Y2, Zstart, Ztable, ZDOC, facI, facP, move_speed, offline_mode)

    print("GirdLoop complete.")