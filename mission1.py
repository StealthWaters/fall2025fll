from hub import port, motion_sensor
import runloop, motor, motor_pair
motor_pair.pair(motor_pair.PAIR_1, port.E, port.C)
motion_sensor.reset_yaw
motion_sensor.get_yaw_face
print("part 1")

async def main():
    print(
    """The position of the robot should be the right wheel should be just covering the second line from the right 
    of the mission start and the fork all the way back | Mission 1""")
    motion_sensor.reset_yaw(0)
    motor.reset_relative_position(port.A, 0)
    await motor.run_for_degrees(port.A, 188, 360) # Move the fork down to the position
    
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -610, 0, velocity=610) # Move the robot to the first mission
   # if motion_sensor.get_yaw_face() > 0:
    print("thousand years of")
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 184, -250, 250) # Turn to face the first mission and sweep to the left
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -100, -250, 250) # Turn to sweep to the right
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=200) # Back up to let the brush settle
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 30, -250, 250) # Turn to face the mission after sweeping
    await runloop.sleep_ms(300) # Wait for the brush to stop moving
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -100, 0, velocity=125) # Thrust
    await motor.run_for_degrees(port.A, -103, 360) # Raise the fork up to pick up the brush
    
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 200, 0, velocity=600)
    await motor.run_for_degrees(port.A, 95, 160) # Raise the fork up to pick up the brush
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -550, 00, 500) # Turn to sweep to the right
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -300, 0, velocity=600) #do this cool turn to move out and face path to go to center
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -120, -500, 500) # turn to face colluseum next to fossil
    await runloop.sleep_ms(500) 
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -30, 0, velocity=610)
    await motor.run_for_degrees(port.A, 80, 360) #relase
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 50, 0, velocity=610)
    await motor.run_for_degrees(port.A, -80, 360) #relase
    #await motor.run_for_degrees(port.A, -147, 999999999) # Raise fork up to pick up the brush
runloop.run(main())
