   await motor.run_for_degrees(port.A, 103, 360) # Raise the fork up to set up for pushing the lever
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -100) # Move forward to release the boulders
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100) # Back up
    await 
