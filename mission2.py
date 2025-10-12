# Mission 2
    # Turn right
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=200)# back up to 
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -90, -250, 250) #reposition to 
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -195, 0, velocity=500)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 67, -150, 250)
